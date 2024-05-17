from pdf2image import convert_from_path
import os
from pathlib import Path

def pdf2img(pdf_path, img_path, filename):
    poper_path = Path(__file__).resolve().parent.parent /'Release-24.02.0-0'/'poppler-24.02.0'/'Library'/'bin'
    images = convert_from_path(pdf_path=pdf_path, poppler_path=poper_path)
    images[0].save(os.path.join(img_path, filename + '.jpg'), 'JPEG')
    return filename + '.jpg'


