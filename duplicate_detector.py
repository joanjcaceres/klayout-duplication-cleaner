from pya import *

def detect_and_optionally_delete_duplicates(layers_to_check=None, delete_duplicates=True, specific_cell=None):
    """
    Detects overlapping identical shapes in specified layers of the current layout.
    Optionally deletes duplicates if delete_duplicates is set to True.
    
    Parameters:
    layers_to_check (list of tuple): List of (layer, datatype) tuples to check. If None, checks all layers.
    delete_duplicates (bool): If True, deletes duplicate shapes. Defaults to True.
    specific_cell (str): Name of a specific cell to check. If None, checks all top cells.
    """

    # Get the current layout and active cell
    layout_view = pya.Application.instance().main_window().current_view()
    
    if not layout_view:
        print("No layout view is open.")
        return

    cell_view = layout_view.active_cellview()
    layout = cell_view.layout()

    # Determine the cells to process
    cells_to_check = []
    if specific_cell:
        cell = layout.cell(specific_cell)
        if cell:
            cells_to_check.append(cell)
        else:
            print(f"Cell '{specific_cell}' not found.")
            return
    else:
        # If no specific cell is provided, use all top cells
        cells_to_check = [cell for cell in layout.top_cells()]

    if not cells_to_check:
        print("No top cells found in the layout.")
        return

    # Determine layers to check
    if layers_to_check is None:
        layers_to_check = [(layer_info.layer, layer_info.datatype) for layer_info in layout.layer_infos()]
    
    # Process each cell
    for cell in cells_to_check:
        print(f"Processing cell: {cell.name}")
        
        # Loop through specified layers
        duplicates_found = False
        for layer_number, datatype in layers_to_check:
            layer_index = layout.find_layer(layer_number, datatype)
            if layer_index < 0:
                print(f"Layer {layer_number}, Datatype {datatype} not found in the layout.")
                continue
            
            # Dictionary to store shape information for detecting duplicates in the current layer
            shape_dict = {}
            
            # Loop through each shape in the specified layer
            for shape in cell.shapes(layer_index):
                if shape.is_box() or shape.is_polygon() or shape.is_path():  # Check for standard shape types
                    bbox = shape.bbox()  # Get the bounding box of the shape
                    shape_str = str(bbox)  # Convert the bounding box to a string for dictionary keys

                    # Check if this shape already exists in the dictionary
                    if shape_str in shape_dict:
                        shape_dict[shape_str].append(shape)
                    else:
                        shape_dict[shape_str] = [shape]
            
            # Output results for the current layer
            for shapes in shape_dict.values():
                if len(shapes) > 1:  # If there are multiple identical overlapping shapes
                    if not duplicates_found:
                        print("Overlapping identical shapes found:")
                        duplicates_found = True
                    
                    # Convert bounding box coordinates to microns (µm)
                    bbox = shapes[0].bbox()
                    x_min = layout.dbu * bbox.left
                    y_min = layout.dbu * bbox.bottom
                    x_max = layout.dbu * bbox.right
                    y_max = layout.dbu * bbox.top
                    area_um2 = layout.dbu * layout.dbu * shapes[0].area()  # Area in square microns
                    
                    # Display the result with units in µm and the count of duplicates
                    print(f"Layer {layer_number}, Datatype {datatype}:")
                    print(f"  Duplicate shape at ({x_min:.5f}, {y_min:.5f}; {x_max:.5f}, {y_max:.5f}) with area {area_um2:.5f} µm²")
                    print(f"  Number of copies: {len(shapes)}")
                    
                    # If delete_duplicates is True, delete all but one instance of each duplicate
                    if delete_duplicates:
                        for shape in shapes[1:]:  # Keep the first shape and delete the rest
                            cell.shapes(layer_index).erase(shape)
                        print(f"  Deleted {len(shapes) - 1} duplicate(s)")

        if not duplicates_found:
            print("No overlapping identical shapes were found in the specified layers for cell:", cell.name)

# Example usage
# To detect duplicates without deleting in all top cells:
detect_and_optionally_delete_duplicates(specific_cell="Cell1", delete_duplicates=False)

# To detect and delete duplicates in all top cells:
# detect_and_optionally_delete_duplicates(delete_duplicates=True)

# To detect and delete duplicates only in a specific cell (e.g., "Cell1"):
# detect_and_optionally_delete_duplicates(specific_cell="Cell1", delete_duplicates=True)
