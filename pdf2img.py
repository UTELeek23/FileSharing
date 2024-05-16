from pdf2image import convert_from_path
import os

poper_path = r'D:\HCMUTE\Python\Release-24.02.0-0\poppler-24.02.0\Library\bin'
pdf_path = r'OS-LAB.pdf'
save_dir = r'D:\HCMUTE\Python\lab10'
images = convert_from_path(pdf_path=pdf_path, poppler_path=poper_path)

images[0].save(os.path.join(save_dir, 'OS-LAB.jpg'), 'JPEG')

    