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


class DeviceHolder():
    def __init__(self) -> None:
        self.devices: Dict[str, ioctl.hidraw.Hidraw] = {}

    def iterate_devices(self) -> Iterator[str]:
        for fname in os.listdir('/dev/'):
            if fname.startswith('hidraw'):
                yield fname

    def add_device(self, path: str) -> None:
        if os.path.exists(path):
            try:
                self.devices[path] = ioctl.hidraw.Hidraw(path)
            except IOError as e:
                print(f"can't open '{path}': {str(e)}", file=sys.stderr)

    def filter_devices(self, hid_info: str) -> None:
        bus_pattern = parse.compile('{bus:d}:{vid:x}:{pid:x}')
        sep_pattern = parse.compile(':{vid:x}:{pid:x}')
        dev_pattern = parse.compile('{vid:x}:{pid:x}')

        for key, hidraw in self.devices.copy().items():
            bus, vid, pid = hidraw.info
            for pattern in [bus_pattern, sep_pattern, dev_pattern]:
                keys = pattern.parse(hid_info)
                if keys:
                    if (
                        'bus' in keys and bus != keys['bus'] or
                        vid != keys['vid'] or
                        pid != keys['pid']
                    ):
                        del self.devices[key]
                    break

    def print_devices(self, verbose: bool = False) -> None:
        first = True
        for key, hidraw in self.devices.items():
            bus, vid, pid = hidraw.info
            if verbose and not first:
                first = False
                print()
            print(f'Device {key}: ID {vid:04x}:{pid:04x} {hidraw.name}')
            if verbose:
                print('Report Descriptor:')
                print(hidraw.report_descriptor)


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

    main = DeviceHolder()

    if args.devnum is not None:
        main.add_device(f'/dev/hidraw{args.devnum}')
    elif args.file is not None:
        main.add_device(args.file)
    else:
        for device in main.get_devices():
            main.add_device(f'/dev/{device}')

        if args.hid_info:
            main.filter_devices(args.hid_info)

    if not main.devices:
        exit(1)

    main.print_devices(args.verbose)


def entrypoint() -> None:
    main(sys.argv[1:])


if __name__ == '__main__':
    main(sys.argv[1:], 'python -m lshid')
