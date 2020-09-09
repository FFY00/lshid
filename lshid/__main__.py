#!/bin/env python
#
# SPDX-License-Identifier: MIT

import argparse
import os
import sys

from typing import Dict, Iterator, List, Optional

import ioctl.hidraw
import parse

import lshid


devices: Dict[str, ioctl.hidraw.Hidraw] = {}


def _get_devices() -> Iterator[str]:
    for fname in os.listdir('/dev/'):
        if fname.startswith('hidraw'):
            yield fname


def _add_device(path: str) -> None:
    if os.path.exists(path):
        try:
            devices[path] = ioctl.hidraw.Hidraw(path)
        except IOError as e:
            print(f"can't open '{path}': {str(e)}", file=sys.stderr)


def _filter_devices(hid_info: str) -> None:
    bus_pattern = parse.compile('{bus:d}:{vid:x}:{pid:x}')
    sep_pattern = parse.compile(':{vid:x}:{pid:x}')
    dev_pattern = parse.compile('{vid:x}:{pid:x}')

    for key, hidraw in devices.copy().items():
        bus, vid, pid = hidraw.info
        for pattern in [bus_pattern, sep_pattern, dev_pattern]:
            keys = pattern.parse(hid_info)
            if keys:
                if (
                    'bus' in keys and bus != keys['bus'] or
                    vid != keys['vid'] or
                    pid != keys['pid']
                ):
                    del devices[key]
                break


def _print_devices(verbose: bool = False) -> None:
    first = True
    for key, hidraw in devices.items():
        bus, vid, pid = hidraw.info
        if verbose and not first:
            print()
        print(f'Device {key}: ID {vid:04x}:{pid:04x} {hidraw.name}')
        if verbose:
            print('Report Descriptor:')
            print(hidraw.report_descriptor)
        first = False


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


def main(cli_args: List[str], prog: Optional[str] = None) -> None:
    parser = main_parser()
    if prog:
        parser.prog = prog
    args = parser.parse_args(cli_args)

    if args.version:
        print(f'lshid {lshid.__version__}')
        return

    if args.devnum is not None:
        _add_device(f'/dev/hidraw{args.devnum}')
    elif args.file is not None:
        _add_device(args.file)
    else:
        for device in _get_devices():
            _add_device(f'/dev/{device}')

        if args.hid_info:
            _filter_devices(args.hid_info)

    if not devices:
        exit(1)

    _print_devices(args.verbose)


def entrypoint() -> None:
    main(sys.argv[1:])


if __name__ == '__main__':
    main(sys.argv[1:], 'python -m lshid')
