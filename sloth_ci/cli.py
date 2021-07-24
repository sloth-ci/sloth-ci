from importlib import import_module

from argparse import ArgumentParser

from yaml import load, FullLoader

from cliar import Cliar
from cliar import ignore as ignore_method

from .bed import Bed

from . import __version__


class CLI(Cliar):
    '''Welcome to Sloth CI CLI!

Run "sci start" to start the server.'''

    def __new__(cls):
        '''Apply extenions before creating a CLI instance.

        The built-in API extension is always applied before any custom ones.
        '''

        api_extension = {
            'api': {
                'module': 'api'
            }
        }

        PreExtendedCLI, pre_errors = cls.extend(api_extension)

        parser = ArgumentParser(add_help=False)
        parser.add_argument('-config', default='./sloth.yml')
        config = parser.parse_known_args()[0].config

        try:
            cls.config = load(open(config), Loader=FullLoader)

        except FileNotFoundError:
            print('Please run inside a dir with "sloth.yml" or specify the server config with "-c."')
            exit()

        except Exception as e:
            print('Failed to parse the config file: %s' % e)
            exit()

        ExtendedCLI, errors = PreExtendedCLI.extend(cls.config.get('extensions'))

        for error in pre_errors + errors:
            print(error)

        return super().__new__(ExtendedCLI)

    @classmethod
    @ignore_method
    def extend(cls, extensions):
        '''Sequentially chain-inherit CLI classes from extensions.

        The first extension's CLI class inherits from the base CLI class and becomes the base class, then the second one inherits from it, and so on.

        :param extensions: list of extensions to load.

        :returns: `ExtendedCLI` is a CLI class inherited from all extensions' CLI classes; `errors` is the list of errors raised during extension loading.
        '''

        ExtendedCLI = cls
        errors = []

        if extensions:
            for extension_name, extension_config in extensions.items():
                try:
                    ext = import_module('sloth_ci_ext_%s' % extension_config['module'])

                    ExtendedCLI = ext.extend_cli(ExtendedCLI, {
                            'name': extension_name,
                            'config': extension_config
                        }
                    )

                except AttributeError as e:
                    pass

                except Exception as e:
                    errors.append('Could not load extension %s: %s' % (extension_name, e))

        return ExtendedCLI, errors

    def _root(self, config='./sloth.yml', version=False):
        if version:
            print(__version__)
        else:
            return NotImplemented

    def start(self):
        '''start server'''

        try:
            print(
                'Starting Sloth CI on http://%s:%d'
                % (self.config['host'], self.config['port'])
            )

            Bed(self.config).start()

        except Exception as e:
            print('Failed to start Sloth CI: %s' % e)

def main():
    CLI().parse()

