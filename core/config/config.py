import configparser
import ast
import sys


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('core/config/config.ini')


    def get(self, section, value, return_type='string'):
        try:
            match return_type:
                case 'string':
                    return self.config[section][value]
                case 'int':
                    return int(self.config[section][value])
                case 'float':
                    return float(self.config[section][value])
                case 'bool':
                    return bool(self.config[section][value])
                case 'tuple':
                    return ast.literal_eval(self.config[section][value])
        except KeyError as e:
            print(f'Missing configuration key: {e}')
            sys.exit(1)