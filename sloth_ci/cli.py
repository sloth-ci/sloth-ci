from argparse import ArgumentParser

from yaml import load

from .bed import Bed

def main():
    '''Main CLI function.'''

    parser = ArgumentParser()
    parser.add_argument('-c', '--config', help='Server config.', default='sloth.yml')

    parsed_args = parser.parse_args()

    path_to_config_file = parsed_args.config

    try:
        Bed(load(open(path_to_config_file))).start()
    
    except FileNotFoundError:
        print('Either put a sloth.yml file in this directory or specify the path with -c.')

    except Exception as e:
        print('Invalid config file.')