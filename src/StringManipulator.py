from tkinter import *
import sys

class INITIAL_STATE:
    current_delimiter = '\n' if sys.platform != 'win32' else '\r\n'
    target_delimiter = '\n' if sys.platform != 'win32' else '\r\n'
    current_quote = ''
    target_quote = ''
    prefix = ''
    suffix = ''
    indent = 0

class MODIFICATIONS:
    TARGET_QUOTE = 'target_quote'
    CASING = [
        'all_lowercase',
        'all_uppercase',
        'capitalize_first',
        'proper'
    ]
    STRIP_BLANKS = 'strip_blanks'
    TRIM_WHITESPACE = 'trim_whitespace'
    ALPHABETIZE = 'alphabetize'
    DEDUPLICATE = 'remove_duplicates'
    SMART_FORMAT = 'smart_format'

class UNICODE_CONTROL:
    NL = '↵'              # ⏎ ␊ ↵ ⮐
    CR = '↴'       # ␍


class StringManipulator:
#   [ str ] [ mods ] [ new str ]

    def __init__(self, text):
        self.initialize_session_variables()
        self.pending_modifications = {}
        self.elements = None
        self.element_count = IntVar(value=0)
        self.set_original_text(text)

        self.undo = []


    def set_original_text(self, text):
        if text != '' and text != None:
            self.original_text = text
        else:
            self.original_text = ''
        self.current_text = self.original_text
        self.calculate_elements()


    def initialize_session_variables(self):
        self.current_delimiter = StringVar(value=INITIAL_STATE.current_delimiter)
        self.current_delimiter_repr = StringVar(value=self.get_delimiter_repr(INITIAL_STATE.current_delimiter))
        self.target_delimiter = StringVar(value=INITIAL_STATE.target_delimiter)
        self.target_delimiter_repr = StringVar(value=self.get_delimiter_repr(INITIAL_STATE.target_delimiter))

        self.current_quote = StringVar(value=INITIAL_STATE.current_quote)
        self.target_quote = StringVar(value=INITIAL_STATE.target_quote)

        self.current_prefix = StringVar(value=INITIAL_STATE.prefix)
        self.target_prefix = StringVar(value=INITIAL_STATE.prefix)
        self.current_suffix = StringVar(value=INITIAL_STATE.suffix)
        self.target_suffix = StringVar(value=INITIAL_STATE.suffix)

        self.current_indent = IntVar(value=INITIAL_STATE.indent)
        self.target_indent = IntVar(value=INITIAL_STATE.indent)

        self.queue_str = StringVar(value='')


    def reinitialize_session_variables(self):
        self.current_delimiter.set(INITIAL_STATE.current_delimiter)
        self.current_delimiter_repr.set(self.get_delimiter_repr(INITIAL_STATE.current_delimiter))
        self.target_delimiter.set(INITIAL_STATE.target_delimiter)
        self.target_delimiter_repr.set(self.get_delimiter_repr(INITIAL_STATE.target_delimiter))

        self.current_quote.set(INITIAL_STATE.current_quote)
        self.target_quote.set(INITIAL_STATE.target_quote)
        self.current_prefix.set(INITIAL_STATE.prefix)
        self.target_prefix.set(INITIAL_STATE.prefix)
        self.current_suffix.set(INITIAL_STATE.suffix)
        self.target_suffix.set(INITIAL_STATE.suffix)

        self.current_indent.set(INITIAL_STATE.indent)
        self.target_indent.set(INITIAL_STATE.indent)

        self.queue_str.set('')


    def reset_state(self):
        self.original_text = self.original_text
        self.reinitialize_session_variables()

        self.calculate_elements()
        self.pending_modifications = {}
        self.queue_str.set(self.modification_queue(True))


    def update_state(self, reset=False):
        self.current_text = self.target_delimiter.get().join([
            (' ' * self.target_indent.get()) +
            self.target_quote.get() +
            self.target_prefix.get() + e + self.target_suffix.get()
            + self.target_quote.get()
            for e in self.elements
        ])

        if reset:
            if self.target_delimiter != '':
                self.set_current_delimiter(self.target_delimiter.get())
                self.set_current_quote(self.target_quote.get())
                self.set_current_prefix(self.target_prefix.get())
                self.set_current_suffix(self.target_suffix.get())
                self.current_indent.set(self.target_indent.get())

            self.pending_modifications = {}
            self.queue_str.set(self.modification_queue(True))

    def calculate_elements(self):
        self.elements = self.current_text.split(self.current_delimiter.get())
        self.element_count.set(len(self.elements))
        # print(f"Elements set - count: {self.element_count.get()}")
        # print(f"Elements\n: {self.elements}\n")
        # print(f"Current Delimiter: {self.current_delimiter_repr.get()}")
        # print(f"Target Delimiter: {self.target_delimiter_repr.get()}")

    @staticmethod
    def unescape_delimiter_string(string):
        if string == None: return ''
        return string.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')

    def set_current_delimiter(self, delimiter):
        delimiter = self.unescape_delimiter_string(delimiter)
        if self.current_delimiter.get() != delimiter:
            self.current_delimiter.set(delimiter)
            self.current_delimiter_repr.set(self.get_delimiter_repr(delimiter))
            self.calculate_elements()
        if self.current_delimiter.get() != self.target_delimiter:
            self.pending_modifications['change_delimiter'] = self.target_delimiter

    def set_target_delimiter(self, delimiter):
        delimiter = self.unescape_delimiter_string(delimiter)
        self.target_delimiter.set(delimiter)
        self.target_delimiter_repr.set(self.get_delimiter_repr(delimiter))
        self.pending_modifications['change_delimiter'] = delimiter
        self.queue_str.set(self.modification_queue(True))
        return True

    def set_current_quote(self, quote_char):
        if self.current_quote.get() != quote_char:
            self.current_quote.set(quote_char)
        self.queue_str.set(self.modification_queue(True))

    def set_target_quote(self, quote_char):
        if self.current_quote.get() != quote_char:
            self.target_quote.set(quote_char)
            self.pending_modifications[MODIFICATIONS.TARGET_QUOTE] = self.target_quote
        self.queue_str.set(self.modification_queue(True))

    def set_target_indent(self, indent):
        if indent == '':
            self.target_indent.set(INITIAL_STATE.indent)
            self.pending_modifications.pop('change_indent')
        else:
            if self.target_indent.get() != indent:
                self.target_indent.set(int(indent))
                self.pending_modifications['change_indent'] = self.target_indent
        self.queue_str.set(self.modification_queue(True))

    def set_current_prefix(self, prefix):
        if prefix == '':
            self.current_prefix.set(INITIAL_STATE.prefix)
        else:
            self.current_prefix.set(prefix)
        #self.queue_str.set(self.modification_queue(True))

    def set_prefix(self, prefix):
        if prefix == '':
            self.target_prefix.set(INITIAL_STATE.prefix)
        else:
            self.target_prefix.set(prefix)
        #self.queue_str.set(self.modification_queue(True))

    def set_current_suffix(self, suffix):
        if suffix == '':
            self.current_suffix.set(INITIAL_STATE.suffix)
        else:
            self.current_suffix.set(suffix)
        #self.queue_str.set(self.modification_queue(True))

    def set_suffix(self, suffix):
        if suffix == '':
            self.target_suffix.set(INITIAL_STATE.suffix)
        else:
            self.target_suffix.set(suffix)
        #self.queue_str.set(self.modification_queue(True))

    def get_delimiter_repr(self, delimiter):
        if delimiter == '':
            return 'None'
        
        tmp = delimiter.replace('\n', UNICODE_CONTROL.NL)
        tmp = tmp.replace('\r', UNICODE_CONTROL.CR)
        tmp = tmp.replace('\t', '\\t')
        tmp = tmp.replace(' ', '\\s')

        return tmp

    def get_capsules(self):
        """
            Return a classified list of elements and their encapsulating pieces,
            i.e. a capsule.
        """
        return [    
            [
                {
                    'type': 'indent',
                    'string': '·' * self.current_indent.get()
                },
                {
                    'type': 'prefix',
                    'string': self.current_prefix.get()
                },
                {
                    'type': 'quote',
                    'string': self.current_quote.get()
                },
                {
                    'type': 'element',
                    'string': e
                },
                {
                    'type': 'quote',
                    'string': self.current_quote.get()
                },
                {
                    'type': 'suffix',
                    'string': self.current_suffix.get()
                }
            ]
            for e in
            self.elements
        ]

    def queue_find_replace(self, f, r):
        if self.pending_modifications.get('find_replace', None) == None:
            self.pending_modifications['find_replace'] = {}
        self.pending_modifications['find_replace'][f] = r.replace('\\n', '\n')
        self.queue_str.set(self.modification_queue(True))

    def toggle_boolean_modification(self, value):
        if self.pending_modifications.get(value, None) in (None, False):
            self.pending_modifications[value] = True
        elif self.pending_modifications.get(value, None) == True:
            self.pending_modifications[value] = False
        self.queue_str.set(self.modification_queue(True))

    def set_smart_format(self, format_string):
        # TODO: Validate
        self.pending_modifications[MODIFICATIONS.SMART_FORMAT] = format_string
        self.queue_str.set(self.modification_queue(True))

    def set_casing_modification(self, value):
        if self.pending_modifications.get('casing', None) == value:
            self.pending_modifications.pop('casing')
        else:
            self.pending_modifications['casing'] = value
        self.queue_str.set(self.modification_queue(True))

    def advance_casing_setting(self):
        if self.pending_modifications.get('casing', None) == None:
            self.pending_modifications['casing'] = MODIFICATIONS.CASING[0]
        else:
            current = MODIFICATIONS.CASING.index(self.pending_modifications['casing'])
            if current >= len(MODIFICATIONS.CASING) - 1:
                self.pending_modifications.pop('casing')
            else:
                self.pending_modifications['casing'] = MODIFICATIONS.CASING[current + 1]
        self.queue_str.set(self.modification_queue(True))

    def apply_modifications(self, reset=True):
        if self.pending_modifications.get(MODIFICATIONS.TRIM_WHITESPACE, False) == True:
            self.elements = [e.strip() for e in self.elements]

        if self.pending_modifications.get(MODIFICATIONS.STRIP_BLANKS, False) == True:
            self.elements = [e for e in self.elements if e != '']

        if self.pending_modifications.get('find_replace', None) != None:
            fr = self.pending_modifications['find_replace']
            for k in fr:
                self.elements = [e.replace(k, fr[k]) for e in self.elements]

        smart_format_string = self.pending_modifications.get(MODIFICATIONS.SMART_FORMAT, False)
        if smart_format_string != False:
            # TODO: Replace 
            self.elements = [smart_format_string.replace('\$', 'DO_LL_ARPL_ACE_HOL_DER').replace('$$', e).replace('DO_LL_ARPL_ACE_HOL_DER', '$') for e in self.elements]

        if self.pending_modifications.get(MODIFICATIONS.DEDUPLICATE, False) == True:
            tmp = []
            for e in self.elements:
                if e not in tmp: tmp.append(e)
            self.elements = tmp

        casing = self.pending_modifications.get('casing', None)
        if casing == 'all_lowercase': self.elements = [e.lower() for e in self.elements]
        if casing == 'all_uppercase': self.elements = [e.upper() for e in self.elements]
        if casing == 'capitalize_first': self.elements = [str(e)[0].upper() + str(e)[1:] if len(e) > 0 else e for e in self.elements]
        if casing == 'proper': self.elements = [e.capitalize() for e in self.elements]

        if self.pending_modifications.get(MODIFICATIONS.ALPHABETIZE, False) == True:
            tmp = sorted(self.elements)
            self.elements = tmp

        self.update_state(reset)

    def modification_queue(self, get_str=False):
        tmp = []
        if self.pending_modifications.get('change_delimiter', None) != None:
            tmp.append(
                'Change Delimiter: ('
               f'{self.get_delimiter_repr(self.current_delimiter.get())}'
               f' -> {self.get_delimiter_repr(self.target_delimiter.get())})'
            )

        if self.pending_modifications.get(MODIFICATIONS.STRIP_BLANKS, False) == True:
            tmp.append(f'Remove blank elements')

        if self.pending_modifications.get(MODIFICATIONS.TRIM_WHITESPACE, False) == True:
            tmp.append(f'Trim whitespace from elements')

        if self.pending_modifications.get('find_replace', None) != None:
            for k in self.pending_modifications['find_replace']:
                tmp.append(f'Find/Replace: "{k}" -> "{self.pending_modifications["find_replace"][k]}"')

        smart_format_string = self.pending_modifications.get(MODIFICATIONS.SMART_FORMAT, False)
        if smart_format_string != False:
            tmp.append(f'Format elements into "{smart_format_string}"')

        if self.pending_modifications.get(MODIFICATIONS.DEDUPLICATE, False) == True:
            tmp.append(f'Remove duplicate elements')

        casing = self.pending_modifications.get('casing', None)
        if casing == 'all_lowercase': tmp.append(f'Lower case')
        if casing == 'all_uppercase': tmp.append(f'Upper case')
        if casing == 'capitalize_first': tmp.append(f'Capitalize first letter')
        if casing == 'proper': tmp.append(f'Proper case')

        if self.pending_modifications.get(MODIFICATIONS.TARGET_QUOTE, None) != None:
            tmp.append(f'Quote each element with {self.target_quote.get()}')

        if self.pending_modifications.get(MODIFICATIONS.ALPHABETIZE, False) == True:
            tmp.append(f'Sort alphabetically')

        if self.pending_modifications.get('change_indent', None) != None:
            tmp.append(f'Indent each line by {str(self.target_indent.get())}')

        if len(tmp) == 0: return ' '
        if get_str:
            return '\n'.join(tmp)
        return tmp
