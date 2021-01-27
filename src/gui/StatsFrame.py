import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

FIELD_SIZES = {
    'xs': 4,
    's': 8,
    'm': 10,
    'l': 18
}

class StatsFrame(Frame):
    settings = {
        'newline_delim_mode': False, # not used
        'apply_formatting': True
    }
    def __init__(self, config, sm):
        """
        Display current configuration.
        """
        self.config = config
        self.sm = sm

        tk.Frame.__init__(
            self,
            bg=self.config.CONFIG['Window']['bg'],
            bd=5
        )

        self.label_config = self.config.CONFIG['Label']
        self.readout_config = self.config.CONFIG['Readout']

        self.create_element_count_frame().grid(
            row=0, column=0, rowspan=3, columnspan=1,
            sticky=''
        )

        self.create_settings_frame().grid(
            row=0, column=1, rowspan=3, columnspan=1,
            sticky='news'
        )

        self.create_help_frame().grid(
            row=0, column=2, rowspan=3, columnspan=1,
            sticky='news'
        )


    def create_element_count_frame(self):
        """
        Create the top left panel showing a current count of
        elements split by delimiter
        """
        frame = tk.Frame(
            self,
            background='#625D5D',
            height=100,
            width=100,
            padx=5,
            pady=5,
            bd=2,
            relief=GROOVE
        )

        label = self.header_label(frame, "Elements", FIELD_SIZES['s'], 1, bg=3)
        readout = self.readout_label(frame, self.sm.element_count, FIELD_SIZES['s'], 2)
        label.grid(row=0, column=0, columnspan=1, rowspan=1, sticky='s')
        readout.grid(row=1, column=0, columnspan=1, rowspan=2, sticky='n')

        return frame


    def create_settings_frame(self):
        """
        Create the central settings readout panel showing
        current configuration.
        """
        frame = tk.Frame(
            self,
            bg='#625D5D',
            height=72,
            width=800,
            padx=5,
            pady=5,
            bd=2,
            relief=GROOVE
        )

        label_modifiers = self.header_label(frame, "Modifiers", FIELD_SIZES['m'], 1, bg=3, anchor=tk.E)
        label_target = self.header_label(frame, "target", FIELD_SIZES['m'], 1, bg=2, anchor=tk.E)
        label_current = self.header_label(frame, "current", FIELD_SIZES['m'], 1, bg=2, anchor=tk.E)

        label_modifiers.grid(row=0, column=1, sticky='news')
        label_current.grid(row=1, column=1, sticky='news')
        label_target.grid(row=2, column=1, sticky='news')

        label_quote = self.header_label(frame, "Quote", FIELD_SIZES['m'], 1, bg=1)
        quote_current = self.readout_label(frame, self.sm.current_quote, FIELD_SIZES['m'], 1)
        quote_target = self.readout_label(frame, self.sm.target_quote, FIELD_SIZES['m'], 1)

        label_quote.grid(row=0, column=2, sticky='sw')
        quote_current.grid(row=1, column=2, sticky='w')
        quote_target.grid(row=2, column=2, sticky='nw')

        label_delimiter = self.header_label(frame, "Delimiter", FIELD_SIZES['m'], 1, bg=1)
        delimiter_current = self.readout_label(frame, self.sm.current_delimiter_repr, FIELD_SIZES['m'], 1)
        delimiter_target = self.readout_label(frame, self.sm.target_delimiter_repr, FIELD_SIZES['m'], 1)

        label_delimiter.grid(row=0, column=3, sticky='sw')
        delimiter_current.grid(row=1, column=3, sticky='w')
        delimiter_target.grid(row=2, column=3, sticky='nw')

        label_indent = self.header_label(frame, "Indent", FIELD_SIZES['s'], 1, bg=1)
        indent_current = self.readout_label(frame, self.sm.current_indent, FIELD_SIZES['s'], 1)
        indent_target = self.readout_label(frame, self.sm.target_indent, FIELD_SIZES['s'], 1)

        label_indent.grid(row=0, column=4, sticky='sw')
        indent_current.grid(row=1, column=4, sticky='w')
        indent_target.grid(row=2, column=4, sticky='nw')

        label_prefix = self.header_label(frame, "Prefix", FIELD_SIZES['l'], 1, bg=1)
        prefix_current = self.readout_label(frame, self.sm.current_prefix, FIELD_SIZES['l'], 1)
        prefix_target = self.readout_label(frame, self.sm.target_prefix, FIELD_SIZES['l'], 1)

        label_prefix.grid(row=0, column=5, sticky='sw')
        prefix_current.grid(row=1, column=5, sticky='w')
        prefix_target.grid(row=2, column=5, sticky='nw')

        label_suffix = self.header_label(frame, "Suffix", FIELD_SIZES['l'], 1, bg=1)
        suffix_current = self.readout_label(frame, self.sm.current_suffix, FIELD_SIZES['l'], 1)
        suffix_target = self.readout_label(frame, self.sm.target_suffix, FIELD_SIZES['l'], 1)

        label_suffix.grid(row=0, column=6, sticky='sw')
        suffix_current.grid(row=1, column=6, sticky='w')
        suffix_target.grid(row=2, column=6, sticky='nw')

        return frame

    def create_help_frame(self):
        """
        Create a frame to contain the help button.
        """
        frame = tk.Frame(
            self,
            bg='#625D5D',
            height=72,
            width=45,
            padx=5,
            pady=5,
            bd=2,
            relief=GROOVE
        )

        return frame

    # TODO: Kwargs for value overwrite
    def header_label(self, frame, text, width=10, height_multiplier=1, bg=1, anchor=None) -> Label:
        anchor = tk.CENTER if anchor == None else anchor
        return Label(
            frame,
            anchor=anchor,
            text=text,
            bg=self.label_config['bg' + str(bg)],
            fg=self.label_config['fg'],
            borderwidth=self.label_config['bw'],
            relief=self.label_config['relief'],
            padx=self.label_config['padx'],
            pady=self.label_config['pady'] * height_multiplier,
            height=self.label_config['h'] * height_multiplier,
            width=width,
            font=Font(family=self.label_config['fontface'], size=self.label_config['fontsize'])
        )

    # TODO: Kwargs for value overwrite
    def readout_label(self, frame, textvar, width=10, height_multiplier=1, anchor=None) -> Label:
        anchor = tk.CENTER if anchor == None else anchor
        extra_padding = (height_multiplier - 1) * 3
        return Label(
            frame,
            anchor=anchor,
            textvariable=textvar,
            bg=self.readout_config['bg'],
            fg=self.readout_config['fg'],
            borderwidth=self.readout_config['bw'],
            padx=self.readout_config['padx'],
            pady=self.readout_config['pady'] + extra_padding,
            relief=self.readout_config['relief'],
            height=self.readout_config['h'] * height_multiplier,
            width=width,
            font=Font(family=self.readout_config['fontface'], size=self.readout_config['fontsize'])
        )
