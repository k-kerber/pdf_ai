from llama_index.readers.file import PyMuPDFReader
from pathlib import Path
import pymupdf
import pymupdf4llm
from pprint import pprint
from humanfriendly import prompts
from json import dumps

class PDFToAI:
    def __init__(self, path):
        p = Path(path)
        if p.exists() and p.is_file() and p.suffix == ".pdf":
            self.__alt_metadata = {
                'author': '',
                'creationDate': "",
                'creator': '',
                'encryption': None,
                'format': '',
                'keywords': '',
                'modDate': "",
                'producer': '',
                'subject': '',
                'title':  '',
                'trapped': ''
            }
            self.__base_metadata = self.__get_base_metadata()
            self.__doc = self.__get_doc()
            self.__ex_metadata = self.__get_ex_metadata()
            self.__headings = []
            self.__llama_doc = self.__get_llama_doc()
            self.__path = path
            self.__markdown = ''
            self.__metadata = self.__get_metadata()
            self.__xref_xml_metadata = self.__get_xref_xml_metadata()
            
    def __get_base_metadata(self, key=None):
        if self.__base_metadata is None:
            self.__base_metadata = self.__doc.metadata
        if key:
            if key in self.__base_metadata:
                return { key: self.__base_metadata.get(key) }
            else:
                return None
        return self.__base_metadata
        
    def __get_doc(self):
        if not self.__doc:
            self.__doc = pymupdf.open(self.__path)
        return self.__doc

    def __get_ex_metadata(self, key=None):
        if self.__ex_metadata is None:
            self.__ex_metadata = {}
            xref = self.__get_xref_xml_metadata()
            doc = self.__get_doc()
            if xref is None or doc is None:
                return None
            for k in doc.xref_get_keys(xref):
                self.__ex_metadata[k] = doc.xref_get_key(xref, k)[1]
        if key:
            if key in self.__ex_metadata:
                return { key: self.__ex_metadata.get(key) }
            else:
                return self.__set_ex_metadata(key)
        return self.__ex_metadata

    def __get_llama_doc(self):
        if self.__llama_doc is None:
            loader = PyMuPDFReader()
            self.__llama_doc = loader.load(file_path=self.__path)[0]
        return self.__llama_doc

    def __get_metadata(self):
        return self.__get_base_metadata() | self.__get_ex_metadata()
    
    def __get_xref_xml_metadata(self):
        if not self.__xref_xml_metadata:
            doc = self.__get_doc()
            if not doc.xref_xml_metadata:
                what, value = doc.xref_get_key(-1, "Info")  # /Info key in the trailer 
                if what != "xref":
                    return
                else:
                    self.__xref_xml_metadata = int(value.replace("0 R", ""))  # extract the metadata xref
            else:
                self.__xref_xml_metadata = doc.xref_xml_metadata
        return self.__xref_xml_metadata

    def __set_ex_metadata(self, adict=None, key=None, value=''):
        if adict:
            for k in adict:
                
        k = str(key)
        if k:
            self.__doc.xref_set_key(self.__metadata_xref, k, pymupdf.get_pdf_str(value))
            (key, value) = self.__doc.xref_get_key(self.__metadata_xref, k)
            return {key: value}
        return None

    def get_alt_metadata(self)
        return self.__alt_metadata
            


    def set_metadata(self, key=None, value=''):
        if key:
            k = str(key)
            v = pymupdf.get_pdf_str(value)
            if (k in self.__base_metadata):
            

    def get_metadata(self):
        return self.__base_metadata | self.__ex_metadata
    
    def get_doc(self):
        return self.__doc

    def get_metadata(self, key=None):
        if key:
            if key in self.__metadata:
                return { key: self.__metadata.get(key) }
            else:
                
                return 
        return self.__metadata

    def __to_json(self, value, stream=None):
        pprint(dumps(value, stream=stream), indent=4)