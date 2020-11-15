# SPDX-License-Identifier: MIT

import os

from typing import Dict, Iterator

import hid_parser
import ioctl.hidraw


__version__ = '0.2.2'


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
                raise RuntimeError(f"can't open '{path}': {str(e)}") from None

    def filter_devices(self, hid_info: str) -> None:
        try:
            import parse
        except ImportError:
            raise RuntimeError("can't filter devices: missing 'parse' dependency") from None

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
                print()
            print(f'Device {key}: ID {vid:04x}:{pid:04x} {hidraw.name}')
            if verbose:
                print('Report Descriptor:')
                hid_parser.ReportDescriptor(hidraw.report_descriptor).print(level=1)
            first = False
