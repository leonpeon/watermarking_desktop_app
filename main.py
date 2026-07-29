from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
from tkinter import simpledialog
import os

# Shows the image on the left screen if clicked on.
def image_select(image_name):
    if image_name == "start":
        file_name = os.path.join("images", os.listdir("images")[0])
        image = Image.open(file_name)
    else:
        file_name = os.path.join("images", image_name.replace("_thumbnail", ""))
        image = Image.open(file_name)

    # Adjusts image size
    new_width = 300
    aspect_ratio = image.height / image.width
    new_height = int(new_width * aspect_ratio)

    # Displays image on left side
    side_image_file = ImageTk.PhotoImage(image.resize((new_width, new_height), Image.Resampling.LANCZOS))
    side_image.image = side_image_file
    side_image.file_path = file_name
    side_image.configure(image=side_image_file)
    side_image.pack(padx=50)

# Adds a watermark onto a selected photo and saves it to the corresponding folder
def watermark(img, watermark_text):
    image = Image.open(img).convert("RGBA")
    font_size = int(image.width // 20)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", font_size)

    draw.text(xy=(0 + image.width // 10, image.height - image.height // 5),
              text=f"© {watermark_text}",
              font=font,
              fill=(255, 255, 255, 200),
              stroke_width=2,
              stroke_fill="grey"
              )

    # Saves image to "watermarked_images" folder
    file = os.path.splitext(os.path.basename(img))[0]
    end_folder = os.path.join("watermarked_images", file + "_watermark.jpg")
    image.convert("RGB").save(end_folder, "JPEG")
    show_final_image(end_folder)

# Asks user for what their watermark should be
def customise_watermark():
    user_text = simpledialog.askstring("Watermark", "Enter your watermark text: ")
    image = side_image.file_path
    print(image)
    watermark(image, user_text)

# Displays processed image to the user
def show_final_image(image):
    final_img_window = tk.Toplevel(window)
    final_img_window.title("Watermarked Image")

    final_image = Image.open(image)

    final_image.thumbnail((600, 600))

    photo = ImageTk.PhotoImage(final_image)

    label = tk.Label(final_img_window, image=photo)
    label.image = photo
    label.pack()

# Creates thumbnails for all images in the images file.
for image in os.listdir("images"):
    image_path = os.path.join("images", image)
    file_name = os.path.splitext(image)[0]
    end_folder = os.path.join("thumbnails", file_name + "_thumbnail.jpg")
    if os.path.exists(end_folder):
        pass
    else:
        try:
            with Image.open(image_path) as im:
                im.thumbnail((100,100))
                im.save(end_folder, "JPEG")
        except OSError:
            print("Cannot create thumbnail for", image)
        print(image)

# Creating the window
window = tk.Tk()
window.title("Watermark App")

window_width = 960
window_height = 550
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2 - 30

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Creating the frames
left_frame = tk.LabelFrame(window, text="Image Preview", height=700, width=240, padx=20, pady=5)
left_frame.grid(column=0, row=0, rowspan=2, padx=20)
left_frame.grid_propagate(False)

right_frame = tk.LabelFrame(window, text="Image Select", height=440, width=440, padx=10, pady=10)
right_frame.grid(column=1, row=0)
right_frame.grid_propagate(False)

button_frame = tk.Frame(window)
button_frame.grid(column=1, row=2)

# "Select Image" button
button = tk.Button(button_frame, text="Select Image", width=15, command=customise_watermark)
button.pack(pady=20, ipadx=40)

# LEFT FRAME
side_image = tk.Label(left_frame)
side_image.pack(padx=50)
image_select("start")

# RIGHT FRAME
canvas = tk.Canvas(right_frame, background="pink", height=400, width=400)
canvas.pack()

# mouse wheel scrolling
def mousewheel(event):
    top, bottom = canvas.yview()
    delta = -int(event.delta/60)

    if delta < 0 and top <= 0:
        return
    if delta > 0 and bottom >= 1:
        return

    canvas.yview_scroll(delta, "units")

canvas.bind("<MouseWheel>", mousewheel)

# scrollbar
scrollbar = tk.Scrollbar(right_frame, relief="raised", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.place(relx=1, rely=0, relheight=1, anchor="ne")

# Frame inside canvas
image_frame = tk.Frame(canvas, background="pink")
image_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window(
    (0, 0),
    window=image_frame,
    anchor="nw"
)

# Loops through images and turns them into buttons
label_list = []
for thumbnail in os.listdir("thumbnails"):
    file = os.path.join("thumbnails", thumbnail)

    img_obj = ImageTk.PhotoImage(Image.open(file))

    label = tk.Button(image_frame, image=img_obj, command=lambda thumbnail=thumbnail: image_select(thumbnail))
    label.image = img_obj
    label_list.append(label)

# Sorts the images into rows and columns of three
column = 0
row = 0
for img in label_list:
    img.grid(column=column, row=row, pady=5, padx=5)
    column += 1
    if column == 3:
        row += 1
        column = 0

window.mainloop()