from pathlib import Path
import json
import pypdfium2 as pdfium
from PySide6.QtGui import QImage
HERE=Path(__file__).resolve().parent
run=Path((HERE/'review_run.txt').read_text(encoding='utf-8'))
manifest=json.loads((run/'inputs/manifest.json').read_text(encoding='utf-8'))
source=next(x for x in manifest['sources'] if x['ticker']=='NTU')
doc=pdfium.PdfDocument(source['path']);page=doc[24];b=page.render(scale=4,rev_byteorder=True)
fmt=QImage.Format.Format_RGB888 if b.n_channels==3 else QImage.Format.Format_RGBA8888
im=QImage(b.buffer,b.width,b.height,b.stride,fmt).copy()
assert im.copy(280,1070,1920,380).save(str(run/'source_pages/NTU_25_comparative_detail.png'))
b.close();page.close();doc.close()
