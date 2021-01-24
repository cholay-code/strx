import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

import sys
import clipboard
import os

import Config

from StringManipulator import StringManipulator as StringManipulator
from StringManipulator import MODIFICATIONS

from gui import *

#####################################################
# StrX GUI
#   - chodelay / humphrey.fakenamington@gmail.com
#   - 2020-12
#
# TODO
# ----
#    GUI
#    X Help Section for modification keys
#    - Tidy up frames to match window size on Windows & Mac
#    - Disable/Enable Wrap / Colourization
#    - PgUp / PgDown scrolling
#    - Add highlight to "Find" terms
#
#    Functionality
#    - Pretty printing modes (use numeric keys)
#      - 1 SQL* (prioritize PSQL)
#      - 2 JSON
#      - 3 JSON to Object(s) (elaborate)
#      - 4 HTML
#    - Two layer delimiters (delim & line endings?)
#    X Fix buffer_to_buffer token duplication.
#    - recognise \r as an escape sequence
#    - (E)xtract awk-style
#    - (G)rep
#    - Clear start/end of line from matching Regex.
#	- Shortcut: M / N ? - / + ?
#    X Smart (R)eformatting e.g.
#      X $$ = self.$$
#      - NVL($this$, '') AS "$THIS$"
#      - $index$: $this$
#    - Smart Indent -> Remove common indent
#    - (#) Tabulate
#        - | col1 | col2   | column3 |
#        - | val1 | value2 | value3  |
#   - Presets
#    Codebase
#    - Export config to YAML file.
#    - Standalone application creation methods.
#       X Icon
#    - Clean out repo and get onto Github
#
######################################################

class AppWindow():
    """
    Main application window
    """
    def __init__(self):
        self.main = Frame()
        self.master = self.main.master

        self.sm = StringManipulator('')

        config = Config.CONFIG['Window']
        self.master.title(config['title'])
        self.master.geometry(f"{config['w']}x{config['h']}")
        self.master.configure(
            bg=config['bg']
        )
        self.master.resizable(height=False, width=False)
        self.master.iconbitmap(os.path.join('..', 'gfx', 'strx.ico'))

        self.stats = StatsFrame(Config, self.sm)
        self.stats.grid(row=0, column=0, columnspan=10, sticky='news')

        self.text_buffer = TextFrame(Config, self.sm)
        self.text_buffer.grid(row=1, column=0, columnspan=10, sticky='news')

        self.input = InputFrame(Config)
        self.input.grid(row=2, column=0, columnspan=8, sticky='news')

        self.help = HelpFrame(Config)

        self.events = EventHandler(self.master, self.sm, self.stats, self.help, self.text_buffer, self.input)
        self.events.copy_from_clipboard()


