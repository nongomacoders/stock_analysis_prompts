import sys
from pathlib import Path
import pypdfium2 as pdfium
from PySide6.QtGui import QImage
sys.stdout.reconfigure(encoding='utf-8')
root=Path.cwd()
run=Path((root/'scratch/ntu_comparison_latest.txt').read_text(encoding='utf-8').strip())
calc=run/'calculations'
calc.mkdir(exist_ok=True)
pdf=next((root/'companies/consumer_lending/NTU/sources').rglob('*.pdf'))
doc=pdfium.PdfDocument(str(pdf))
texts=[]
for i in range(len(doc)):
    page=doc[i]
    tp=page.get_textpage()
    texts.append(f'--- PHYSICAL PAGE {i+1} ---\n'+tp.get_text_range())
    tp.close()
    if i+1 in [8,12,13,23,25,31]:
        bitmap=page.render(scale=1.7,rev_byteorder=True)
        fmt=QImage.Format.Format_RGBA8888 if bitmap.n_channels==4 else QImage.Format.Format_RGB888
        img=QImage(bitmap.buffer,bitmap.width,bitmap.height,bitmap.stride,fmt).copy()
        assert img.save(str(calc/f'page_{i+1:02}.png'))
        bitmap.close()
    page.close()
doc.close()
(calc/'source_pages.txt').write_text('\n\n'.join(texts),encoding='utf-8')
for number in [8,9,12,13,14,15,16]:
    print(texts[number-1])
