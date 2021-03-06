#!/bin/env python
#
# SPDX-License-Identifier: MIT

import argparse
import sys
import traceback
import warnings

from typing import List, Optional

import hid_parser

import lshid


def main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='List HID devices')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='increase verbosity (show descriptors)'
    )
    parser.add_argument(
        '-s', metavar='devnum',
        type=int, dest='devnum',
        help='show only devices with specified device and/or bus numbers (in decimal)'
    )
    parser.add_argument(
        '-d', metavar='[[bus]:][vendor]:[product]',
        type=str, dest='hid_info',
        help='show only devices with the specified bus, vendor and product ID numbers (in hexadecimal)'
    )
    parser.add_argument(
        '-D', metavar='/dev/hidrawX',
        type=str, dest='file',
        help='selects which device node lshid will examine'
    )
    # TODO: tree
    parser.add_argument(
        '-V', '--version',
        action='store_true',
        help='show version of program'
    )
    return parser


def lshid_cmd(cli_args: List[str], prog: Optional[str] = None) -> None:
    parser = main_parser()
    if prog:
        parser.prog = prog
    args = parser.parse_args(cli_args)

    if args.version:
        print(f'lshid {lshid.__version__}')
        return

    main = lshid.DeviceHolder()

    if args.devnum is not None:
        main.add_device(f'/dev/hidraw{args.devnum}')
    elif args.file is not None:
        main.add_device(args.file)
    else:
        for device in main.iterate_devices():
            try:
                main.add_device(f'/dev/{device}')
            except RuntimeError as e:
                print(str(e), file=sys.stderr)

        if args.hid_info:
            main.filter_devices(args.hid_info)

    if not main.devices:
        exit(1)

    main.print_devices(args.verbose)


def main(cli_args: List[str], prog: Optional[str] = None) -> None:
    warnings.filterwarnings('ignore', category=hid_parser.HIDComplianceWarning)

    try:
        lshid_cmd(cli_args, prog)
    except Exception as e:
        print(f'\n{traceback.format_exc()}\nERROR ' + str(e).strip('\'" '), file=sys.stderr)
        exit(1)


def entrypoint() -> None:
    main(sys.argv[1:])


if __name__ == '__main__':
    main(sys.argv[1:], 'python -m lshid')
