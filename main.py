import tkinter as tk
from tkinter import ttk
from pygame import mixer
import random

BG_IMAGE_FILE = 'bg3.png'
GIF_FILE = 'gifka3.gif'
MUSIC_FILE = 'music.mp3'

WINDOW_WIDTH = 801
WINDOW_HEIGHT = 801

ALPHABET_SIZE = 26
BLOCK_LENGTH = 4
MIN_SUM = 6        
MAX_SUM = 96    
MAX_GENERATION_ATTEMPTS = 10000

ENTRY_WIDTH = 10
TEXT_FONT = ("Arial", 12)

ENTRY_UP_X, ENTRY_UP_Y = 60, 150
ENTRY_DOWN_X, ENTRY_DOWN_Y = 60, 180
TEXT_OUTPUT_X, TEXT_OUTPUT_Y = 40, 220
GIF_CENTER_X, GIF_CENTER_Y = 500, 250
BUTTON_GIF_X, BUTTON_GIF_Y = 60, 250
BUTTON_GEN_X, BUTTON_GEN_Y = 60, 280

GIF_FRAME_COUNT = 41
GIF_UPDATE_INTERVAL_MS = 100

def key_generation(interval_up, interval_down):
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


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('lab3')
        self.root.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')

        self.canvas = tk.Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.bg_img = None
        try:
            self.bg_img = tk.PhotoImage(file=BG_IMAGE_FILE)
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)
        except tk.TclError:
            pass

        self.entr_up = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.entr_down = tk.Entry(self.root, width=ENTRY_WIDTH)
        self.canvas.create_window(ENTRY_UP_X, ENTRY_UP_Y, anchor='nw', window=self.entr_up)
        self.canvas.create_window(ENTRY_DOWN_X, ENTRY_DOWN_Y, anchor='nw', window=self.entr_down)

        self.text_item_id = None
        self.gif_label = None
        self.gif_frames = []

        btn_gif = ttk.Button(self.root, text='Click!!!', command=self.show_gif)
        btn_gen = ttk.Button(self.root, text="Click for generation", command=self.click_button)
        self.canvas.create_window(BUTTON_GIF_X, BUTTON_GIF_Y, anchor="nw", window=btn_gif)
        self.canvas.create_window(BUTTON_GEN_X, BUTTON_GEN_Y, anchor="nw", window=btn_gen)

        self.init_music()

    def init_music(self):
        try:
            mixer.init()
            mixer.music.load(MUSIC_FILE)
            mixer.music.play(-1)
        except Exception:
            pass  

    def click_button(self):
        key = key_generation(self.entr_up.get(), self.entr_down.get())
        if self.text_item_id:
            self.canvas.delete(self.text_item_id)
        self.text_item_id = self.canvas.create_text(
            TEXT_OUTPUT_X, TEXT_OUTPUT_Y,
            anchor='nw',
            text=key,
            fill="black",
            font=TEXT_FONT
        )

    def load_gif_frames(self):
        if not self.gif_frames:
            try:
                self.gif_frames = [
                    tk.PhotoImage(file=GIF_FILE, format=f'gif -index {i}')
                    for i in range(GIF_FRAME_COUNT)
                ]
            except tk.TclError:
                self.gif_frames = []

    def show_gif(self):
        if not self.gif_frames:
            self.load_gif_frames()
            if not self.gif_frames:
                return

        if self.gif_label is None:
            self.gif_label = tk.Label(self.root, bg="white")
            self.canvas.create_window(GIF_CENTER_X, GIF_CENTER_Y, window=self.gif_label)

        self.update_gif(0)

    def update_gif(self, ind):
        if not self.gif_frames:
            return
        frame = self.gif_frames[ind]
        self.gif_label.config(image=frame)
        next_ind = (ind + 1) % len(self.gif_frames)
        self.root.after(GIF_UPDATE_INTERVAL_MS, self.update_gif, next_ind)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()