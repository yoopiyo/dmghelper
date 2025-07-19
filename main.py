# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: main.py
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import threading
from mss import mss
import cv2
import numpy as np
import os
import time
from datetime import datetime, timedelta
import uuid
import hashlib
import pyperclip
import sys
import webbrowser
from pynput import keyboard as pynput_keyboard
import tempfile
import requests
from email.utils import parsedate_to_datetime
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
import logging
SECRET_SALT = 'B3uYNLlpQYQPw1EwNY43B-xnx'
KEY_FILE = 'activation.key'
MAX_DAYS = 14
os.makedirs('logs') if not os.path.exists('logs') else os.path
log_filename = f"logs/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s', handlers=[logging.FileHandler(log_filename, encoding='utf-8'), logging.StreamHandler()])

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_warn(message):
    logging.warning(message)
CURRENT_VERSION = 'v1.11'
UPDATE_URL = 'https://raw.githubusercontent.com/my0kul/DHelper/main/version.txt'
UPDATE_DOWNLOAD_URL = 'https://raw.githubusercontent.com/my0kul/DHelper/main/DemorganHelper.exe'

def auto_update_check():
    time.sleep(2)
    latest_version = check_for_update()
    if latest_version:
        answer = messagebox.askyesno('Обновление', f'Доступна новая версия: {latest_version}\nХотите обновиться сейчас?')
        if answer:
            download_and_install_update(UPDATE_DOWNLOAD_URL)
        return None

def check_for_update():
    try:
        response = requests.get(UPDATE_URL, timeout=5)
        if response.status_code == 200:
            latest_version = response.text.strip()
            log_info(f'Текущая версия: {CURRENT_VERSION}, последняя: {latest_version}')
            if latest_version!= CURRENT_VERSION:
                return latest_version
    except Exception as e:
        log_error(f'Не удалось проверить обновления: {e}')
        return None

def get_current_executable_path():
    """Возвращает путь к текущему исполняемому файлу (работает как для .py, так и для .exe)"""  # inserted
    if getattr(sys, 'frozen', False):
        return sys.executable

