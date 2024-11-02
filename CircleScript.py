import pcbnew
import math

# Parameters
num_leds = 16
radius = 38.25*1000000  # Radius of the circle in nanometers (5 mm)
center_x = 118*1000000  # Center X position in nanometers (10 mm)
center_y = 81*1000000  # Center Y position in nanometers (10 mm)

# Get the board
board = pcbnew.GetBoard()

# Find all LEDs on the board
leds = []
condis = []
for footprint in board.GetFootprints():
    if "WS2812B" in footprint.GetValue():  # Adjust this condition based on your LED footprint
        leds.append(footprint)
    elif "C" == footprint.GetValue():
        condis.append(footprint)


leds.sort(key=lambda led: int(led.GetReference()[1:]))
condis.sort(key=lambda led: int(led.GetReference()[1:]))

if len(leds) != len(condis) or len(leds) != num_leds:
    print("ERROR len(leds)=",len(leds),"!= len(condis)=",len(condis))
    condis = 1/0

# Calculate the angle between each LED
angle_increment = 2 * math.pi / num_leds

def move_obj(elm, i, offset, radius):
    
    angle = i * angle_increment
    x = center_x + int(radius * math.cos(angle+offset))
    y = center_y + int(radius * math.sin(angle+offset))
    
    # Set new position using VECTOR2I
    elm.SetPosition(pcbnew.VECTOR2I(x, y))

    # Set rotation (in degrees)
    elm.SetOrientation(pcbnew.EDA_ANGLE(int(-math.degrees(angle))))


for i in range(num_leds):
    led = leds[i]
    c = condis[i]

    index_rotate = i+9+3

    move_obj(led,index_rotate,0, radius)
    move_obj(c,index_rotate,-.12, radius*.93)
    
# Refresh the board to see changes
pcbnew.Refresh()
