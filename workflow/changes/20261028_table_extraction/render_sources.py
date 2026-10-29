from pathlib import Path
import json
import hashlib
import pypdfium2 as pdfium
from PySide6.QtGui import QImage
HERE=Path(__file__).resolve().parent
run=Path((HERE/'pilot_run.txt').read_text().strip())
plan=json.loads((run/'plan.json').read_text())
out=HERE/'renders';out.mkdir(exist_ok=True)
for source in plan['documents']:
    path=Path(source['path'])
    assert hashlib.sha256(path.read_bytes()).hexdigest()==source['sha256']
    ticker='NTU' if 'nutun' in path.name else 'PAN'
    pages=[22,24,25] if ticker=='NTU' else [48,49]
    doc=pdfium.PdfDocument(path)
    try:
        for number in pages:
            page=doc[number-1];bitmap=page.render(scale=1.5,rev_byteorder=True)
            fmt=QImage.Format.Format_RGB888 if bitmap.n_channels==3 else QImage.Format.Format_RGBA8888
            image=QImage(bitmap.buffer,bitmap.width,bitmap.height,bitmap.stride,fmt).copy()
            assert image.save(str(out/f'{ticker}_{number}.png'))
            bitmap.close();page.close()
    finally:doc.close()
print('Rendered five hash-verified original pages; handles closed.')
