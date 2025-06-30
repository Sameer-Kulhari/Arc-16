import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import MatrixScanner
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.modules.rgb import RGB 
from kmk.extensions.display import Display
from kmk.extensions.display.display_oled import DisplayOLED 
from adafruit_display_text.label import Label
import terminalio


keyboard = KMKKeyboard()


keyboard.col_pins = (board.GPIO4, board.GPIO26, board.GPIO27, board.GPIO28)
keyboard.row_pins = (board.GPIO0, board.GPIO1, board.GPIO2, board.GPIO3)
keyboard.diode_orientation = MatrixScanner.DIODE_COL2ROW


keyboard.modules.append(Layers())


rgb = RGB(
    pixel_pin=board.GPIO29,
    num_pixels=9,
    rgb_order=(1, 0, 2),  # GRB
    brightness_limit=64,
    animation_speed=2.0,
)
rgb.default_rgb_effect = rgb.RGB_MODE_BREATHE_RAINBOW
keyboard.modules.append(rgb)


oled = DisplayOLED(
    width=128,
    height=32,
    sda=board.SDA,
    scl=board.SCL,
    addr=0x3C,
    rotate=0,
)
display = Display(oled)

# OLED for showing current layer name
def draw_oled(display_inst, keyboard):
    current_layer = keyboard.active_layers[0] if keyboard.active_layers else 0
    layer_names = ['Base', 'Fn', 'RGB']
    name = layer_names[current_layer] if current_layer < len(layer_names) else f'Layer {current_layer}'

    display_inst.clear_display_group()
    label = Label(terminalio.FONT, text=f'Layer: {name}', x=0, y=8)
    display_inst.display_group.append(label)

display.draw_callback = draw_oled
keyboard.extensions.append(display)



LAYER_FN = KC.TG(1)   
LAYER_RGB = KC.TG(2)  
LAYER_BASE = KC.TG(0) 

# Keymap
keyboard.keymap = [

    # Layer 0: Base
    [
        KC.ESC,  KC.Q,    KC.W,    KC.E,
        KC.A,    KC.S,    KC.D,    KC.F,
        KC.Z,    KC.X,    KC.C,    KC.V,
        LAYER_FN, KC.SPC, KC.ENT,  KC.BSPC,
    ],

    # Layer 1: Function Layer
    [
        KC.TILD, KC.N1,   KC.N2,   KC.N3,
        KC.N4,   KC.N5,   KC.N6,   KC.N7,
        KC.N8,   KC.N9,   KC.N0,   KC.MINS,
        LAYER_RGB, KC.LEFT, KC.DOWN, KC.RIGHT,
    ],

    # Layer 2: RGB Controls
    [
        KC.RGB_TOG, KC.RGB_MOD, KC.RGB_HUI, KC.RGB_HUD,
        KC.RGB_VAI, KC.RGB_VAD, KC.NO,      KC.NO,
        KC.NO,      KC.NO,      KC.NO,      KC.NO,
        LAYER_BASE,    KC.TRNS,    KC.TRNS,    KC.TRNS,
    ]
]

if __name__ == '__main__':
    keyboard.go()
