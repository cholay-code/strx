import tkinter as tk
from tkinter import *
from tkinter import ttk

import sys
import pyglet, os

# TODO: Look into DPI scaling and improve solution
FONT_SIZE = 14 if sys.platform == 'darwin' else 10
WINDOW_HEIGHT = 446 if sys.platform == 'darwin' else 420
WINDOW_WIDTH = 786 if sys.platform == 'darwin' else 785

# FLAT
# RAISED
# SUNKEN
# GROOVE
# RIDGE

# CONFIG
# TODO: export to YAML

COLORS = {
    'light_window_bg': "#989090",
    'dark_bg_label': "#585050",
    'light_input_guide_bg': "#BCB0B0",
    'light_label_bg': "#CCB0B0",
    'light_label_bg_1': "#DDD0D0",
    'light_label_bg_2': "#DDD0D0",
    'light_label_bg_3': "#E2C7C7",
    'light_readout_bg': "#E0E0E0",
    'dark_textbox_bg': "#282424",
    'light_textbox_bg': "#E5E5E5",
    'dark_queuebox_bg': "#180404",
    'dark_bg_input_text': "#481414",
    'dark_bg_highlight': '#DD4444',
    'dark_fg_text': "#DDD",
    'light_text_fg': "#111",
    'light_label_fg': "#200",
    'dark_element_fg': "#DDD",
    'dark_indent_fg': "#DDD",
    'dark_indent_bg': "#A55",
    'dark_quote_fg': "#225",
    'dark_quote_bg': "#FFF",
    'dark_delimiter_bg': "#513108",
    'dark_delimiter_fg': "#FFF",
    'dark_prefix_fg': "#2D2",
    'dark_suffix_fg': "#F2F",
    'light_help_bg': "#D8C0C0",
    'light_help_fg': "#500"
}

COLOR_MODE = 'light'

# Import fonts from files using pyglet (for Windows)
FONTS = {
    'fixed_width': ('Hack', FONT_SIZE),
    'sans_serif': ('Hack', FONT_SIZE)
}

if sys.platform != 'darwin':
    pyglet.font.add_file(os.path.join('..', 'fnt' , 'Hack-Regular.ttf'))
    pyglet.font.add_file(os.path.join('..', 'fnt' , 'VLOBJ.ttf'))
    FONTS = {
        'fixed_width': ('hack', FONT_SIZE),
        'sans_serif': ('vlobj', FONT_SIZE)
    }

FONTSIZE = {
    's': 14 if sys.platform == 'darwin' else 10,
    'm': 16 if sys.platform == 'darwin' else 12,
    'l': 20 if sys.platform == 'darwin' else 14
}

CONFIG = {
    'Window': {
        'title': 'StrX',
        'w': WINDOW_WIDTH,
        'h': WINDOW_HEIGHT,
        'bg': COLORS[COLOR_MODE+'_window_bg']
    },

    'InputLabel': {
        'bg': COLORS['dark_bg_label'],
        'fg': COLORS['dark_fg_text'],
        'h': 1,
        'w': 12,
        'padx': 2,
        'pady': 2,
        'bw': 2,
        'relief': SUNKEN,
        'font': FONTS['sans_serif']
    },

    'Text': {
        'bg': COLORS['dark_textbox_bg'],
        'fg': COLORS['dark_fg_text'],
        'h': 18,
        'w': 61,
        'padx': 2,
        'pady': 2,
        'relief': SUNKEN,
        'font': FONTS['fixed_width'],
        'bw': 1
    },

    'Queue': {
        'bg': COLORS['dark_queuebox_bg'],
        'fg': COLORS['dark_fg_text'],
        'h': 18,
        'w': 30,
        'padx': 2,
        'pady': 2,
        'relief': SUNKEN,
        'font': FONTS['fixed_width'],
        'bw': 1
    },

    'Label': {
        'bg': COLORS[COLOR_MODE + '_label_bg'],
        'bg1': COLORS[COLOR_MODE + '_label_bg_1'],
        'bg2': COLORS[COLOR_MODE + '_label_bg_2'],
        'bg3': COLORS[COLOR_MODE + '_label_bg_3'],
        'fg': COLORS[COLOR_MODE + '_label_fg'],
        'h': 1,
        'w': 10,
        'padx': 2,
        'pady': 2,
        'bw': 1,
        'relief': RIDGE,
        'font': FONTS['sans_serif'],
        'fontface': FONTS['sans_serif'][0],
        'fontsize': FONTSIZE['s']
    },

    'InputGuide': {
        'bg': COLORS[COLOR_MODE + '_input_guide_bg'],
        'fg': COLORS[COLOR_MODE + '_text_fg'],
        'highlight_bg': COLORS['dark_bg_highlight'],
        'h': 1,
        'w': 15,
        'padx': 2,
        'pady': 3,
        'bw': 1,
        'font': FONTS['sans_serif'],
	    'relief': RIDGE,
        'text_bg': COLORS['dark_bg_input_text']
    },

    'Input': {
        'bg': COLORS[COLOR_MODE + '_textbox_bg'],
        'fg': COLORS[COLOR_MODE + '_text_fg'],
        'highlight_bg': COLORS['dark_bg_highlight'],
        'h': 1,
        'w': 63,
        'padx': 3,
        'pady': 2,
        'bw': 1,
        'font': FONTS['fixed_width'],
	    'relief': RIDGE,
        'text_bg': COLORS['dark_bg_input_text']
    },

    'Readout': {
        'bg': COLORS[COLOR_MODE + '_readout_bg'],
        'fg': COLORS[COLOR_MODE + '_text_fg'],
        'h': 1,
        'w': 10,
        'padx': 2,
        'pady': 2,
        'bw': 1,
        'relief': RIDGE,
        'font': FONTS['fixed_width'],
        'fontface': FONTS['fixed_width'][0],
        'fontsize': FONTSIZE['s']
    },

    'Help': {
        'bg': COLORS[COLOR_MODE + '_help_bg'],
        'fg': COLORS[COLOR_MODE + '_help_fg'],
        'h': 18,
        'w': 60,
        'padx': 5,
        'pady': 5,
        'font': FONTS['fixed_width']
    }
}

SAMPLE_STRING = """Hilipati hilipati hilipampaa
Rimpatirillaa ripirapirullaa
Rumpatirumpa tiripirampuu
Jamparingaa rimpatiraparan
Tsupantupiran dillandu
Japat stilla dipudupu dullaa
Dumpatidupa lipans dullaa
Dipidapi dullaa rimpati rukan
Ribitit stukan dillandu
Jatsatsa barillas dilla lapadeian dullan deian doo
Joparimba badabadeia stulla
Laba daba daba dujan dillandu
Barillas dilla deiaduu badaba daga daga daga daga dujaduu
Badu dubi dubi dubi dejaduu
Badaba dillas dillan dejaduu"""