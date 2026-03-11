import re
import requests
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from PyQt6.QtCore import QObject, pyqtSignal

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WorkerSignals(QObject):
    log = pyqtSignal(str)
    success = pyqtSignal(str, str, bool, int)
    fail = pyqtSignal(str, bool, int)

def run_zoe_parser(queue, silent, fetch_id, signals):
    if not silent: signals.log.emit(f"Running the parser for: {queue}")
    try:
        urls = [
            "https://www.zoe.com.ua/графіки-погодинних-стабілізаційних/",
            "https://www.zoe.com.ua/outage",
            "https://www.zoe.com.ua/"
        ]
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept-Language": "uk-UA,uk;q=0.9"}
        ukr_months = {'січня': 1, 'лютого': 2, 'березня': 3, 'квітня': 4, 'травня': 5, 'червня': 6, 'липня': 7, 'серпня': 8, 'вересня': 9, 'жовтня': 10, 'листопада': 11, 'грудня': 12}
        date_pattern = re.compile(r'(?i)(\d{1,2})\s+(січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)')
        
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        valid_dates = [today, tomorrow]
        
        parsed_schedules = {today: [], tomorrow: []}
        first_date_mention_line = {}
        found_any_data = False

        for url in urls:
            if not silent: signals.log.emit(f"Checking url: {url}")
            try:
                r = requests.get(url, headers=headers, timeout=10, verify=False)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    lines = soup.get_text(separator='\n', strip=True).split('\n')
                    
                    current_date_block = None
                    
                    for line_idx, line in enumerate(lines):
                        line = line.strip()
                        if not line: continue
                        
                        match = date_pattern.search(line)
                        if match:
                            d = int(match.group(1))
                            m_str = match.group(2).lower()
                            m = ukr_months[m_str]
                            y = today.year
                            if m == 1 and today.month == 12: y += 1 
                            line_date = datetime(y, m, d).date()
                            
                            if line_date in valid_dates:
                                if line_date not in first_date_mention_line:
                                    first_date_mention_line[line_date] = line_idx
                                    if not silent: signals.log.emit(f"Reading the latest schedule on: {line_date.strftime('%Y-%m-%d')}")
                                
                                if line_idx - first_date_mention_line[line_date] > 50:
                                    current_date_block = None
                                else:
                                    current_date_block = line_date
                                    found_any_data = True
                            else:
                                current_date_block = None 
                        
                        if current_date_block is not None:
                            if re.search(rf'^{re.escape(queue)}\s*[:\-]', line) or re.search(rf'\b{re.escape(queue)}\b\s*[:\-]', line):
                                matches = re.finditer(r'([0-2]?[0-9]:[0-5][0-9])\s*[-–—]\s*([0-2]?[0-9]:[0-5][0-9])', line)
                                found_in_line = False
                                for m in matches:
                                    interval_str = f"{m.group(1)}-{m.group(2)}"
                                    if interval_str not in parsed_schedules[current_date_block]:
                                        parsed_schedules[current_date_block].append(interval_str)
                                        found_in_line = True
                                        
                    if found_any_data: 
                        break 
            except Exception: continue 
        
        def merge_strings(interval_list):
            if not interval_list: return ""
            raw = []
            for s in interval_list:
                try:
                    start_s, end_s = s.split('-')
                    sh, sm = map(int, start_s.split(':'))
                    eh, em = map(int, end_s.split(':'))
                    start_dt = datetime.combine(today, datetime.min.time()).replace(hour=sh, minute=sm)
                    end_dt = datetime.combine(today, datetime.min.time()).replace(hour=eh, minute=em)
                    if end_dt <= start_dt: end_dt += timedelta(days=1)
                    raw.append((start_dt, end_dt))
                except Exception: pass
            if not raw: return ""
            
            raw.sort(key=lambda x: x[0])
            merged = [raw[0]]
            for curr in raw[1:]:
                prev = merged[-1]
                if curr[0] <= prev[1]:
                    merged[-1] = (prev[0], max(prev[1], curr[1]))
                else:
                    merged.append(curr)
            return ", ".join([f"{m[0].strftime('%H:%M')}-{m[1].strftime('%H:%M')}" for m in merged])

        emitted_non_silent = False
        
        if today in first_date_mention_line:
            res_today = merge_strings(parsed_schedules[today])
            signals.success.emit(today.strftime('%Y-%m-%d'), res_today, silent, fetch_id)
            emitted_non_silent = True
            
        if tomorrow in first_date_mention_line:
            res_tomorrow = merge_strings(parsed_schedules[tomorrow])
            force_silent = True if emitted_non_silent else silent
            signals.success.emit(tomorrow.strftime('%Y-%m-%d'), res_tomorrow, force_silent, fetch_id)
            emitted_non_silent = True

        if not emitted_non_silent:
            signals.fail.emit(f"Outages for {queue} not fount.", silent, fetch_id)
            
    except Exception as e:
        if not silent:
            signals.log.emit(f"Error: {str(e)}")
            signals.fail.emit("Connection interrupted.", silent, fetch_id)