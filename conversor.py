from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image
import pytesseract
import pyperclip
import os
import ctypes

# start tesseract
pytesseract.pytesseract.tesseract_cmd = os.path.join(
    os.path.dirname(__file__), 'Tesseract-OCR', 'tesseract.exe')


# Create a screen

root = Tk()
root.attributes('-fullscreen', True, '-alpha', 0.2)

# create a canvas to draw on screen
canvas = tk.Canvas(root, bg='white')
canvas.pack(fill=tk.BOTH, expand=True)

# close the aplicaton when press Esc


def quit(event=None):
    root.quit()


# sets a list that take 2 coordinates to create a rect and print the content inside
coordinates = []


def rect_erase():
    canvas.delete('all')


def draw_rect():
    global pos_x, pos_y, pos_x2, pos_y2
    rect_erase()
    canvas.create_rectangle(
        coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1], fill='red')


def get_mouse_position(event):
    x, y = event.x, event.y  # get mouse pos
    print(f"x:{x} , y{y}")
    if event and len(coordinates) < 2:
        new_coordinate = (x, y)  # create a tuple using the coordinate
        if new_coordinate not in coordinates:  # check if the coordinate isn't the same
            coordinates.append(new_coordinate)
            if len(coordinates) == 2:
                draw_rect()
            print(coordinates)


def clear_selection(event):  # clear selection
    coordinates.clear()
    rect_erase()

# img functions


def get_digits(img_path):
    try:
        img = Image.open(img_path)
        digits = pytesseract.image_to_string(img)
        pyperclip.copy(digits)
        ctypes.windll.user32.MessageBoxW(
            0, "Texto copiado para o clipboard!", "Informação", 0x40 | 0x1)
    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")


def print_selected_area(event):
    if len(coordinates) == 2:
        # erase the red selector
        rect_erase()
        root.attributes('-alpha', 0)

        # force update root to erase the selector
        root.update()

        try:
            img = ImageGrab.grab(bbox=(
                coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1]))

            dir = 'img'

            if not os.path.exists(dir):
                os.makedirs(dir)

            file_path = os.path.join(dir, 'temp.png')

            img.save(file_path)
        except Exception as e:
            print(e)

        try:
            get_digits(file_path)
        except Exception as e:
            print(f"expt 2 : {e}")
        finally:
            os.remove(file_path)
            quit()

    # binds
root.bind('<Button-1>', get_mouse_position)
root.bind('<Button-3>', clear_selection)
root.bind('<Control-c>', print_selected_area)
root.bind('<Escape>', quit)


root.mainloop()
