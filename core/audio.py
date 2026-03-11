import os
import time
import threading

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def play_alert_sound(custom_sound_path, sound_type, log_signal=None):
    def _play():
        try:
            if custom_sound_path and os.path.exists(custom_sound_path):
                ext = os.path.splitext(custom_sound_path)[1].lower()
                if ext == '.mp3':
                    try:
                        import pygame
                        if not pygame.mixer.get_init():
                            pygame.mixer.init()
                        pygame.mixer.music.load(custom_sound_path)
                        pygame.mixer.music.play()
                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                    except ImportError:
                        if log_signal: log_signal.emit("Error: try, pip install pygame")
                    except Exception as e:
                        if log_signal: log_signal.emit(f"Error MP3: {str(e)}")
                else:
                    import winsound
                    winsound.PlaySound(custom_sound_path, winsound.SND_FILENAME)
            else:
                try:
                    import winsound
                    if sound_type == "voltage":
                        winsound.Beep(2000, 800)
                    elif sound_type == "time":
                        winsound.Beep(1500, 300)
                        time.sleep(0.1)
                        winsound.Beep(1500, 300)
                        time.sleep(0.1)
                        winsound.Beep(1500, 600)
                except Exception:
                    pass
        except Exception as e:
            if log_signal: log_signal.emit(f"Sound playback error: {str(e)}") 
            
    threading.Thread(target=_play, daemon=True).start()