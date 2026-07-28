from PIL import Image
import tkinter as tk
import os


# Creates thumbnails for all images in the images file.
for image in os.listdir("images"):
    end_image = os.path.splitext(image)[0] + ".thumbnail"
    if image != end_image:
        try:
            with Image.open(image) as im:
                im.thumbnail((50,50))
                im.save(end_image, "JPEG")
        except OSError:
            print("Cannot create thumbnail for ", image)
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

canvas = tk.Canvas(window)
# scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)

window.mainloop()

