from llama_index.readers.file import PyMuPDFReader
from pathlib import Path
import pymupdf
import pymupdf4llm

class PDFAI:


    def __init__(self, path):
        p = Path(path)
        if p.exists() and p.is_file() and p.suffix == ".pdf":
            doc = pymupdf.open(path)
            xref = doc.xref_xml_metadata
            ex_metadata = {}
            for k in doc.xref_get_keys(xref):
                ex_metadata[k] = doc.xref_get_key(xref, k)[1]
            self.__doc = doc
            self.__ex_metadata = ex_metadata
            self.__headings = []
            self.__llama_doc = PyMuPDFReader().load(file_path=path)[0]
            self.__markdown = pymupdf4llm.to_markdown(path)
            self.__metadata = doc.metadata | ex_metadata
            self.__path = path
            self.__xref_xml_metadata = xref


    def get_metadata(self, key=None):
        m = self.__doc.metadata
        e = self.__ex_metadata
        if key is None:
            return m | e
        else:
            k = str(key)
            v = None
            if k in m:
                v = m.get(k)
            elif k in e:
                v = e.get(k)
            return {k: v}


    def set_metadata(self, adict):
        keys = ['author', 'creationDate', 'creator', 'encryption', 'format', 'keywords', 'modDate', 'producer', 'subject', 'title', 'trapped']
        m = {}
        for k in adict:
            value = pymupdf.get_pdf_str(adict.get(k))
            key = str(k)
            if key in keys:
                m[key] = value
            else:
                self.__doc.xref_set_key(self.__xref_xml_metadata, key, value)
                self.__ex_metadata[key] = value
        if len(m) > 0:
            u = self.__doc.metadata | m
            self.__doc.set_metadata(u)