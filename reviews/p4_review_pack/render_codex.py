import sys,pathlib,pypdfium2 as pdfium
from PySide6.QtGui import QImage
sys.stdout.reconfigure(encoding='utf-8')
d=pdfium.PdfDocument('companies/mining/PAN/sources/Pan-African-Resources-year-end-results-SENS-announcement-2026.pdf')
for i in [18,21,22,23,24,29,33,34,35,44,46]:
 pg=d[i-1];bm=pg.render(scale=2);fmt=QImage.Format.Format_BGR888 if bm.n_channels==3 else QImage.Format.Format_ARGB32
 im=QImage(bytes(bm.buffer),bm.width,bm.height,bm.stride,fmt).copy();out=pathlib.Path(f'reviews/p4_review_pack/codex_evidence/p{i}.png').resolve();ok=im.save(str(out),'PNG');assert ok,(i,bm.n_channels,im.isNull());bm.close();pg.close()
d.close()
