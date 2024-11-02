import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from pyrevit import forms
from System.Collections.Generic import List


doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get all linked documents
collector = FilteredElementCollector(doc)
linkInstances = collector.OfClass(RevitLinkInstance).ToElements()

# Create options for checkbox selection
link_options = {link.Name: link for link in linkInstances}

#print(link_options)

# Prompt user to select links

selected_links = forms.SelectFromList.show(link_options.keys(), title='Select Revit Links', width=500, height=400, button_name='Select Links', multiselect=True)

# Check if any links were selected
if not selected_links:
    print("No links selected. Exiting...")
    sys.exit()

# Get the actual link instances from selected names
selected_link_instances = [link_options[name] for name in selected_links]

# Define structural categories

structural_categories = {
    "Structural Foundations": BuiltInCategory.OST_StructuralFoundation,
    "Structural Columns": BuiltInCategory.OST_StructuralColumns,
    "Structural Framing (Beams)": BuiltInCategory.OST_StructuralFraming,
    "Structural Floors": BuiltInCategory.OST_StructuralFraming,
    "Walls": BuiltInCategory.OST_Walls,
    "Floors": BuiltInCategory.OST_Floors
}

# Show selection dialog for categories
selected_categories = forms.SelectFromList.show(
    structural_categories.keys(),
    title='Select Categories',
    width=500,
    height=400,
    multiselect=True,
    button_name='Select Categories'
)

if not selected_categories:
    print("No categories selected. Exiting...")
    sys.exit()

# Selection filter class for multiple categories
class MultiCategoryLinkedFilter(ISelectionFilter):
    def __init__(self, linkedDoc, categories):
        self.linkedDoc = linkedDoc
        self.categoryIds = [Category.GetCategory(linkedDoc, cat).Id 
                          for cat in categories]
    
    def AllowElement(self, element):
        return (element.Document == self.linkedDoc 
                and element.Category 
                and element.Category.Id in self.categoryIds)
    
    def AllowReference(self, reference, position):
        return True

try:
    # Get the selected link instances and categories
    selected_link_instances = [link_options[name] for name in selected_links]
    selected_builtin_categories = [structural_categories[name] for name in selected_categories]
    
    all_selected_elements = []  # Store all selected elements
    
    # Process each selected link
    for link_instance in selected_link_instances:
        linkedDoc = link_instance.GetLinkDocument()
        link_type = doc.GetElement(link_instance.GetTypeId())
        link_name = link_type.Parameter[BuiltInParameter.SYMBOL_NAME_PARAM].AsString()
        
        print("\nCollecting elements from {}:".format(link_name))
        
        # Collect elements for all selected categories in this link
        link_elements = []
        all_selected_element_ids = []
        
        
        for category in selected_builtin_categories:
            # Create collector for this category
            collector = FilteredElementCollector(linkedDoc)\
                .OfCategory(category)\
                .WhereElementIsNotElementType()\
                .ToElements()
            collectorTwo = FilteredElementCollector(linkedDoc)\
                .OfCategory(category)\
                .WhereElementIsNotElementType()\
                .ToElementIds()
            
            # Add elements to our lists
            category_elements = list(collector)
            link_elements.extend(category_elements)
            all_selected_elements.extend(category_elements)
            all_selected_element_ids.extend(collectorTwo)
            
            # Print count for this category
            category_name = Category.GetCategory(linkedDoc, category).Name
            print("- Found {} {} elements".format(len(category_elements), category_name))
        
        print("Total elements in {}: {}".format(link_name, len(link_elements)))
                
    # Print total count
    print("\nTotal elements collected across all links: {}".format(len(all_selected_elements)))
    
    # Optional: Print details of each element
    print("\nDetailed Element List:")
    for elem in all_selected_elements:
        print("- ID: {} - Category: {} - Link: {}".format(
            elem.Id, 
            elem.Category.Name, 
            elem.Document.Title
        ))
        print(all_selected_element_ids)

        
    if all_selected_element_ids:
        with Transaction(doc, "Copy Selected Elements In Place") as t:
            t.Start()
            copied_element_ids = List[ElementId](all_selected_element_ids)
            try:
                for link_instance in selected_link_instances:
                    linkedDoc = link_instance.GetLinkDocument()
                    transform = link_instance.GetTotalTransform()
                    
        
                
                
                    new_element_ids = ElementTransformUtils.CopyElements(
                    linkedDoc,
                    copied_element_ids,  # Element IDs to copy
                    doc,    # Current document
                    transform,                   # No translation (copy in place)
                    None
                    )
                print("\nSuccessfully copied {} elements.".format(len(copied_element_ids)))
        
            except Exception as e:
                print("Error copying elements: {}".format(e))
        
            t.Commit()
    
    else:
        forms.alert("No elements were selected for copying.")

except Exception as e:
    print("Error: {}".format(e))
