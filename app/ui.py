import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QCheckBox, QGraphicsEllipseItem, QGraphicsPolygonItem
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor, QPolygonF, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QPointF

from app.exiva import Exiva 

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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.viewer = ImageViewer()
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_marker)
        self.submit_button.setEnabled(False)  

        plus_button = QPushButton('+')
        minus_button = QPushButton('-')
        plus_button.clicked.connect(self.viewer.next_image)
        minus_button.clicked.connect(self.viewer.prev_image)

        button_layout = QHBoxLayout()
        button_layout.addWidget(plus_button)
        button_layout.addWidget(minus_button)

        self.direction_checkboxes = []
        directions = [
            ["NW", "N", "NE"],
            ["W", " ", "E"],
            ["SW", "S", "SE"]
        ]
        
        direction_layout = QVBoxLayout()

        for row in directions:
            row_layout = QHBoxLayout()
            group = []
            for direction in row:
                checkbox = QCheckBox(direction)
                checkbox.clicked.connect(self.handle_direction_checkbox_click)
                self.direction_checkboxes.append(checkbox)
                group.append(checkbox)
                row_layout.addWidget(checkbox)
            direction_layout.addLayout(row_layout)

        self.exclusive_group(self.direction_checkboxes) 

        self.distance_checkboxes = []
        distances = ["Nearby", "Normal", "Far", "Very Far"]
        distance_layout = QHBoxLayout()
        group = []
        for distance in distances:
            checkbox = QCheckBox(distance)
            checkbox.clicked.connect(self.handle_distance_checkbox_click)
            self.distance_checkboxes.append(checkbox)
            group.append(checkbox)
            distance_layout.addWidget(checkbox)
        distance_layout.addStretch(1)
        direction_layout.addLayout(distance_layout)
        self.exclusive_group(group)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.submit_button)
        left_layout.addLayout(direction_layout)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.viewer)

        self.clear_all_button = QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clear_all)

        left_layout.addWidget(self.clear_all_button)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.setWindowTitle('Fiend Finder 3000')
        self.adjustWindowSize()

    def adjustWindowSize(self):
        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        self.resize(screen_rect.width(), screen_rect.height())

    def submit_marker(self):
        if self.viewer.marker:
            marker_pos = self.viewer.marker.pos()
            x_pos = marker_pos.x()
            y_pos = marker_pos.y()
            exiva = Exiva(x_pos, y_pos)

            range_key = None
            for checkbox in self.distance_checkboxes:
                if checkbox.isChecked():
                    range_key = checkbox.text()
                    break

            direction_key = None
            for checkbox in self.direction_checkboxes:
                if checkbox.isChecked():
                    direction_key = checkbox.text()
                    break
            
            if range_key and direction_key:
                vertices = exiva.get_vertices(direction_key, range_key)
                
                adjusted_vertices = [(x + x_pos, y + y_pos) for x, y in vertices]

                polygon = QPolygonF([QPointF(x, y) for x, y in adjusted_vertices])
                polygon_item = QGraphicsPolygonItem(polygon)
                polygon_item.setPen(Qt.red)
                polygon_item.setBrush(QBrush(QColor(255, 0, 0, 128)))  

                self.viewer.add_polygon(polygon_item)

                self.viewer.markers.append(self.viewer.marker)
                self.viewer.marker = None

                print("Exiva object created at coordinates:", x_pos, ",", y_pos)
                exiva.print_all()

                self.clear_all_button.setEnabled(True)  

    def clear_all(self):
        for marker in self.viewer.markers:
            self.viewer.scene().removeItem(marker)
        self.viewer.markers = []  

        for polygon in self.viewer.polygons:
            self.viewer.scene().removeItem(polygon)
        self.viewer.polygons = []  

        self.clear_all_button.setEnabled(False) 

    def exclusive_group(self, checkboxes):
        for checkbox in checkboxes:
            checkbox.toggled.connect(lambda state, cb=checkbox: self.checkbox_exclusive_toggle(cb, checkboxes))

    def checkbox_exclusive_toggle(self, selected_checkbox, checkboxes):
        if selected_checkbox.isChecked():
            for checkbox in checkboxes:
                if checkbox != selected_checkbox:
                    checkbox.setChecked(False)
        
        self.check_submit_button_state()

    def handle_direction_checkbox_click(self):
        self.check_submit_button_state()

    def handle_distance_checkbox_click(self):
        self.check_submit_button_state()

    def check_submit_button_state(self):
        if (any(checkbox.isChecked() for checkbox in self.direction_checkboxes) and
            any(checkbox.isChecked() for checkbox in self.distance_checkboxes)):
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
