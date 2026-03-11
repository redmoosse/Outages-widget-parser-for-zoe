from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QCalendarWidget, QTextEdit,
                             QStackedWidget, QSlider, QSpinBox, QDateTimeEdit, QDateEdit,
                             QFormLayout, QCheckBox, QLineEdit, QScrollArea, QFileDialog)
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QDate
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QTextCharFormat

def create_app_icon():
    pixmap = QPixmap(64, 64)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor("#FF5252"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
    painter.setPen(QColor("white"))
    painter.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "⚡")
    painter.end()
    return QIcon(pixmap)

class UIMixin:
    def update_styles(self):
        alpha = int((self.opacity_val / 100.0) * 255)
        tc = self.text_color
        fs = self.font_size
        
        show_bg = True
        if hasattr(self, 'cb_bg_alert_only') and self.cb_bg_alert_only.isChecked():
            show_bg = getattr(self, 'is_alerting_bg', False)
            
        bg_css = ""
        if show_bg and getattr(self, 'custom_bg_path', '') and __import__('os').path.exists(self.custom_bg_path):
            bg_url = self.custom_bg_path.replace("\\", "/")
            bg_css = f'background-image: url("{bg_url}"); background-position: center; background-repeat: no-repeat;'
        
        css = f"""
            #main_container {{ background-color: rgba(22, 22, 22, {alpha}); {bg_css}
                border: 1px solid rgba(80, 80, 80, {alpha}); border-radius: 16px; }}
            QLabel {{ font-family: 'Segoe UI', sans-serif; color: {tc}; }}
            QLabel#status_lbl {{ font-weight: 900; font-size: {int(fs * 2.0)}px; }}
            QLabel#timer_lbl {{ font-family: 'Consolas', monospace; font-weight: 900; font-size: {int(fs * 1.8)}px; color: {tc}; }}
            QLabel#settings_lbl {{ font-weight: bold; font-size: {fs}px; color: {tc}; }}
            QLabel#tuya_data_lbl {{ font-weight: bold; font-size: {max(11, int(fs * 0.9))}px; color: {tc}; }}
            QLabel#tuya_time_lbl {{ font-weight: bold; font-size: {max(9, int(fs * 0.75))}px; color: #888; }}
            QPushButton#btn_icon {{ background: transparent; color: {tc}; border: none; padding: 4px; }}
            QPushButton#btn_icon:hover {{ background-color: rgba(255,255,255,0.1); border-radius: 8px; }}
            QPushButton#btn_min, QPushButton#btn_close {{ background: transparent; color: #888; border: none; font-size: 20px; font-weight: 900; }}
            QPushButton#btn_min:hover {{ background-color: rgba(255,255,255,0.1); color: {tc}; border-radius: 8px; }}
            QPushButton#btn_close:hover {{ background-color: #FF5252; color: #fff; border-radius: 8px; }}
            QPushButton#btn_action {{ background-color: rgba(51, 51, 51, {alpha}); color: {tc}; border: 1px solid rgba(85, 85, 85, {alpha}); border-radius: 6px; padding: 6px; font-weight: bold; font-size: {fs}px; }}
            QPushButton#btn_action:hover {{ background-color: rgba(85, 85, 85, 255); }}
            QPushButton#btn_action_green {{ background-color: rgba(46, 125, 50, {alpha}); color: white; border: 1px solid rgba(85, 85, 85, {alpha}); border-radius: 6px; padding: 6px; font-weight: bold; font-size: {fs}px; }}
            QPushButton#btn_action_green:hover {{ background-color: rgba(27, 94, 32, 255); }}
            QPushButton#btn_tuya_toggle {{ background: transparent; color: {tc}; text-align: center; font-weight: bold; font-size: {fs+1}px; padding: 5px; border: none; }}
            QPushButton#btn_tuya_toggle:hover {{ color: #4CAF50; }}
            QCalendarWidget QWidget {{ color: {tc}; font-size: {max(8, fs - 3)}pt; }}
            QCalendarWidget QWidget#qt_calendar_navigationbar {{ background-color: transparent; border-top-left-radius: 8px; border-top-right-radius: 8px; }}
            QCalendarWidget QToolButton {{ color: {tc}; font-weight: bold; font-size: {max(8, fs - 2)}pt; border-radius: 4px; padding: 4px 8px; margin: 2px; }}
            QCalendarWidget QToolButton::menu-indicator {{ image: none; width: 0px; }}
            QCalendarWidget QToolButton:hover {{ background-color: rgba(255, 255, 255, 30); }}
            QCalendarWidget QMenu {{ background-color: rgba(34, 34, 34, 255); color: {tc}; }}
            QCalendarWidget QSpinBox {{ background-color: transparent; border: none; color: {tc}; font-size: {max(8, fs - 2)}pt; font-weight: bold; }}
            QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {{ width: 0px; }}
            QCalendarWidget QTableView {{ background-color: transparent; selection-background-color: #4CAF50; gridline-color: rgba(100, 100, 100, {alpha}); }}
            QTextEdit, QLineEdit {{ background-color: rgba(15, 15, 15, {alpha}); border: 1px solid rgba(85, 85, 85, {alpha}); border-radius: 6px; font-family: 'Consolas', monospace; font-size: {max(13, fs)}px; font-weight: bold; color: {tc}; padding: 8px; }}
            QSpinBox, QDateTimeEdit, QDateEdit {{ background-color: rgba(51, 51, 51, {alpha}); color: {tc}; border: 1px solid rgba(85, 85, 85, {alpha}); border-radius: 4px; padding: 4px; font-size: {fs}px; min-height: 24px; }}
            QCheckBox {{ color: {tc}; font-weight: bold; font-size: {fs}px; }}
            QScrollArea {{ background: transparent; border: none; }}
            QWidget#scroll_content {{ background: transparent; }}
            QScrollBar:vertical {{ background: rgba(30, 30, 30, 150); width: 8px; border-radius: 4px; }}
            QScrollBar::handle:vertical {{ background: rgba(100, 100, 100, 200); border-radius: 4px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """
        self.setStyleSheet(css)

        fmt_normal = QTextCharFormat()
        fmt_normal.setForeground(QColor(tc))
        self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, fmt_normal)
        self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, fmt_normal)

    def init_ui(self):
        self.setWindowIcon(create_app_icon())
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumSize(250, 150)
        self.resize(*self.compact_size)

        self.container = QWidget(self)
        self.container.setObjectName("main_container")
        self.container.setGeometry(0, 0, *self.compact_size)
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 10, 15, 15)
        layout.setSpacing(10)

        top_bar = QHBoxLayout()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        emoji_font = QFont("Segoe UI Emoji", 14)
        
        self.cal_btn = QPushButton("📅")
        self.cal_btn.setObjectName("btn_icon")
        self.cal_btn.setFont(emoji_font)
        self.cal_btn.setFixedSize(34, 34)
        self.cal_btn.clicked.connect(lambda: self.toggle_expand(0))
        top_bar.addWidget(self.cal_btn)

        self.log_btn = QPushButton("📝")
        self.log_btn.setObjectName("btn_icon")
        self.log_btn.setFont(emoji_font)
        self.log_btn.setFixedSize(34, 34)
        self.log_btn.clicked.connect(lambda: self.toggle_expand(1))
        top_bar.addWidget(self.log_btn)

        self.set_btn = QPushButton("⚙️")
        self.set_btn.setObjectName("btn_icon")
        self.set_btn.setFont(emoji_font)
        self.set_btn.setFixedSize(34, 34)
        self.set_btn.clicked.connect(lambda: self.toggle_expand(2))
        top_bar.addWidget(self.set_btn)
        
        top_bar.addStretch()
        
        self.min_btn = QPushButton("—")
        self.min_btn.setObjectName("btn_min")
        self.min_btn.setFixedSize(36, 36) 
        self.min_btn.clicked.connect(self.minimize_window)
        top_bar.addWidget(self.min_btn)

        self.close_btn = QPushButton("×")
        self.close_btn.setObjectName("btn_close")
        self.close_btn.setFixedSize(36, 36)
        self.close_btn.clicked.connect(QApplication.instance().quit)
        top_bar.addWidget(self.close_btn)
        
        layout.addLayout(top_bar)

        self.status_label = QLabel("Status: ...")
        self.status_label.setObjectName("status_lbl")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setObjectName("timer_lbl")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.tuya_data_label = QLabel("Voltage: -- V  |  Power: -- W")
        self.tuya_data_label.setObjectName("tuya_data_lbl")
        self.tuya_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.tuya_time_label = QLabel("Last Updated: --:--:--")
        self.tuya_time_label.setObjectName("tuya_time_lbl")
        self.tuya_time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.status_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.tuya_data_label)
        layout.addWidget(self.tuya_time_label)

        self.stack = QStackedWidget()
        
        self.cal_widget = QWidget()
        cal_layout = QVBoxLayout(self.cal_widget)
        cal_layout.setContentsMargins(0, 0, 0, 0)
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.selectionChanged.connect(self.on_calendar_selection_changed) 
        cal_layout.addWidget(self.calendar)
        self.schedule_display = QTextEdit()
        self.schedule_display.setReadOnly(True)
        cal_layout.addWidget(self.schedule_display)
        self.stack.addWidget(self.cal_widget)

        self.log_widget = QWidget()
        log_layout = QVBoxLayout(self.log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        log_layout.addWidget(self.log_display)
        self.stack.addWidget(self.log_widget)

        self.set_widget = QWidget()
        set_layout = QVBoxLayout(self.set_widget)
        set_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        scroll_content = QWidget()
        scroll_content.setObjectName("scroll_content")
        form_layout = QFormLayout(scroll_content)
        form_layout.setVerticalSpacing(15)
        
        self.slider_opacity = QSlider(Qt.Orientation.Horizontal)
        self.slider_opacity.setRange(20, 100)
        self.slider_opacity.valueChanged.connect(self.live_setting_update) 
        
        self.spin_font = QSpinBox()
        self.spin_font.setRange(8, 36)
        self.spin_font.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin_font.valueChanged.connect(self.live_setting_update)
        self.spin_font.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_color = QPushButton("Pick Text Color")
        self.btn_color.setObjectName("btn_action")
        self.btn_color.clicked.connect(self.choose_text_color)
        
        bg_layout = QHBoxLayout()
        self.le_bg_path = QLineEdit()
        self.le_bg_path.setPlaceholderText("Default Background")
        self.le_bg_path.setReadOnly(True)
        self.btn_choose_bg = QPushButton("📁")
        self.btn_choose_bg.setObjectName("btn_icon")
        self.btn_choose_bg.clicked.connect(self.choose_bg_file)
        self.btn_clear_bg = QPushButton("❌")
        self.btn_clear_bg.setObjectName("btn_icon")
        self.btn_clear_bg.clicked.connect(self.clear_bg_file)
        bg_layout.addWidget(self.le_bg_path)
        bg_layout.addWidget(self.btn_choose_bg)
        bg_layout.addWidget(self.btn_clear_bg)
        
        self.cb_bg_alert_only = QCheckBox("Show only on Alert")
        self.cb_bg_alert_only.stateChanged.connect(self.live_setting_update)

        sound_layout = QHBoxLayout()
        self.le_sound_path = QLineEdit()
        self.le_sound_path.setPlaceholderText("System Sound")
        self.le_sound_path.setReadOnly(True)
        self.btn_choose_sound = QPushButton("📁")
        self.btn_choose_sound.setObjectName("btn_icon")
        self.btn_choose_sound.clicked.connect(self.choose_sound_file)
        self.btn_clear_sound = QPushButton("❌")
        self.btn_clear_sound.setObjectName("btn_icon")
        self.btn_clear_sound.clicked.connect(self.clear_sound_file)
        sound_layout.addWidget(self.le_sound_path)
        sound_layout.addWidget(self.btn_choose_sound)
        sound_layout.addWidget(self.btn_clear_sound)

        self.cb_use_math_mode = QCheckBox("Enable Auto-Calendar")
        self.cb_use_math_mode.stateChanged.connect(self.live_setting_update)

        self.spin_off = QSpinBox()
        self.spin_off.setRange(1, 24)
        self.spin_off.setSuffix(" h")
        self.spin_off.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin_off.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.spin_on = QSpinBox()
        self.spin_on.setRange(1, 24)
        self.spin_on.setSuffix(" h")
        self.spin_on.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin_on.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dt_edit = QDateTimeEdit()
        self.dt_edit.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.dt_edit.setCalendarPopup(False) 
        self.dt_edit.setButtonSymbols(QDateTimeEdit.ButtonSymbols.NoButtons)

        update_layout = QHBoxLayout()
        self.cb_auto_zoe = QCheckBox("Auto-Update")
        self.cb_auto_zoe.stateChanged.connect(self._trigger_debounce_save)
        self.spin_auto_interval = QSpinBox()
        self.spin_auto_interval.setRange(1, 1440)
        self.spin_auto_interval.setSuffix(" m")
        self.spin_auto_interval.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.spin_auto_interval.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spin_auto_interval.valueChanged.connect(self._trigger_debounce_save)
        update_layout.addWidget(self.cb_auto_zoe)
        update_layout.addWidget(self.spin_auto_interval)
        update_layout.addStretch()

        self.le_queue = QLineEdit()
        self.le_queue.setPlaceholderText("Example: 1.2")
        self.le_queue.textChanged.connect(self._trigger_queue_debounce)
        
        self.btn_fetch = QPushButton("Update now")
        self.btn_fetch.setObjectName("btn_action_green")
        self.btn_fetch.clicked.connect(lambda: self.fetch_zoe_schedule(silent=False))

        self.custom_date_edit = QDateEdit()
        self.custom_date_edit.setDisplayFormat("dd.MM.yyyy")
        self.custom_date_edit.setCalendarPopup(True)
        self.custom_date_edit.setDate(QDate.currentDate())
        self.custom_date_edit.dateChanged.connect(self.on_settings_date_changed)

        self.cb_custom = QCheckBox("Custom date")
        self.cb_custom.stateChanged.connect(self.live_custom_update)
        self.le_custom = QLineEdit()
        self.le_custom.setPlaceholderText("08:00-12:00, 16:00-20:00")
        self.le_custom.textChanged.connect(self.live_custom_update)

        def create_lbl(text):
            lbl = QLabel(text)
            lbl.setObjectName("settings_lbl")
            return lbl

        form_layout.addRow(create_lbl("Bg Opacity:"), self.slider_opacity)
        form_layout.addRow(create_lbl("Font Size:"), self.spin_font)
        form_layout.addRow(create_lbl("Text Color:"), self.btn_color)
        form_layout.addRow(create_lbl("Background:"), bg_layout) 
        form_layout.addRow("", self.cb_bg_alert_only)
        form_layout.addRow(create_lbl("Alert Sound:"), sound_layout)
        
        lbl_math = create_lbl("--- Auto-Calendar ---")
        lbl_math.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addRow(lbl_math)
        form_layout.addRow("", self.cb_use_math_mode)
        form_layout.addRow(create_lbl("Start Point:"), self.dt_edit)
        form_layout.addRow(create_lbl("Default OFF:"), self.spin_off)
        form_layout.addRow(create_lbl("Default ON:"), self.spin_on)
        
        lbl_zoe = create_lbl("--- Parser ---")
        lbl_zoe.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addRow(lbl_zoe)
        form_layout.addRow(create_lbl("Outage:"), self.le_queue)
        form_layout.addRow("", update_layout)
        form_layout.addRow("", self.btn_fetch)
        
        lbl_custom = create_lbl("--- Custom Outage ---")
        lbl_custom.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addRow(lbl_custom)
        form_layout.addRow(self.cb_custom, self.custom_date_edit)
        form_layout.addRow(create_lbl("Hours:"), self.le_custom)
        
        tuya_toggle_layout = QHBoxLayout()
        self.btn_tuya_toggle = QPushButton("▼ Smart Plug (Tuya)" if self.tuya_expanded else "▶ Smart Plug (Tuya)")
        self.btn_tuya_toggle.setObjectName("btn_tuya_toggle")
        self.btn_tuya_toggle.clicked.connect(self.toggle_tuya_container)
        tuya_toggle_layout.addStretch()
        tuya_toggle_layout.addWidget(self.btn_tuya_toggle)
        tuya_toggle_layout.addStretch()
        form_layout.addRow(tuya_toggle_layout)
        
        self.tuya_container = QWidget()
        tuya_form = QFormLayout(self.tuya_container)
        tuya_form.setContentsMargins(15, 0, 0, 0)
        self.cb_tuya = QCheckBox("Enable API")
        self.le_tuya_region = QLineEdit()
        self.le_tuya_region.setPlaceholderText("eu, us, cn, in")
        self.le_tuya_id = QLineEdit()
        self.le_tuya_id.setPlaceholderText("Client ID")
        self.le_tuya_secret = QLineEdit()
        self.le_tuya_secret.setPlaceholderText("Secret")
        self.le_tuya_secret.setEchoMode(QLineEdit.EchoMode.Password)
        self.le_tuya_device = QLineEdit()
        self.le_tuya_device.setPlaceholderText("Device ID")
        
        tuya_form.addRow(self.cb_tuya)
        tuya_form.addRow(create_lbl("Region:"), self.le_tuya_region)
        tuya_form.addRow(create_lbl("Client ID:"), self.le_tuya_id)
        tuya_form.addRow(create_lbl("Secret:"), self.le_tuya_secret)
        tuya_form.addRow(create_lbl("Device ID:"), self.le_tuya_device)
        self.tuya_container.setVisible(self.tuya_expanded)
        form_layout.addRow(self.tuya_container)
        
        scroll.setWidget(scroll_content)
        set_layout.addWidget(scroll)

        self.btn_save = QPushButton("Save")
        self.btn_save.setObjectName("btn_action")
        self.btn_save.clicked.connect(self.save_settings)
        set_layout.addWidget(self.btn_save)

        self.btn_reset = QPushButton("Reset Defaults")
        self.btn_reset.setObjectName("btn_action")
        self.btn_reset.clicked.connect(lambda: self.reset_to_defaults(False))
        set_layout.addWidget(self.btn_reset)

        self.stack.addWidget(self.set_widget)
        self.stack.hide()
        layout.addWidget(self.stack)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.valueChanged.connect(self.on_animation_step)