def download_and_install_update(download_url):
    try:
        current_exe_path = get_current_executable_path()
        app_dir = os.path.dirname(current_exe_path)
        update_path = os.path.join(app_dir, 'update.tmp')
        final_exe_path = os.path.join(app_dir, 'DemorganHelper.exe')
        log_info(f'Загрузка обновления: {download_url}')
        response = requests.get(download_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(update_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    pass  # postinserted
                else:  # inserted
                    f.write(chunk)
                log_info('Обновление загружено.')
                updater_script = os.path.join(tempfile.gettempdir(), 'updater.bat')
                with open(updater_script, 'w') as bat_file:
                    bat_file.write(f'\n@echo off\ntimeout /t 2 >nul\n\nset \"CURRENT_APP={current_exe_path}\"\nset \"UPDATE_FILE={update_path}\"\nset \"FINAL_EXE={final_exe_path}\"\n\necho Checking administrator privileges...\nnet session >nul 2>&1\nif %errorLevel% NEQ 0 (\n    echo Error: Administrator privileges are required.\n    pause\n    exit /b 1\n)\n\necho Stopping DemorganHelper.exe processes...\ntaskkill /im DemorganHelper.exe /f >nul 2>&1\n\necho Moving update to destination...\nif exist \"%FINAL_EXE%\" del /F /Q \"%FINAL_EXE%\"\nmove /Y \"%UPDATE_FILE%\" \"%FINAL_EXE%\"\n\nif exist \"%FINAL_EXE%\" (\n    echo Update successfully installed.\n    start \"\" \"{final_exe_path}\"\n) else (\n    echo Failed to move the file.\n    exit /b 1\n)\n\nexit\n')
                    log_info('Запуск скрипта обновления...')
                    ctypes.windll.shell32.ShellExecuteW(None, 'runas', 'cmd.exe', f'/c {updater_script}', None, 1)
                    sys.exit()
    except Exception as e:
        log_error(f'Ошибка при установке обновления: {e}')
        messagebox.showerror('Ошибка', f'Не удалось установить обновление:\n{str(e)}')

def get_internet_time():
    try:
        response = requests.get('https://www.google.com', timeout=5)
        date_header = response.headers.get('Date')
        if date_header:
            dt = parsedate_to_datetime(date_header)
            return dt.timestamp()
    except Exception as e:
        log_error(f'Не удалось получить время: {e}')
        return None

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

def get_device_id():
    return str(uuid.getnode())

def generate_activation_key(device_id):
    return hashlib.sha256((device_id + SECRET_SALT).encode()).hexdigest()[:16]

def check_key(key):
    device_id = get_device_id()
    expected_key = generate_activation_key(device_id)
    return key.strip() == expected_key

def copy_device_id():
    device_id = get_device_id()
    pyperclip.copy(device_id)
    messagebox.showinfo('Копирование', 'ID устройства скопирован в буфер обмена.')

def on_activate(entry_key, window):
    input_key = entry_key.get().strip()
    if not input_key:
        messagebox.showwarning('Ошибка', 'Введите ключ активации.')
    return None

def is_activation_valid():
    decrypted = load_decrypted_key()
    if not decrypted:
        pass  # postinserted
    return False

def xor_encrypt(data, key):
    return ''.join((chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data)))

def save_encrypted_key(plain_text, password='B3uYNLlpQYQPw1EwNY43B-xnx'):
    encrypted = xor_encrypt(plain_text, password)
    with open(KEY_FILE, 'w') as f:
        f.write(encrypted)

def load_decrypted_key(password='B3uYNLlpQYQPw1EwNY43B-xnx'):
    if not os.path.exists(KEY_FILE):
        pass  # postinserted
    return None

def show_activation_window():
    window = tk.Tk()
    window.title('Активация DHelper')
    window.geometry('440x270')
    window.configure(bg='#2E2E2E')
    window.resizable(False, False)
    window.eval('tk::PlaceWindow . center')
    icon_path = resource_path('assets/icon.ico')
    if os.path.exists(icon_path):
        window.iconbitmap(icon_path)
    title = tk.Label(window, text='DHelper', font=('Segoe UI', 16, 'bold'), bg='#2E2E2E', fg='#00BFFF')
    title.pack(pady=15)
    desc = tk.Label(window, text='Введите ключ активации или свяжитесь с разработчиком (ds: myokul).', font=('Segoe UI', 10), bg='#2E2E2E', fg='#FFFFFF')
    desc.pack(pady=(0, 10))
    dev_id_frame = tk.Frame(window, bg='#2E2E2E')
    dev_id_frame.pack(pady=5)
    dev_id_label = tk.Label(dev_id_frame, text='Ваш ID:', font=('Segoe UI', 10), bg='#2E2E2E', fg='#AAAAAA')
    dev_id_label.pack(side=tk.LEFT, padx=5)
    dev_id_text = tk.Entry(dev_id_frame, width=20, font=('Consolas', 10), bd=1, relief='flat')
    dev_id_text.insert(0, get_device_id())
    dev_id_text.config(state='readonly')
    dev_id_text.pack(side=tk.LEFT)
    copy_btn = tk.Button(dev_id_frame, text='Копировать', command=copy_device_id, width=10, bg='#00BFFF', fg='black', bd=0)
    copy_btn.pack(side=tk.LEFT, padx=5)
    key_label = tk.Label(window, text='Ключ активации:', font=('Segoe UI', 10), bg='#2E2E2E', fg='#FFFFFF')
    key_label.pack(pady=(10, 0))
    key_entry = tk.Entry(window, width=30, font=('Consolas', 12), justify='center')
    key_entry.focus_set()
    key_entry.pack(pady=5)

    def show_context_menu(event, entry):
        context_menu = tk.Menu(entry, tearoff=0)
        context_menu.add_command(label='Вставить', command=lambda: paste_text(entry))
        try:
            context_menu.tk_popup(x=event.x_root, y=event.y_root)
            context_menu.grab_release()
        except Exception as e:
            log_error(f'Ошибка в show_context_menu: {e}')



    def on_paste(event):
        try:
            clipboard = window.clipboard_get()
            key_entry.insert(tk.INSERT, clipboard)
            return 'break'
        except tk.TclError:
            return 'break'
    key_entry.bind('<Control-v>', on_paste)
    key_entry.bind('<Button-3>', lambda e: show_context_menu(e, key_entry))
    key_entry.bind('<Button-2>', lambda e: show_context_menu(e, key_entry))
    activate_btn = tk.Button(window, text='Активировать', command=lambda: on_activate(key_entry, window), width=20, bg='#00BFFF', fg='black', bd=0, font=('Segoe UI', 10, 'bold'))
    activate_btn.pack(pady=15)
    window.mainloop()

def paste_text(entry):
    try:
        clipboard = entry.clipboard_get()
        entry.insert(tk.INSERT, clipboard)
    except tk.TclError:
        return None

def start_main_app():
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
TIMER_NAMES = {'Туалет': 35, 'Полы': 55, 'Сортировка': 75, 'Бургеры': 20}
ACTIVATION_DELAYS = {'Туалет': 1.5, 'Полы': 8.0, 'Сортировка': 1.5, 'Бургеры': 1.5}
TEMPLATE_PATHS = {'Туалет': resource_path('assets/toilet.png'), 'Полы': resource_path('assets/floor.png'), 'Сортировка': resource_path('assets/sort.png'), 'Бургеры': resource_path('assets/food.png')}
THRESHOLD = 0.23
SAVE_DEBUG = False
ANALYSIS_SIZE = 400
BG_COLOR = '#1E1E1E'
TEXT_COLOR = '#FFFFFF'
ACCENT_COLOR = '#917AFF'
WARNING_COLOR = '#FFD600'
SUCCESS_COLOR = '#00FFAA'
FONT_FAMILY = 'Segoe UI'

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f'DHelper by myokul [{CURRENT_VERSION}]')
        self.root.geometry('320x170')
        self.root.configure(bg=BG_COLOR)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)
        self.subscription_label = tk.Label(root, text='', font=tkfont.Font(family=FONT_FAMILY, size=9), bg=BG_COLOR, fg='#AAAAAA')
        self.subscription_label.pack(pady=(10, 0))
        self.root.attributes('-topmost', True)
        self.default_font = tkfont.Font(family=FONT_FAMILY, size=11)
        self.bold_font = tkfont.Font(family=FONT_FAMILY, size=13, weight='bold')
        icon_path = resource_path('assets/icon.ico')
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        self.status_label = tk.Label(root, text='Обновляется...', font=self.default_font, bg=BG_COLOR, fg=WARNING_COLOR, pady=2)
        self.status_label.pack(pady=(0, 2))
        frame = tk.Frame(root, bg=BG_COLOR)
        label = tk.Label(frame, text='Ожидание', font=self.default_font, width=10, anchor='w', bg=BG_COLOR, fg=TEXT_COLOR)
        timer_label = tk.Label(frame, text='00:00', font=self.bold_font, width=6, bg=BG_COLOR, fg=SUCCESS_COLOR)
        label.pack(side=tk.LEFT, padx=10)
        timer_label.pack(side=tk.LEFT)
        frame.pack(pady=2)
        self.task_timer = {'name': label, 'label': timer_label, 'thread': None, 'running': False}
        self.reset_button = tk.Button(root, text='Сброс таймера', command=self.set_timer_stopped, width=20, bg=WARNING_COLOR, fg='black', bd=0, font=('Segoe UI', 10, 'bold'))
        self.reset_button.pack(pady=5)
        self.discord_button = tk.Button(root, text='Перейти в Discord', command=self.open_discord, width=20, bg=ACCENT_COLOR, fg='white', bd=0, font=('Segoe UI', 10, 'bold'))
        self.discord_button.pack(pady=5)
        self.update_main_timer()
        self.start_keyboard_listener()

    def start_food_sequence(self):
        if self.task_timer['running']:
            pass  # postinserted
        return None

    def open_discord(self):
        webbrowser.open_new('https://discord.gg/2t8twWgfZJ')

    def update_subscription_status(self):
        decrypted = load_decrypted_key()
        if not decrypted:
            self.subscription_label.config(text='Подписка не активирована', fg='#FFA500')
        return None

    def start_keyboard_listener(self):
        listener = pynput_keyboard.Listener(on_press=self.on_key_press, daemon=True)
        listener.start()
        log_info('start_keyboard_listener')

    def on_key_press(self, key):
        try:
            if key == pynput_keyboard.Key.up or key == pynput_keyboard.KeyCode(vk=101) or key == pynput_keyboard.KeyCode(vk=69):
                log_info('Физическая клавиша \'E\' нажата')
                self.root.after(0, self.handle_e_key)
            return None
        except Exception as e:
            log_error(f'Ошибка при обработке нажатия клавиши: {e}')
            return None

    def handle_e_key(self):
        for name, delay in ACTIVATION_DELAYS.items():
            self.root.after(int(delay * 1000), lambda n=name: self.check_template_after_delay(n))

    def check_template_after_delay(self, task_name):
        template_path = TEMPLATE_PATHS.get(task_name)
        if not template_path or not os.path.exists(template_path):
            log_error(f'Шаблон не найден: {task_name}')
        return None

    def start_timer(self, name):
        if self.task_timer['running']:
            pass  # postinserted
        return None

    def update_timer_label(self, text):
        """Обновляет текст метки — вызывается в главном потоке"""  # inserted
        self.task_timer['label'].config(text=text)

    def set_timer_stopped(self):
        """Останавливает таймер — вызывается в главном потоке"""  # inserted
        self.task_timer['running'] = False
        self.task_timer['name'].config(text='Ожидание')
        self.task_timer['label'].config(text='00:00')

    def update_main_timer(self):
        threading.Thread(target=self.background_update, daemon=True).start()
        self.root.after(1000, self.update_main_timer)
        self.update_subscription_status()
        self.root.after(6000, self.update_subscription_status)

    def background_update(self):
        internet_time = get_internet_time()
        if internet_time is None:
            self.status_label.config(text='Ошибка сети', fg='#FF5555')
            self.root.after(5000, self.background_update)
        return None

    def update_gui(self, status, color, mins_left, secs_left):
        time_left_str = f'{mins_left} : {secs_left:02d}'
        self.status_label.config(text=f'{status} (до смены: {time_left_str})', fg=color)
        time_left_str = f'{mins_left} : {secs_left:02d}'

