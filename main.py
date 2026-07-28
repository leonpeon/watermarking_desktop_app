from PIL import Image
import tkinter as tk
import os

for image in os.listdir("images"):
    print(image)

window = tk.Tk()

window.title("Watermark App")

window_width = 900
window_height = 550
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2 - 30

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.mainloop()

