import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

HELP_TEXT = (
    'Keyboard Shortcuts:\n\n'
    '[C]: Copy To Clipboard\n'
    '[V]: Paste From Clipboard\n'
    '[A]: Alphabetise\n'
    '[B]: Remove blank elements\n'
    '[D]: Change Target Delimiter\n'
    '[F]: Find/Replace\n'
    '[J]: Cycle Casing\n'
    '[Q]: Edit Quote Character\n'
    '[S]: Specify Source Delimiter\n'
    '[T]: Remove whitespace\n'
    '[U]: Dedupe\n'
    '[X]: Copy, then Paste\n'
    '[[]: Edit Prefix\n'
    '[]]: Edit Suffix\n'
    '[Backspace]: Reset\n'
    '[Enter]: Apply'
)

class HelpFrame():
    def __init__(self, config):
        """
        Keybinding help section.
        """
        self.config = config.CONFIG['Help']

    def create(self):
        # print('HelpFrame create()')
        self.frame = tk.Frame()
        self.frame.grid(row=0, column=0, columnspan=12, rowspan=3, sticky='')

        label = Label(
            self.frame,
            anchor=tk.W,
            bg=self.config['bg'],
            fg=self.config['fg'],
            height=self.config['h'],
            width=self.config['w'],
            text=HELP_TEXT,
            justify=LEFT, 
            font=Font(family=self.config['font'][0], size=self.config['font'][1]),
            state=NORMAL,
            relief=GROOVE, 
            padx=self.config['padx'],
            pady=self.config['pady'],
            borderwidth=4
        )

        label.grid(row=1, column=8, sticky='news')

        self.label = label

    def destroy(self):
        # print('HelpFrame destroy()')
        self.frame.destroy()