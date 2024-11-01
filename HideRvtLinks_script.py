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
active_view = doc.ActiveView

# Get all linked documents
collector = FilteredElementCollector(doc)
linkInstances = collector.OfClass(RevitLinkInstance).ToElements()

# Create options for checkbox selection
link_options = {link.Name: link for link in linkInstances}

#print(link_options)

# Prompt user to select links

selected_link_name = forms.SelectFromList.show(link_options.keys(), title='Select Revit Links', width=500, height=400, button_name='Select Links', multiselect=True)

# Check if any links were selected
if not selected_link_name:
    print("No links selected. Exiting...")
    sys.exit() 
    
selected_link_instances = [link_options[name] for name in selected_link_name]


#print(selected_link_instances.Id)
    
    # Start a transaction to hide the selected link in the current view
with Transaction(doc, "Hide Selected Link") as t:
    t.Start()
    
    try:
        linksIds = []
        for link_instance in selected_link_instances:
            linkedDoc = link_instance.GetLinkDocument()
            link_id = link_instance.GetTypeId()
            linksIds.extend([link_id])
        element_ids = List[ElementId](linksIds)
        active_view.HideElements(element_ids)
        #print("Successfully hid the selected link: {}".format(link_instance))
    except Exception as e:
        print("Error hiding link: {}".format(e))
    t.Commit()

