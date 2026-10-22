from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap, QPolygonF
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView

from .pdf_source import Capture, PdfSource


class PdfCanvas(QGraphicsView):
    selection_changed = Signal(object)
    problem = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setBackgroundBrush(QColor("#e7ecf2"))
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.source = None
        self.page = 1
        self.mode = "area"
        self.start = None
        self.end = None
        self.outline = None
        self.text_polygons = []
        self.fit_enabled = True
        self.set_mode("area")

    def set_source(self, source: PdfSource):
        self.source = source
        self.show_page(1)

    def show_page(self, page: int):
        self.clear_selection()
        self.page = page
        self.scene().clear()
        if self.source:
            image = self.source.render(page)
            width, height = self.source.size(page)
            item = self.scene().addPixmap(QPixmap.fromImage(image))
            item.setScale(width / image.width())
            self.setSceneRect(QRectF(0, 0, width, height))
            if self.fit_enabled:
                self.fit_page()

    def set_mode(self, mode: str):
        self.mode = mode
        self.clear_selection()
        self.setCursor(Qt.CursorShape.IBeamCursor if mode == "text" else Qt.CursorShape.CrossCursor)

    def clear_selection(self):
        self.start = self.end = self.outline = None
        self.text_polygons = []
        self.viewport().update()
        self.selection_changed.emit(None)

    def fit_page(self):
        self.fit_enabled = True
        if self.source:
            self.fitInView(self.sceneRect().adjusted(-8, -8, 8, 8), Qt.AspectRatioMode.KeepAspectRatio)

    def zoom(self, multiplier: float):
        self.fit_enabled = False
        current = self.transform().m11()
        desired = min(5.0, max(0.2, current * multiplier))
        self.scale(desired / current, desired / current)

    def point_on_page(self, point) -> QPointF:
        mapped = self.mapToScene(point)
        rect = self.sceneRect()
        return QPointF(max(0.0, min(rect.width(), mapped.x())), max(0.0, min(rect.height(), mapped.y())))

    def mousePressEvent(self, event):
        self.setFocus()
        if self.source and event.button() == Qt.MouseButton.LeftButton:
            if not self.sceneRect().contains(self.mapToScene(event.position().toPoint())):
                return
            self.clear_selection()
            self.start = self.point_on_page(event.position().toPoint())
            self.end = self.start
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.start is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.end = self.point_on_page(event.position().toPoint())
            self.outline = QRectF(self.start, self.end).normalized()
            if self.mode == "text":
                self.text_polygons = self.source.selection(self.page, self.start, self.end).bounds()
            self.viewport().update()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.start is not None:
            self.end = self.point_on_page(event.position().toPoint())
            try:
                if self.mode == "text":
                    capture = self.source.capture_text(self.page, self.start, self.end)
                else:
                    capture = self.source.capture_area(self.page, QRectF(self.start, self.end))
                self.show_capture(capture)
                self.selection_changed.emit(capture)
            except (ValueError, OSError) as exc:
                self.clear_selection()
                self.problem.emit(str(exc))
            finally:
                self.start = self.end = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def show_capture(self, capture: Capture):
        x0, top, x1, bottom = capture.bbox
        self.outline = QRectF(x0, top, x1 - x0, bottom - top)
        self.text_polygons = [QPolygonF([QPointF(*point) for point in poly]) for poly in capture.polygons]
        self.viewport().update()

    def select_full_page(self):
        if self.source:
            cap = self.source.capture_area(self.page, self.sceneRect())
            self.show_capture(cap)
            self.selection_changed.emit(cap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.clear_selection()
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.zoom(1.2 if event.angleDelta().y() > 0 else 1 / 1.2)
            event.accept()
        else:
            super().wheelEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.fit_enabled:
            self.fit_page()

    def drawForeground(self, painter, rect):
        super().drawForeground(painter, rect)
        painter.save()
        pen = QPen(QColor("#087e8b"), 1.5)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(QColor(8, 126, 139, 45))
        if self.text_polygons:
            for polygon in self.text_polygons:
                painter.drawPolygon(polygon)
        elif self.outline:
            painter.drawRect(self.outline)
        painter.restore()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.source is None:
            painter = QPainter(self.viewport())
            painter.setPen(QColor("#526478"))
            painter.drawText(self.viewport().rect(), Qt.AlignmentFlag.AlignCenter,
                             "Open a PDF to begin\n\nSelect text or draw an area, then save a section.")
            painter.end()
