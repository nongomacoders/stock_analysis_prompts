import sys
from pathlib import Path
import pypdfium2 as pdfium
from PySide6.QtGui import QImage

root = Path.cwd()
run = root / 'companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T175621Z_codex_max_comparison'
calc = run / 'calculations'
calc.mkdir(exist_ok=True)
pdf = next((root / 'companies/consumer_lending/NTU/sources').rglob('*.pdf'))
doc = pdfium.PdfDocument(str(pdf))
texts = []
for i in range(len(doc)):
    page = doc[i]
    tp = page.get_textpage()
    texts.append(f'--- PHYSICAL PAGE {i+1} ---\n' + tp.get_text_range())
    tp.close()
    if i + 1 in [8, 12, 13, 23, 25, 31]:
        bitmap = page.render(scale=1.7, rev_byteorder=True)
        fmt = QImage.Format.Format_RGBA8888 if bitmap.n_channels == 4 else QImage.Format.Format_RGB888
        img = QImage(bitmap.buffer, bitmap.width, bitmap.height, bitmap.stride, fmt).copy()
        assert img.save(str(calc / f'page_{i+1:02}.png'))
        bitmap.close()
    page.close()
doc.close()
(calc / 'source_pages.txt').write_text('\n\n'.join(texts), encoding='utf-8')
print("Rendered pages and extracted source_pages.txt to calculations successfully.")
