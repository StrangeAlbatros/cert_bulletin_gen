#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

from .bulletin import Bulletin

__version__ = "1.0.1"

def get_args():
    """ Get the arguments """
    parser = ArgumentParser(
        prog="Cert Bulletin Generator",
        description='Generate a bulletin of vulnerabilities from cert',
        epilog="An application wich generate a bulletin of vulnerabilities from cert"
    )
    parser.add_argument(
        '-c', '--config', dest='config',
        help='config file'
    )
    parser.add_argument(
        '--no-compil',action='store_true',
        help='no latex compilation, only latex file generation'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true', dest='debug',
        help='Increase output verbosity'
    )
    parser.add_argument(
        '--pdf-name', dest='pdf_name', type=str,
        help='name of the pdf file'
    )
    # parser.add_argument(
    #     '-o', '--output', dest='output',
    #     help='output file'
    # )
    # parser.add_argument(
    #     'begin_date', metavar='begin_date', type=str,
    #     help='begin date'
    # )
    # parser.add_argument(
    #     'end_date', metavar='end_date', type=str,
    #     help='end date'
    # )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__)
    )
    return parser.parse_args()

if __name__ == "__main__":
    Bulletin(get_args())