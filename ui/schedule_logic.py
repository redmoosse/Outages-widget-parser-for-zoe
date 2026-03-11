from datetime import datetime, timedelta

class ScheduleMixin:
    def get_custom_off_intervals(self, target_date):
        intervals = []
        target_date_str = target_date.strftime('%Y-%m-%d')
        sched = self.custom_schedules.get(target_date_str, {})
        
        if not sched.get("enabled", False): return intervals
        
        clean_text = sched.get("text", "").replace('–', '-').replace('—', '-').replace('−', '-')
        try:
            for part in clean_text.split(','):
                if '-' in part:
                    start_str, end_str = part.split('-')
                    sh, sm = map(int, start_str.strip().split(':'))
                    eh, em = map(int, end_str.strip().split(':'))
                    start_dt = datetime.combine(target_date, datetime.min.time()).replace(hour=sh, minute=sm)
                    end_dt = datetime.combine(target_date, datetime.min.time()).replace(hour=eh, minute=em)
                    if end_dt <= start_dt: end_dt += timedelta(days=1)
                    intervals.append((start_dt, end_dt))
        except Exception: pass
        return sorted(intervals, key=lambda x: x[0])

    def get_math_off_intervals(self, target_date):
        intervals = []
        current_time = datetime.combine(target_date, datetime.min.time())
        day_end = current_time + timedelta(days=1)
        
        diff = (current_time - self.start_point).total_seconds()
        if diff < 0:
            diff = self.cycle_duration - (abs(diff) % self.cycle_duration)
            if diff == self.cycle_duration: diff = 0
            
        cycle_pos = diff % self.cycle_duration
        
        while current_time < day_end:
            if cycle_pos < self.off_duration:
                remaining_off = self.off_duration - cycle_pos
                next_time = current_time + timedelta(seconds=remaining_off)
                intervals.append((current_time, min(next_time, day_end)))
                current_time = next_time
                cycle_pos = self.off_duration
            else:
                remaining_on = self.cycle_duration - cycle_pos
                next_time = current_time + timedelta(seconds=remaining_on)
                current_time = next_time
                cycle_pos = 0
                
        return intervals

    def get_intervals_for_date(self, target_date):
        target_date_str = target_date.strftime('%Y-%m-%d')
        sched = self.custom_schedules.get(target_date_str, {})
        
        if sched.get("enabled", False) and sched.get("text", "").strip():
            return self.get_custom_off_intervals(target_date)
        elif getattr(self, 'use_math_mode', False):
            return self.get_math_off_intervals(target_date)
        else:
            return []

    def update_live_timer(self):
        now = datetime.now()
        today_date = now.date()
        tomorrow_date = today_date + timedelta(days=1)
        
        intervals_today = self.get_intervals_for_date(today_date)
        intervals_tomorrow = self.get_intervals_for_date(tomorrow_date)
        all_intervals = intervals_today + intervals_tomorrow
        
        current_outage = None
        next_outage = None
        
        for start_dt, end_dt in all_intervals:
            if start_dt <= now < end_dt:
                current_outage = (start_dt, end_dt)
                break
            elif now < start_dt:
                next_outage = (start_dt, end_dt)
                break
                
        if current_outage:
            state = "OFF"
            time_left = (current_outage[1] - now).total_seconds()
        elif next_outage:
            state = "ON"
            time_left = (next_outage[0] - now).total_seconds()
        else:
            state = "No Outages"
            time_left = -1
                
        if self.current_timer_state is not None and self.current_timer_state != state:
            self.log_message(f"State changed to: {state}")
        self.current_timer_state = state
        
        if time_left == -1:
            self.timer_label.hide()
            self.status_label.setText(state)
            self.status_label.setStyleSheet(f"color: #4CAF50; font-weight: 900; font-size: {int(self.font_size * 2.0)}px;")
            self.alerted_time = False
            return
            
        self.timer_label.show()
        if state == "ON" and time_left <= 300:
            if not self.alerted_time:
                self.play_sound("time")
                self.log_message("5 MINUTES UNTIL POWER OFF!")
                self.alerted_time = True
        elif state == "OFF" or time_left > 300:
            self.alerted_time = False

        self.status_label.setStyleSheet(f"color: {'#FF5252' if state == 'OFF' else '#4CAF50'}; font-weight: 900; font-size: {int(self.font_size * 2.0)}px;")
        h, rem = divmod(int(time_left), 3600)
        m, s = divmod(rem, 60)
        self.status_label.setText(state)
        self.timer_label.setText(f"{h:02}:{m:02}:{s:02}")

    def update_daily_schedule(self):
        qdate = self.calendar.selectedDate()
        target_date = datetime(qdate.year(), qdate.month(), qdate.day()).date()
        
        intervals = self.get_intervals_for_date(target_date)
        
        target_date_str = target_date.strftime('%Y-%m-%d')
        sched = self.custom_schedules.get(target_date_str, {})
        is_custom_enabled = sched.get("enabled", False)
        
        schedule_text = f"Outages on {qdate.toString('dd.MM.yyyy')}:\n\n"

        if is_custom_enabled and sched.get("text", "").strip():
            schedule_text += "[CUSTOM]\n"
        elif self.use_math_mode:
            schedule_text += "[AUTO-CALENDAR]\n"

        if not intervals:
            schedule_text += "Light on\n"
        else:
            for start_dt, end_dt in intervals:
                schedule_text += f"[{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}] 🔴 OFF\n"
                    
        self.schedule_display.setText(schedule_text)