import sys
import ctypes
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import QTimer, QDate

from core.zoe_parser import WorkerSignals
from ui.ui_setup import UIMixin
from ui.settings import SettingsMixin
from ui.window_events import WindowMixin
from ui.schedule_logic import ScheduleMixin
from ui.app_actions import ActionsMixin

myappid = 'mycompany.myproduct.subproduct.version'
try:
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

class PowerScheduleWidget(QWidget, UIMixin, SettingsMixin, WindowMixin, ScheduleMixin, ActionsMixin):
    def __init__(self):
        super().__init__()
        
        self.default_start = datetime(2026, 3, 2, 12, 0, 0)
        self.default_off = 5
        self.default_on = 4
        self.default_opacity = 95
        self.default_font_size = 13
        
        self.is_expanded = False
        self.resizing = False
        self._updating = True
        
        self.tuya_token = None
        self.last_tuya_v = None
        self.last_tuya_w = None
        self.tuya_error_logged = False
        self.alerted_voltage = False
        self.alerted_time = False
        self.current_timer_state = None
        
        self.is_alerting_bg = False
        self.current_fetch_id = 0 

        self.signals = WorkerSignals()
        self.signals.log.connect(self.log_message)
        self.signals.success.connect(self._apply_zoe_result)
        self.signals.fail.connect(self._fail_zoe_result)

        self.load_settings()
        self.init_ui()
        self.apply_settings_to_ui()
        self.update_styles()
        
        if self.pos_x is not None and self.pos_y is not None:
            screen = QApplication.primaryScreen().availableGeometry()
            safe_x = max(0, min(self.pos_x, screen.width() - self.compact_size[0]))
            safe_y = max(0, min(self.pos_y, screen.height() - self.compact_size[1]))
            self.move(safe_x, safe_y)
        else:
            self.stick_to_corner()
            
        self._updating = False

        self.schedule_timer = QTimer()
        self.schedule_timer.timeout.connect(self.update_live_timer)
        self.schedule_timer.start(1000)

        self.tuya_timer = QTimer()
        self.tuya_timer.timeout.connect(self.refresh_tuya_stats)
        self.tuya_timer.start(10000)

        self.zoe_auto_timer = QTimer()
        self.zoe_auto_timer.timeout.connect(self.auto_fetch_zoe)
        if self.auto_update_zoe:
            self.zoe_auto_timer.start(self.auto_update_interval * 60000)

        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.setInterval(500)
        self.debounce_timer.timeout.connect(self._apply_auto_update_changes)

        self.queue_debounce_timer = QTimer()
        self.queue_debounce_timer.setSingleShot(True)
        self.queue_debounce_timer.setInterval(1000)
        self.queue_debounce_timer.timeout.connect(self._auto_fetch_on_type)

        self.calendar.setSelectedDate(QDate.currentDate())
        self.on_calendar_selection_changed() 
        
        self.load_logs()
        self.log_message("System started.", alert=False)
        self.refresh_tuya_stats() 
        
        if self.zoe_queue.strip():
            QTimer.singleShot(1000, lambda: self.fetch_zoe_schedule(silent=True))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PowerScheduleWidget()
    w.show()
    w.setMouseTracking(True)
    w.container.setMouseTracking(True)
    sys.exit(app.exec())