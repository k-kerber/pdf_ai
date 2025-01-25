import argparse
from collections import Counter
from humanfriendly import prompts
from pathlib import Path
from pdf_ai.src.pdf_ai.pdf_ai import PDFAI
from pprint import pprint
import pymupdf4llm
from json import dumps

# argument parameter templates
path_arg = {
    "type": str,
    "nargs": 1,
}

# argument parser
parser = argparse.ArgumentParser(prog="pdf_metadata", description="This program makes it easy to work with PDF file metadata")
# 'input' argument
parser.add_argument(dest="input_file", metavar="INPUT_FILE", help="usage: pdf_metadata 'path'", **path_arg)
# command parser
commands = parser.add_subparsers(dest="command", title="commands", help="usage: [show | dump | import | edit | suggest]")
# show command
show_metadata = commands.add_parser('show', help="usage: show ['key']")
# show 'key' argument
show_metadata.add_argument(dest='show_key', required=False, type=str, nargs=1, metavar="SHOW_KEY", help="shows the value of the supplied key if it exists", **key_arg)
# import command
import_command = commands.add_parser('import', fromfile_prefix_chars='@', help="usage: import '@path'")
# import 'path' argument
import_command.add_argument(dest="metadata", metavar="METADATA", type=str, nargs="+", help="Replaces the metadata dictionary with the values supplied by passing a json formatted string from stdn or from a file path prefixed with '@'")
# dump command
dump_command = commands.add_parser("dump", help="usage: dump ['path'] [['key(s)']]")
# dump 'path' argument
dump_command.add_argument(dest='dump_file', required=False, type=str, nargs=1, metavar="DUMP_FILE", help="the path to the dump file")
# dump 'keys' argument
dump_command.add_argument(dest='dump_keys', required=False, type=str, nargs="*", metavar="DUMP_KEYS", help="print the value of the supplied key(s) to file or std out")
# update command
edit_command = commands.add_parser('edit', help="usage: edit 'key' 'value'")
# update 'path' argument
edit_command.add_argument(dest="key_value", type=str, nargs=2, metavar="KEY_VALUE", help="Create, update, and delete metadata key/value pairs.\n\
    The type of operation is determined by applying the following rules to the key and value arguments passed.\n\
        If key argument exists in metadata and supplied value is not an empty string, update value in metadata.\n\
            If key argument exists in metadata, and value argument is an empty string, try to delete the key/value item in metadata or set an empty value in metadata.\n\
                If key does not exist in metadata, create key/value pair to metadata.")

# format output
def __output(value, stream=None):
    pprint(dumps(value), indent=4, stream=stream)

# return PDFToAI
def __pdf():
    rerturn PDFAI(args.input_file)

# return input_file full metadata or key/value item pair
def __get_metadata(key=None):
    return __pdf().metadata(key)

# default show_metadata function
def __show_metadata(show_key=None):
    __output(__get_metadata(show_key))
    
# default dump_command function
def __dump(path=None, key=None):
    stream = None
    if path:
        f = Path(path)
        if not f.exists():
            p = f.parent
            if not p.exists():
                p.mkdir(mode=641, parents=True)
            f.touch(mode=641)
        stream = f.open("w", encoding="utf8")
    __output(value, stream=stream)    

def __pdf_to_md():
    return pymupdf4llm.to_markdown()
    
    
        

def show_main_menu():
    print("MAIN MENU\n")
    prompts.prompt_for_choice([
        "Set Target Path",
        "Get Metadata",
        "Set Metadata", 
    ])[item]")

show_metadata.set_defaults(func=__show)    
dump_command.set_defaults(func=__dump)
args = parser.parse_args()
