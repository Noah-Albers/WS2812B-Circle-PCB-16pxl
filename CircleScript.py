import pcbnew
import math

# Parameters
num_elms = 16
radius = 38.25*1000000*1.015
center_x = 118.5*1000000
center_y = 81.5*1000000
footprint_name = "TEXT"
offset = .18
index_rotation = -4
personal_rotation = 0 #deg

def sort_and_filter_handler(fp):
    if isinstance(fp, pcbnew.PCB_TEXT):
        try:
            return int(fp.GetText())
        except ValueError:
            return None
    return int(fp.GetReference()[1:])


def run():

    # Get the board
    board = pcbnew.GetBoard()

    # Find all elements on the board
    found_elements = []
    for fp in board.GetFootprints() + board.GetDrawings():
        compVal = fp.GetValue() if isinstance(fp,pcbnew.FOOTPRINT) else (
            "TEXT" if isinstance(fp,pcbnew.PCB_TEXT) else "unknown"
        )
        
        if footprint_name == compVal:
            found_elements.append(fp)
        elif footprint_name == "?":
            print(compVal)


    found_elements = [item for item in found_elements if sort_and_filter_handler(item) is not None]
    found_elements.sort(key=lambda led: sort_and_filter_handler(led))

    if len(found_elements) != num_elms:
        print("ERROR len(found_elements)=",len(found_elements),"!= ",num_elms)
        return

    # Calculate the angle between each LED
    angle_increment = 2 * math.pi / num_elms


    for i in range(num_elms):
        elm = found_elements[i]

        index_rotate = i+index_rotation

        angle = index_rotate * angle_increment

        x = int(center_x + radius * math.cos(angle+offset))
        y = int(center_y + radius * math.sin(angle+offset))
        
        # Set new position using VECTOR2I
        elm.SetPosition(pcbnew.VECTOR2I(x, y))

        if isinstance(elm, pcbnew.PCB_TEXT):
            elm.SetTextAngle(pcbnew.EDA_ANGLE(int(-math.degrees(angle)+personal_rotation)))
        else:
            elm.SetOrientation(pcbnew.EDA_ANGLE(int(-math.degrees(angle)+personal_rotation)))
        
    # Refresh the board to see changes
    pcbnew.Refresh()

def resize_text():
    # Load the current board
    b = pcbnew.GetBoard()

    # Iterate over all drawings on the board
    for item in b.GetDrawings():
        if isinstance(item, pcbnew.PCB_TEXT):
            # Check if the text is an integer
            try:
                text_value = int(item.GetText())
                # If the text can be converted to an integer, set the size and thickness
                new_text_size = pcbnew.VECTOR2I(3000000, 3000000)  # 3 mm x 3 mm in nanometers
                item.SetTextSize(new_text_size)

                new_thickness = 400000  # 0.4 mm in nanometers
                item.SetTextThickness(new_thickness)

                print(f"Updated text element: {item.GetText()} to size 3x3 mm and thickness 0.4 mm.")
            except ValueError:
                # If the text cannot be converted to an integer, skip it
                continue

    # Refresh the board to reflect changes
    pcbnew.Refresh()

    print("Board refreshed successfully.")    

run()
#resize_text()