# app/viewer.py

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF

from app.exiva import Exiva  # Importing Exiva class from exiva.py

class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale_factor = 1.25
        self.current_image_index = 7
        self.image_items = []
        self.min_scale = 0.2
        self.max_scale = 2048 / 40
        self.markers = [] 
        self.marker = None  
        self.polygons = []  

        for i in range(16):
            pixmap = QPixmap(f'map_png/{i}.png')
            item = QGraphicsPixmapItem(pixmap)
            self.image_items.append(item)
            if i == 7:
                self.scene().addItem(item)

        self.show_image(self.current_image_index)
        self.scale_image_to_fit()

    def wheelEvent(self, event):
        zoom_in_factor = self.scale_factor
        zoom_out_factor = 1 / self.scale_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
              
        new_scale = self.transform().m11() * zoom_factor

        if self.min_scale <= new_scale <= self.max_scale:
            self.scale(zoom_factor, zoom_factor)

        self.update_layering()

    def show_image(self, index):
        for item in self.image_items:
            self.scene().removeItem(item)
        
        self.scene().addItem(self.image_items[index])
        self.setSceneRect(QRectF(self.image_items[index].pixmap().rect()))

        for marker in self.markers:
            self.scene().addItem(marker)
        
        for polygon in self.polygons:
            self.scene().addItem(polygon)

    def prev_image(self):
        if self.current_image_index < 15:
            self.current_image_index += 1
            self.show_image(self.current_image_index)

    def next_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image(self.current_image_index)

    def scale_image_to_fit(self):
        current_item = self.image_items[self.current_image_index]
        initial_scale = min(self.width() / current_item.pixmap().width(),
                            self.height() / current_item.pixmap().height())
        self.resetTransform()
        self.scale(initial_scale, initial_scale)

    def add_marker(self, event):
        if self.marker:
            self.scene().removeItem(self.marker) 
        
        marker_size = 10.0
        marker = QGraphicsEllipseItem(-marker_size / 2, -marker_size / 2, marker_size, marker_size)
        marker.setPen(Qt.red)
        marker.setBrush(Qt.red)
        marker.setPos(self.mapToScene(event.pos()))
        self.scene().addItem(marker)
        self.marker = marker  
        marker.setZValue(1)
        self.markers.append(marker)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.RightButton:
            self.add_marker(event)

    def update_layering(self):
        for marker in self.markers:
            marker.setZValue(1)

        for polygon in self.polygons:
            polygon.setZValue(1)

    def add_polygon(self, polygon_item):
        polygon_item.setZValue(1)
        self.polygons.append(polygon_item)
        self.scene().addItem(polygon_item)
