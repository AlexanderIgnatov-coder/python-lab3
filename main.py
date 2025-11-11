import tkinter as tk
from tkinter import ttk
from pygame import mixer
import random


#Константы: общие
WINDOW_WIDTH = 801
WINDOW_HEIGHT = 801

# Константы: генерация ключа
ALPHABET_SIZE = 26
BLOCK_LENGTH = 4
MIN_SUM = 0 + 1 + 2 + 3          # = 6
MAX_SUM = 22 + 23 + 24 + 25      # = 94
MAX_GENERATION_ATTEMPTS = 10000

#Константы: интерфейс
ENTRY_WIDTH = 10
TEXT_FONT = ("Arial", 12)

# Позиции элементов
ENTRY_UP_X, ENTRY_UP_Y = 60, 150
ENTRY_DOWN_X, ENTRY_DOWN_Y = 60, 180
TEXT_OUTPUT_X, TEXT_OUTPUT_Y = 40, 220
GIF_CENTER_X, GIF_CENTER_Y = 500, 250
BUTTON_GIF_X, BUTTON_GIF_Y = 60, 250
BUTTON_GEN_X, BUTTON_GEN_Y = 60, 280

# Константы: анимация
GIF_FRAME_COUNT = 41
GIF_UPDATE_INTERVAL_MS = 100


def key_generation(interval_up, interval_down):
    """Генерирует ключ из трёх 4-буквенных блоков по двум целевым суммам."""
    try:
        target1 = int(interval_up)
        target2 = int(interval_down)
    except (ValueError, TypeError):
        return "Ошибка: введите целые числа"

    if not (MIN_SUM <= target1 <= MAX_SUM) or not (MIN_SUM <= target2 <= MAX_SUM):
        return f"Ошибка: сумма должна быть от {MIN_SUM} до {MAX_SUM}"

    alphabet = [chr(ord('A') + i) for i in range(ALPHABET_SIZE)]
    numbers = list(range(ALPHABET_SIZE))
    valid_targets = [target1, target2]

    def generate_block(target, max_attempts=MAX_GENERATION_ATTEMPTS):
        for _ in range(max_attempts):
            block = random.sample(numbers, BLOCK_LENGTH)
            if sum(block) == target:
                return ''.join(alphabet[i] for i in block)
        return None

    blocks = []
    for target in [target1, target2, random.choice(valid_targets)]:
        block = generate_block(target)
        if block is None:
            return f"Не удалось сгенерировать блок для суммы {target}"
        blocks.append(block)

    return ''.join(blocks)


def load_gif_frames():
    """Загружает кадры GIF один раз и сохраняет в глобальный список."""
    global gif_frames
    if not gif_frames:
        try:
            gif_frames = [
                tk.PhotoImage(file='gifka3.gif', format=f'gif -index {i}')
                for i in range(GIF_FRAME_COUNT)
            ]
        except tk.TclError:
            gif_frames = []


def show_gif():
    global gif_label
    if not gif_frames:
        load_gif_frames()
        if not gif_frames:
            return  # GIF-файл недоступен

    if gif_label is None:
        gif_label = tk.Label(window, bg="white")
        canvas.create_window(GIF_CENTER_X, GIF_CENTER_Y, window=gif_label)

    def update(ind):
        frame = gif_frames[ind]
        gif_label.config(image=frame)
        next_ind = (ind + 1) % len(gif_frames)
        window.after(GIF_UPDATE_INTERVAL_MS, update, next_ind)

    update(0)


def click_button():
    """Генерирует ключ и отображает его на холсте."""
    global text_item_id
    key = key_generation(entr_up.get(), entr_down.get())
    if text_item_id:
        canvas.delete(text_item_id)
    text_item_id = canvas.create_text(
        TEXT_OUTPUT_X, TEXT_OUTPUT_Y,
        anchor='nw',
        text=key,
        fill="black",
        font=TEXT_FONT
    )


# Инициализация GUI
window = tk.Tk()
window.title('lab3')
window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

# Загрузка фона
bg_img = None
try:
    bg_img = tk.PhotoImage(file='bg3.png')
except tk.TclError:
    pass

canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
canvas.pack(fill="both", expand=True)
if bg_img:
    canvas.create_image(0, 0, anchor="nw", image=bg_img)

# Поля ввода
entr_up = tk.Entry(window, width=ENTRY_WIDTH)
entr_down = tk.Entry(window, width=ENTRY_WIDTH)
canvas.create_window(ENTRY_UP_X, ENTRY_UP_Y, anchor='nw', window=entr_up)
canvas.create_window(ENTRY_DOWN_X, ENTRY_DOWN_Y, anchor='nw', window=entr_down)

gif_label = None
gif_frames = []
text_item_id = None

btn_gif = ttk.Button(window, text='Click!!!', command=show_gif)
btn = ttk.Button(window, text="Click for generation", command=click_button)
canvas.create_window(BUTTON_GIF_X, BUTTON_GIF_Y, anchor="nw", window=btn_gif)
canvas.create_window(BUTTON_GEN_X, BUTTON_GEN_Y, anchor="nw", window=btn)

# Фоновая музыка
try:
    mixer.init()
    mixer.music.load('music.mp3')
    mixer.music.play(-1)
except Exception:
    pass  # файл отсутствует — игнорируем


window.mainloop()
