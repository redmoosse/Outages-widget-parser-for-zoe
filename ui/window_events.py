from PyQt6.QtCore import Qt, QRect

class WindowMixin:
    def minimize_window(self):
        self.setWindowState(Qt.WindowState.WindowMinimized)

    def toggle_expand(self, index):
        if not self.is_expanded:
            self.stack.setCurrentIndex(index)
            self.stack.show()
            self.animate_resize(self.compact_size, self.expanded_size)
            self.is_expanded = True
        else:
            if self.stack.currentIndex() == index:
                self.animate_resize(self.expanded_size, self.compact_size)
                self.is_expanded = False
            else:
                self.stack.setCurrentIndex(index)

    def animate_resize(self, start_size, end_size):
        start_rect = self.geometry()
        end_y = start_rect.y() + (start_rect.height() - end_size[1])
        end_rect = QRect(start_rect.x(), end_y, end_size[0], end_size[1])

        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        if end_size == self.compact_size:
            self.stack.hide() 
        self.anim.start()

    def on_animation_step(self, value):
        self.container.setGeometry(0, 0, value.width(), value.height())

    def stick_to_corner(self):
        import sys
        if 'PyQt6.QtWidgets' in sys.modules:
            QApplication = sys.modules['PyQt6.QtWidgets'].QApplication
            screen = QApplication.primaryScreen().availableGeometry()
            self.move(screen.width() - self.compact_size[0] - 25, screen.height() - self.compact_size[1] - 50)

    def mousePressEvent(self, event): 
        if event.button() == Qt.MouseButton.LeftButton:
            if event.pos().x() >= self.width() - 20 and event.pos().y() >= self.height() - 20:
                self.resizing = True
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_geometry = self.geometry()
            else:
                self.resizing = False
                self.dragPos = event.globalPosition().toPoint()
            
    def mouseMoveEvent(self, event):
        if not event.buttons():
            if event.pos().x() >= self.width() - 20 and event.pos().y() >= self.height() - 20:
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
            return

        if self.resizing:
            delta = event.globalPosition().toPoint() - self.resize_start_pos
            new_w = max(250, self.resize_start_geometry.width() + delta.x())
            new_h = max(150, self.resize_start_geometry.height() + delta.y())
            self.resize(new_w, new_h)
            self.container.setGeometry(0, 0, new_w, new_h)
            
            if self.is_expanded:
                self.expanded_size = (new_w, new_h)
            else:
                self.compact_size = (new_w, new_h)
        elif hasattr(self, 'dragPos'):
            self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
            self.dragPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.save_layout()