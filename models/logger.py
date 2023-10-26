from os import name

STYLE = {
    'None': '0',
    'bold': '1'
}

FG = {
    'None': '',
    'gray': ';30',
    'red': ';31',
    'green': ';32',
    'yellow': ';33',
    'blue': ';34',
    'purple': ';35',
    'cyan': ';36',
}

class Log:
    """ quick log class for CLI output """
    def __init__(self, **kwargs):
        """ Init the logger """
        self.level = 'debug' if kwargs.get('debug') else 'info'

    def indication(self, msg):
        """ Log indication message """
        print(' '.join([self.highlight('[#]', 'bold', 'blue'), msg]))

    def info(self, msg):
        """ Log info message """
        print(' '.join([self.highlight('[*]', 'bold', 'blue'), msg]))

    def success(self, msg):
        print(' '.join([self.highlight('[+]', 'bold', 'green'), msg]))

    def debug(self, msg):
        if self.level == 'debug':
            print(' '.join([self.highlight('[-]', 'bold', 'None'), msg]))

    def warn(self, msg):
        print(' '.join([self.highlight('[*]', 'bold', 'yellow'), msg]))

    def error(self, msg):
        print(' '.join([self.highlight('[!]', 'bold', 'red'), msg]))

    def code_gen(self, data, style, color, windows=False):
        """ Generate the code for the given data """
        return data if windows else '\033[0{}{}m{}\033[0m'.format(STYLE[style], FG[color], data)

    def highlight(self, data, style='bold', fg='blue'):
        """ Highlight the data with the given style and color """
        return self.code_gen(data, style, fg, windows=True if name == 'nt' else False)