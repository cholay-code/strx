import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import Font

class InputFrame(Frame):
    active: False

    def __init__(self, config):
        """
        Housies current mode indicator and input
        """
        tk.Frame.__init__(
            self,
            bg=config.COLORS['light_window_bg'],
            padx=5,
            pady=5
        )

        frame = tk.Frame(
            self,
            background='#625D5D',
            padx=2,
            pady=2,
            bd=1,
            relief=SUNKEN
        )

        input_config = config.CONFIG['Input']
        label_config = config.CONFIG['InputGuide']
        self.label_text = StringVar('')

        self.input_label = Label(
            frame,
            textvariable=self.label_text,
            bg=label_config['bg'],
            fg=label_config['fg'],
            borderwidth=input_config['bw'],
            relief=input_config['relief'],
            padx=label_config['padx'],
            pady=label_config['pady'],
            height=label_config['h'],
            width=label_config['w']*2,
            font=Font(family=label_config['font'][0], size=label_config['font'][1])
        )
        self.input_label.grid(row=0, column=0, columnspan=1, sticky='news')
        frame.grid(row=0, column=0, columnspan=1, sticky='news')


        frame = tk.Frame(
            self,
            background='#625D5D',
            padx=2,
            pady=2,
            bd=1,
            relief=SUNKEN
        )
        self.input_text_box = Text(
            frame,
            bg=input_config['bg'],
            fg=input_config['fg'],
            height=input_config['h'],
            width=input_config['w'],
            font=Font(family=input_config['font'][0], size=input_config['font'][1]),
            padx=input_config['padx'],
            pady=input_config['pady'],
            borderwidth=input_config['bw'],
            relief=input_config['relief'],
            state=NORMAL,
            wrap=WORD,
            cursor='arrow',
            highlightthickness=1,
            highlightcolor=input_config['highlight_bg']
        )
        self.input_text_box.grid(row=0, column=1, columnspan=4, sticky='news')
        frame.grid(row=0, column=1, columnspan=4, sticky='news')
        self.input_text_box.state='disabled'


    def activate(self, action='', prefill=''):
        self.label_text.set(action)
        self.input_text_box.focus_set()
        self.input_text_box.state='normal'
        self.input_text_box.insert(END, prefill)


    def deactivate(self):
        self.label_text.set('')
        self.input_text_box.state='disabled'


    def get_value_and_clear(self, allow_blank=True, force_type=None):
        s = self.input_text_box.get('1.0', END).strip('\n')
        if s == '' and not allow_blank: return None
        if force_type is not None:
            try:
                force_type(s)
            except:
                self.input_text_box.delete('1.0', END)
                if force_type == int and s == '':
                    return 0
                else:
                    return None

        self.input_text_box.delete('1.0', END)
        self.deactivate()

        # print(f'InputFrame.get_value_and_clear - {s}')
        return s
