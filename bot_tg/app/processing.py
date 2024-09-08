from spire.doc import *
from spire.doc.common import *
import aspose.words as aw
import os


def docx2pdf(docxPath: str, Path2savePDF: str):
    document = Document()
    document.LoadFromFile(docxPath)
    document.SaveToFile(Path2savePDF, FileFormat.PDF)
    document.Close()


def createpass(docPath:str, password:str):
    doc = aw.Document(docPath)

    if docPath.find(".docx"):
        options = aw.saving.OoxmlSaveOptions(aw.SaveFormat.DOCX)


        options.password = password
    elif docPath.find(".pdf"):
        options = aw.saving.PdfSaveOptions(aw.SaveFormat.PDF)

    os.remove(docPath)
    doc.save(docPath, options)
