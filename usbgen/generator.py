import argparse
import os

import jinja2

from usbgen import usb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input jinja template")
    parser.add_argument("-o", "--output", help="output file")
    args = parser.parse_args()

    path, filename = os.path.split(args.input)
    template =  jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './'),
        keep_trailing_newline=True,
    ).get_template(filename)

    template.globals['usb'] = usb

    output = template.render()

    if args.output is not None:
        outputf = open(args.output, "w")
        outputf.write(output)
        outputf.close()
    else:
        print(output)
