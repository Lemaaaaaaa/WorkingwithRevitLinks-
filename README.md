# Revit Linked Elements Management Scripts

This repository contains three Python scripts designed for **pyRevit**. Each script serves to manage linked Revit documents in different ways within the current Revit project environment. These scripts allow users to:

1. **Copy elements from selected linked Revit models into the current document.**
2. **Hide selected linked Revit models in the active view.**
3. **Unhide previously hidden linked Revit models in the active view.**

Together, these scripts provide efficient tools for controlling visibility and data management of linked Revit models within a project, streamlining workflows that involve handling linked structural and architectural elements.

## Table of Contents

1. [Script 1: Copy Elements from Linked Models](#script-1-copy-elements-from-linked-models)
2. [Script 2: Hide Selected Linked Models](#script-2-hide-selected-linked-models)
3. [Script 3: Unhide Selected Linked Models](#script-3-unhide-selected-linked-models)
4. [Key Libraries and Classes](#key-libraries-and-classes)
5. [Conclusion](#conclusion)

---

## Script 1: Copy Elements from Linked Models

### Purpose

This script allows users to copy specific elements from selected linked Revit documents into the current project. It’s particularly useful when you need to reference structural elements from linked models, such as beams, columns, or foundations, in the active project environment.

### Workflow

1. **Collect Linked Documents**: The script first retrieves all linked Revit documents in the current project using `FilteredElementCollector` and `RevitLinkInstance`.
2. **User Selection of Links and Categories**: It then prompts the user to select the linked models and element categories they wish to copy.
3. **Filter Elements by Category**: Elements are filtered by the selected categories within each linked document.
4. **Copy Elements**: The filtered elements are copied into the current project, maintaining their original positions.
5. **Transaction Management**: The entire copy operation is handled within a Revit transaction to ensure model integrity.

### Key Methods

- `FilteredElementCollector.OfClass(RevitLinkInstance)`: Gathers linked documents.
- `forms.SelectFromList.show`: Presents a selection dialog for the user to choose links and categories.
- `ElementTransformUtils.CopyElements`: Copies elements from the linked model into the current document.

### Code Example

```python
collector = FilteredElementCollector(doc)
linkInstances = collector.OfClass(RevitLinkInstance).ToElements()

selected_link_name = forms.SelectFromList.show(
    link_options.keys(), title='Select Revit Links', width=500, height=400, button_name='Select Links', multiselect=True
)

# Filter and copy elements
element_ids = [link_instance.GetTypeId() for link_instance in selected_link_instances]
ElementTransformUtils.CopyElements(linkedDoc, element_ids, doc, transform, None)