class EventHandler():
    mode = 'MAIN'
    func = ''

    find_buffer = ''
    replace_buffer = ''

    def __init__(self, master, sm, stats, help, text_buffer, input):
        self.master = master
        self.sm = sm
        self.stats = stats
        self.help = help
        self.text_buffer = text_buffer
        self.input = input
        self.bind_all()

    def change_mode(self, mode=None, func=None, input_label_text='', prefill=''):
        # print(f'EventHandler.change_mode({mode}, {func})')
        self.mode = mode if mode != None else 'MAIN'
        self.func = func if func != None else ''

        if mode == 'INPUT':
            self.input.activate(input_label_text, prefill)

    def bind_all(self):
        self.master.bind('<Return>', lambda x : self.enter())
        self.master.bind('<Escape>', lambda x : self.escape())
        self.master.bind('<BackSpace>', lambda x : self.reset())
        self.master.bind('x', lambda x : self.buffer_to_buffer())
        self.master.bind('c', lambda x : self.copy_to_clipboard())
        self.master.bind('v', lambda x : self.copy_from_clipboard())
        self.master.bind('s', lambda x : self.take_input('CURRENT_DELIMITER', 'Current Delimiter:'))
        self.master.bind('d', lambda x : self.take_input('TARGET_DELIMITER', 'Target Delimiter:'))
        self.master.bind('f', lambda x : self.take_input('FIND', 'Find:'))
        self.master.bind('[', lambda x : self.take_input('PREFIX', 'Prefix:'))
        self.master.bind(']', lambda x : self.take_input('SUFFIX', 'Suffix:'))
        self.master.bind('q', lambda x : self.take_input('QUOTE', 'Quote:'))
        self.master.bind('i', lambda x : self.take_input('INDENT', 'Indent:'))
        self.master.bind('r', lambda x : self.take_input('SMART', 'Smart Format:'))
        self.master.bind('j', lambda x : self.advance_casing_setting())
        self.master.bind('b', lambda x : self.toggle_transform(MODIFICATIONS.STRIP_BLANKS))
        self.master.bind('t', lambda x : self.toggle_transform(MODIFICATIONS.TRIM_WHITESPACE))
        self.master.bind('a', lambda x : self.toggle_transform(MODIFICATIONS.ALPHABETIZE))
        self.master.bind('u', lambda x : self.toggle_transform(MODIFICATIONS.DEDUPLICATE))
        self.master.bind('h', lambda x : self.toggle_help())

    def buffer_to_buffer(self):
        if self.mode == 'MAIN':
            self.sm.set_original_text(self.sm.current_text)
            self.sm.reset_state()
            self.text_buffer.refresh_text()

    def copy_to_clipboard(self):
        if self.mode == 'MAIN':
            clipboard.copy(self.sm.current_text)

    def copy_from_clipboard(self):
        if self.mode == 'MAIN':
            self.sm.set_original_text(clipboard.paste())
            self.text_buffer.refresh_text()

    def take_input(self, func, input_label_text=''):
        self.cancel_help()
        if self.mode == 'MAIN':
            self.change_mode('INPUT', func, input_label_text)

    def cancel_help(self):
        if self.mode == 'HELP':
            self.change_mode('MAIN')
            self.help.destroy()
            return True
        return False

    def enable_help(self):
        if self.mode == 'MAIN':
            self.change_mode('HELP')
            self.help.create()

    def toggle_help(self):
        if not self.cancel_help():
            self.enable_help()

    def toggle_transform(self, mod_name):
        self.cancel_help()
        if self.mode == 'MAIN':
            self.sm.toggle_boolean_modification(mod_name)

    def advance_casing_setting(self):
        if self.mode == 'MAIN':
            self.sm.advance_casing_setting()

    def reset(self):
        if self.mode == 'MAIN':
            self.sm.reset_state()

    def escape(self):
        """
        Handle Escape being pressed in all circumstances.
        In INPUT mode, return to MAIN mode and discard input.
        In MAIN mode, do nothing.
        """
        # Dismiss help panel if showing
        if not self.cancel_help():
            self.change_mode('MAIN', '')
            self.input.get_value_and_clear()
            self.text_buffer.textbox.focus_set()

    def enter(self):
        """
        Handle Enter (Return) being pressed in all circumstances.
        In INPUT mode, attempt to consume input and redirect to appropriate StringManipulator method.
        In MAIN mode, run transformations and refresh the display.
        """
        if self.mode == 'MAIN':
            self.sm.apply_modifications()
            self.text_buffer.refresh_text()

        elif self.mode == 'INPUT':
            allow_blank = (self.func not in ['CURRENT_DELIMITER', 'FIND', 'SMART'])
            force_type = int if self.func == 'INDENT' else None
            val = self.input.get_value_and_clear(allow_blank, force_type)

            if val != None:
                revert_focus = True
                if self.func == 'CURRENT_DELIMITER':
                    self.sm.set_current_delimiter(val)
                elif self.func == 'TARGET_DELIMITER':
                    self.sm.set_target_delimiter(val)
                elif self.func == 'PREFIX':
                    self.sm.set_prefix(val)
                elif self.func == 'SUFFIX':
                    self.sm.set_suffix(val)
                elif self.func == 'QUOTE':
                    self.sm.set_target_quote(val)
                elif self.func == 'INDENT':
                    self.sm.set_target_indent(val)
                elif self.func == 'SMART':
                    self.sm.set_smart_format(val)
                elif self.func == 'FIND':
                    self.find_buffer = val
                    revert_focus = False
                    self.change_mode('INPUT', 'REPLACE', 'Replace:')
                elif self.func == 'REPLACE':
                    self.replace_buffer = val
                    self.sm.queue_find_replace(self.find_buffer, self.replace_buffer)

                if revert_focus:
                    self.change_mode()
                    self.text_buffer.textbox.focus_set()

app = AppWindow()
app.main.mainloop()
