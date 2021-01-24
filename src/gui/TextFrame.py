import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

class TextFrame(Frame):
    settings = {
        'newline_delim_mode': False,
        'apply_formatting': True
    }

    def __init__(self, config, sm):
        """
        The main text buffer GUI. Displays elements within text
        string and highlights ephermeral modifications
        """
        self.config = config
        self.sm = sm

        tk.Frame.__init__(
            self,
            bg=self.config.CONFIG['Window']['bg'],
            bd=5
        )
        
        self.create_textbox(self.config.CONFIG['Text']).grid(
            row=0, column=1
        )


        self.create_queue_box(self.config.CONFIG['Queue']).grid(
            row=0, column=0, sticky='news'
        )

        self.refresh_text()


    def create_textbox(self, config):
        """
        Create the main textbox element to display the current state.
        """

        frame = tk.Frame(
            self,
            background='#625D5D',
            padx=3,
            pady=2,
            bd=1,
            relief=SUNKEN
        )

        self.textbox = Text(
            frame,
            bg=config['bg'],
            fg=config['fg'],
            height=config['h'],
            width=config['w'],
            font=Font(
                family=config['font'][0],
                size=config['font'][1]
            ),
            padx=config['padx'],
            pady=config['pady'],
            spacing1=0,
            spacing2=0,
            state=NORMAL,
            wrap=WORD,
            cursor='arrow',
            relief=config['relief'],
            borderwidth=config['bw']
        )
        
        self.create_textbox_tags()

        self.scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=self.textbox.yview)
        self.scrollbar.grid(row=0, column=2, sticky=(N,S))
        self.textbox['yscrollcommand'] = self.scrollbar.set

        self.textbox.grid(row=0, column=0, columnspan=1, sticky='news')
        return frame



    def create_textbox_tags(self):
        """
        Create the styles for tagged content in textbox.
        """
        for style in ['element', 'quote', 'delimiter', 'prefix', 'suffix', 'indent']:
            self.textbox.tag_config(
                style,
                foreground=self.config.COLORS.get('dark_' + style + '_fg', None),
                background=self.config.COLORS.get('dark_' + style + '_bg', None)
            )


    def create_queue_box(self, config):        
        frame = tk.Frame(
            self,
            background='#625D5D',
            padx=2,
            pady=2,
            bd=1,
            relief=SUNKEN
        )

        self.queue = Label(
            frame,
            bg=config['bg'],
            fg=config['fg'],
            height=config['h'],
            width=config['w'],
            textvariable=self.sm.queue_str,
            font=Font(family=config['font'][0], size=config['font'][1]),
            state=NORMAL,
            relief=config['relief'],
            padx=config['padx'],
            pady=config['pady'],
            borderwidth=config['bw']
        )

        self.queue.grid(row=0, column=0, sticky='news')
        return frame

    def refresh_text(self):
        """
        Refresh the text box with a styled string of characters for output.
        """
        # print('TextFrame.py - refresh_text()')
        self.textbox['state'] = 'normal'
        self.textbox.delete('1.0', END)
        parts = self.sm.get_capsules()
        line, char = (1, 0)
        for i in range(0, len(parts)):
            for e in parts[i]:
                self.textbox.insert(END, e['string'])
                if self.settings['apply_formatting']:
                    start, end, line, char = self.advance_index(line, char, e['string'], e['type'])
                    self.textbox.tag_add(e['type'], start, end)

            if i != len(parts) - 1:
                d = self.sm.current_delimiter.get()
                if '\n' in d or '\r' in d:
                    d = self.sm.get_delimiter_repr(self.sm.current_delimiter.get()) + self.sm.current_delimiter.get()
                self.textbox.insert(END, d)
                if self.settings['apply_formatting']:
                    start, end, line, char = self.advance_index(line, char, d, 'delimiter')
                    self.textbox.tag_add('delimiter', start, end)

        self.textbox['state'] = 'disabled'

    @staticmethod
    def advance_index(line, char, s, t) -> (str, str, int, int):
        """
        Advance the line & char counter to help apply tags as text rendered.
        """
        start = f'{line}.{char}'
        newlines = s.count('\n')

        if newlines == 0:
            char += len(s)
        else:
            line += s.count('\n')
            lines = s.split('\n')
            char = len(lines[len(lines)-1])

        end = f'{line}.{char}'

        # print(f's: {s}, start: {start}, end: {end}, line: {line}, char: {char}')
        return start, end, line, char