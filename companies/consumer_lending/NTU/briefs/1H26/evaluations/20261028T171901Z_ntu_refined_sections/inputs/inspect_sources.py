"""Read-only original PDF spot-checks for observed live-run errors."""
import importlib.util
from pathlib import Path
import pypdfium2 as pdfium
from PySide6.QtGui import QImage
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('trial',HERE/'ntu_sections.py');t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
run=Path(t.POINTER.read_text(encoding='utf-8').strip());source=t.m.read(run/'plan.json')['documents'][0]
assert t.m.sha(Path(source['path']))==source['sha256']
(run/'source_pages').mkdir(exist_ok=True)
doc=pdfium.PdfDocument(source['path'])
for number in [13,22,24,25,31]:
    page=doc[number-1];b=page.render(scale=1.8,rev_byteorder=True)
    fmt=QImage.Format.Format_RGB888 if b.n_channels==3 else QImage.Format.Format_RGBA8888
    image=QImage(b.buffer,b.width,b.height,b.stride,fmt).copy()
    assert image.save(str(run/'source_pages'/f'NTU_{number}.png'))
    text=page.get_textpage();t.m.text(run/'source_pages'/f'NTU_{number}.txt',text.get_text_range());text.close()
    b.close();page.close()
doc.close()
print('Rendered5 original pages;source hash verified;all PDF handles closed.')