def save_debug_image(img, prefix='debug'):
    debug_dir = os.path.join('logs', 'debug')
    os.makedirs(debug_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'debug_{prefix}_{timestamp}.png'
    full_path = os.path.join(debug_dir, filename)
    cv2.imwrite(full_path, img)
    log_info(f'[DEBUG] Сохранён скриншот: {full_path}')

def crop_rect_of_image(input_path, output_path, width=1400, height=750):
    """\nОбрезает центральную прямоугольную область заданных размеров из изображения и сохраняет его.\n\n:param input_path: Путь к исходному изображению (например, \'templates/toilet_full.png\')\n:param output_path: Путь для сохранения обрезанного изображения (например, \'templates/toilet.png\')\n:param width: Ширина прямоугольника для обрезки (по умолчанию 600)\n:param height: Высота прямоугольника для обрезки (по умолчанию 400)\n"""  # inserted
    if not os.path.exists(input_path):
        log_error(f'Исходное изображение не найдено: {input_path}')
    return None

def crop_center_of_image(input_path, output_path, size=400):
    """\nОбрезает центральную квадратную область заданного размера из изображения и сохраняет его.\n\n:param input_path: Путь к исходному изображению (например, \'templates/toilet_full.png\')\n:param output_path: Путь для сохранения обрезанного изображения (например, \'templates/toilet.png\')\n:param size: Размер квадрата для обрезки (по умолчанию 400)\n"""  # inserted
    if not os.path.exists(input_path):
        log_error(f'Исходное изображение не найдено: {input_path}')
    return None
FOOD_COLOR = (56, 201, 245)
COLOR_TOLERANCE = 30

def check_food_color(screen_width, screen_height):
    """\nПроверяет цвет центральной области экрана для шаблона \"food.png\".\n"""  # inserted
    with mss() as sct:
        color_analysis_size = 50
        center_x = screen_width // 2
        center_y = screen_height // 2
        left = center_x - color_analysis_size // 2
        top = center_y - color_analysis_size // 2
        analysis_monitor = {'top': top, 'left': left, 'width': color_analysis_size, 'height': color_analysis_size, 'mon': 1}
        screenshot = sct.grab(analysis_monitor)
        img = np.array(screenshot)
        avg_color = np.mean(img, axis=(0, 1)).astype(int)
        if all((abs(avg_color[i] - FOOD_COLOR[i]) <= COLOR_TOLERANCE for i in range(3))):
            log_info('Цвет в центре экрана соответствует ожидаемому для \'food.png\'')
            pass
        return True

def find_template_on_screen(template_path, threshold=0.65):
    with mss() as sct:
        monitor = sct.monitors[1]
        screen_width = monitor['width']
        screen_height = monitor['height']
        base_width = ANALYSIS_SIZE
        base_height = ANALYSIS_SIZE
        if resource_path('assets/food.png') == template_path:
            base_width = 1400
            base_height = 750
            return check_food_color(screen_width, screen_height)
        
if __name__ == '__main__':
    threading.Thread(target=auto_update_check, daemon=True).start()
    if is_activation_valid():
        root = tk.Tk()
        app = TimerApp(root)
        root.mainloop()