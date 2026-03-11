# settings.py
import os
import json
from datetime import datetime
from config import CONFIG_FILE

class SettingsMixin:
    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.start_point = datetime.strptime(data.get("start_date", "2026-03-02 12:00:00"), "%Y-%m-%d %H:%M:%S")
                    self.off_hours = data.get("off_hours", self.default_off)
                    self.on_hours = data.get("on_hours", self.default_on)
                    self.opacity_val = data.get("opacity", self.default_opacity)
                    self.font_size = data.get("font_size", self.default_font_size)
                    
                    self.use_math_mode = data.get("use_math_mode", False)
                    
                    self.custom_schedules = data.get("custom_schedules", {})
                    if "custom_text" in data and data.get("custom_enabled") and not self.custom_schedules:
                        today_str = datetime.now().strftime('%Y-%m-%d')
                        self.custom_schedules[today_str] = {"enabled": True, "text": data["custom_text"]}
                    
                    self.text_color = data.get("text_color", "#FFFFFF")
                    self.custom_sound_path = data.get("custom_sound_path", "")
                    self.custom_bg_path = data.get("custom_bg_path", "")
                    self.bg_alert_only = data.get("bg_alert_only", False)
                    
                    self.zoe_queue = data.get("zoe_queue", "1.2")
                    self.auto_update_zoe = data.get("auto_update_zoe", True)
                    self.auto_update_interval = data.get("auto_update_interval", 15)
                    self.tuya_expanded = data.get("tuya_expanded", False)
                    
                    self.pos_x = data.get("pos_x")
                    self.pos_y = data.get("pos_y")
                    self.compact_size = (data.get("compact_w", 300), data.get("compact_h", 160))
                    self.expanded_size = (data.get("expanded_w", 380), data.get("expanded_h", 700))

                    self.tuya_enabled = data.get("tuya_enabled", False)
                    self.tuya_region = data.get("tuya_region", "eu")
                    self.tuya_id = data.get("tuya_id", "")
                    self.tuya_secret = data.get("tuya_secret", "")
                    self.tuya_device = data.get("tuya_device", "")
            except Exception:
                self.reset_to_defaults(load_only=True)
        else:
            self.reset_to_defaults(load_only=True)
        self.update_durations()

    def save_layout(self):
        data = {}
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        
        cx = self.x()
        cy = self.y() + self.height() - self.compact_size[1]
        
        data["pos_x"] = cx
        data["pos_y"] = cy
        data["compact_w"] = self.compact_size[0]
        data["compact_h"] = self.compact_size[1]
        data["expanded_w"] = self.expanded_size[0]
        data["expanded_h"] = self.expanded_size[1]
        
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass

    def save_settings(self):
        self.start_point = self.dt_edit.dateTime().toPyDateTime()
        self.off_hours = self.spin_off.value()
        self.on_hours = self.spin_on.value()
        self.font_size = self.spin_font.value()
        
        self.zoe_queue = self.le_queue.text()
        self.auto_update_zoe = self.cb_auto_zoe.isChecked()
        self.auto_update_interval = self.spin_auto_interval.value()
        
        if hasattr(self, 'cb_bg_alert_only'):
            self.bg_alert_only = self.cb_bg_alert_only.isChecked()
            
        if hasattr(self, 'cb_use_math_mode'):
            self.use_math_mode = self.cb_use_math_mode.isChecked()
        
        if self.auto_update_zoe:
            self.zoe_auto_timer.start(self.auto_update_interval * 60000)
        else:
            self.zoe_auto_timer.stop()
        
        self.tuya_enabled = self.cb_tuya.isChecked()
        self.tuya_region = self.le_tuya_region.text()
        self.tuya_id = self.le_tuya_id.text()
        self.tuya_secret = self.le_tuya_secret.text()
        self.tuya_device = self.le_tuya_device.text()
        
        self.update_durations()
        self.update_styles()
        
        selected_date_str = self.custom_date_edit.date().toString('yyyy-MM-dd')
        self.custom_schedules[selected_date_str] = {
            "enabled": self.cb_custom.isChecked(),
            "text": self.le_custom.text()
        }
        
        cx = self.x()
        cy = self.y() + self.height() - self.compact_size[1]
        
        data = {
            "start_date": self.start_point.strftime("%Y-%m-%d %H:%M:%S"),
            "off_hours": self.off_hours,
            "on_hours": self.on_hours,
            "opacity": self.opacity_val,
            "font_size": self.font_size,
            "use_math_mode": self.use_math_mode,
            "custom_schedules": self.custom_schedules,
            "text_color": self.text_color,
            "custom_sound_path": self.custom_sound_path,
            "custom_bg_path": self.custom_bg_path,
            "bg_alert_only": self.bg_alert_only,
            "zoe_queue": self.zoe_queue,
            "auto_update_zoe": self.auto_update_zoe,
            "auto_update_interval": self.auto_update_interval,
            "tuya_expanded": self.tuya_expanded,
            "tuya_enabled": self.tuya_enabled,
            "tuya_region": self.tuya_region,
            "tuya_id": self.tuya_id,
            "tuya_secret": self.tuya_secret,
            "tuya_device": self.tuya_device,
            "pos_x": cx,
            "pos_y": cy,
            "compact_w": self.compact_size[0],
            "compact_h": self.compact_size[1],
            "expanded_w": self.expanded_size[0],
            "expanded_h": self.expanded_size[1]
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
            
        self.update_daily_schedule()
        self.update_live_timer()
        self.refresh_tuya_stats()

    def reset_to_defaults(self, load_only=False):
        if not hasattr(self, 'pos_x'):
            self.pos_x = None
            self.pos_y = None
            self.compact_size = (300, 160)
            self.expanded_size = (380, 700)
            
        self.start_point = self.default_start
        self.off_hours = self.default_off
        self.on_hours = self.default_on
        self.opacity_val = self.default_opacity
        self.font_size = self.default_font_size
        self.use_math_mode = False
        self.custom_schedules = {}
        self.text_color = "#FFFFFF"
        self.custom_sound_path = ""
        self.custom_bg_path = ""
        self.bg_alert_only = False
        
        self.zoe_queue = "1.2"
        self.auto_update_zoe = True
        self.auto_update_interval = 15
        self.tuya_expanded = False
        
        self.tuya_enabled = False
        self.tuya_region = "eu"
        self.tuya_id = ""
        self.tuya_secret = ""
        self.tuya_device = ""
        
        self.update_durations()
        
        if not load_only:
            self.apply_settings_to_ui()
            self.update_styles()
            self.save_settings()

    def update_durations(self):
        self.off_duration = self.off_hours * 3600
        self.on_duration = self.on_hours * 3600
        self.cycle_duration = self.off_duration + self.on_duration