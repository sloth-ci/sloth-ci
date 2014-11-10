from argparse import ArgumentParser

from yaml import load

from .bed import Bed

def main():
    '''Main CLI function.'''

    parser = ArgumentParser()
    parser.add_argument('-s', '--sconfig', help='Server config.', default='sloth.yml')

    parsed_args = parser.parse_args()

    sconfig_file = parsed_args.sconfig

    sconfig = load(open(sconfig_file))

    Bed(sconfig).start()