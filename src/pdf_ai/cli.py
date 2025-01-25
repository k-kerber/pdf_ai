import argparse
from pathlib import Path
from pdf_ai import PDFAI
from pprint import pprint
from pymupdf import get_pdf_str
from json import dumps
from json import loads


# argument parser
parser = argparse.ArgumentParser(prog="pdf_metadata", description="This program makes it easy to work with PDF file metadata")
# 'input' argument
parser.add_argument(dest="input_path", metavar="INPUT_PATH", help="usage: pdf_metadata path", type=str, nargs=1)
# command parser
commands = parser.add_subparsers(dest="command", title="commands", help="usage: [show | dump | import | update | suggest]")
# show command
show_command = commands.add_parser('show', help="usage: show [key]")
# show 'key' argument
show_command.add_argument(dest='show_key', required=False, type=str, nargs=1, metavar="SHOW_KEY", help="shows the value of the supplied key if it exists")
# import command
import_command = commands.add_parser('import', fromfile_prefix_chars='@', help="usage: import [@file.json | 'json'")
# import 'path' argument
import_command.add_argument(dest="import_json", metavar="IMPORT_JSON", type=str, nargs=1, help= 'a @file.json or a json string')
# dump command
dump_command = commands.add_parser("dump", help="usage: dump file.json")
# dump 'path' argument
dump_command.add_argument(dest='dump_path', type=str, nargs=1, metavar="DUMP_PATH", help="the path to the dump file")
# update command
update_command = commands.add_parser('update', help="usage: update key value")
# update 'path' argument
update_command.add_argument(dest="update_key_value", type=str, nargs=2, metavar="KEY_VALUE", help="updates metadata with key and value")


# format output
def __output(value, path=None):
    if path is not None:
        path = Path(path).open("w", encoding='utf8')
    pprint(dumps(value), indent=4, stream=path)


# return PDFToAI
def __pdf():
    return PDFAI(args.input_path)


# default function for show and dump
def __show():
    __output(__pdf().get_metadata(key=args.show_key), path=args.dump_path)


show_command.set_defaults(func=__show)


dump_command.set_defaults(func=__show)


def update():
    pdf = __pdf()
    update = None
    if args.import_json is not None:
        update = loads(args.import_json)
    elif args.update_key_value is not None:
        update = {get_pdf_str(args.update_key_value[0]): get_pdf_str(args.update_key_value[1])}
    if type(update) is not dict:
        update = dict(update)
    pdf.set_metadata(update)


import_command.set_defaults(func=__update)


update_command.set_defaults(func=__update)


args = parser.parse_args()
