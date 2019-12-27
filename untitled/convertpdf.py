import img2pdf
from PIL import Image
import os

# storing image path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path = os.path.join(BASE_DIR, "untitled", "page-db4e552e-857a5531-0001.png")

fileList = os.listdir(os.path.join(BASE_DIR, 'untitled'))
imageList = [img_path]

from fpdf import FPDF
pdf = FPDF()
# imagelist is the list with all image filenames
for image in imageList:
    pdf.add_page()
    pdf.image(image)
pdf.output("yourfile.pdf", "F")