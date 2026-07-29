from PIL import Image, ImageTk
import tkinter as tk
import os


# Creates thumbnails for all images in the images file.
for image in os.listdir("images"):
    image_path = os.path.join("images", image)
    file_name = os.path.splitext(image)[0]
    end_folder = os.path.join("thumbnails", file_name + "_thumbnail.jpg")
    if os.path.exists("thumbnails"):
        pass
    else:
        try:
            with Image.open(image_path) as im:
                im.thumbnail((100,100))
                im.save(end_folder, "JPEG")
        except OSError:
            print("Cannot create thumbnail for", image)
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

#FRAMES
left_frame = tk.LabelFrame(window, text="Image Preview", padx=20, pady=20)
left_frame.pack(side="left", padx=40)

right_frame = tk.LabelFrame(window, text="Image Select", padx=10, pady=10)
right_frame.pack(side="right", padx=40)

# IMPROVE UI FOR APP: Have the left frame show the image selected, 
# and the right frame show the available images that can be processed

# LEFT FRAME
file_name = os.path.join("images", os.listdir("images")[0])
image = Image.open(file_name)

new_width = 300
aspect_ratio = image.height / image.width
new_height = int(new_width * aspect_ratio)

side_image_file = ImageTk.PhotoImage(image.resize((new_width, new_height), Image.Resampling.LANCZOS))
side_image = tk.Label(left_frame, image=side_image_file)
side_image.pack(padx=50)


# RIGHT FRAME

label_list = []
for thumbnail in os.listdir("thumbnails"):
    file = os.path.join("thumbnails", thumbnail)

    img_obj = ImageTk.PhotoImage(Image.open(file))

    label = tk.Label(right_frame, image=img_obj)
    label.image = img_obj
    label_list.append(label)

column = 0
row = 0
for img in label_list:
    img.grid(column=column, row=row)
    column += 1
    if column == 5:
        row += 1
        column = 0


# scrollbar = Scrollbar(window, orient="vertical", command=canvas.yview)

window.mainloop()