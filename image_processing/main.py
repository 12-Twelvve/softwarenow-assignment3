import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fake PS Edits")
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self.root.configure(bg="#f4f6f8")

        self.image = None
        self.processed_image = None

        self.setup_ui()

    def setup_ui(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg="#2c3e50", width=280)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Main display
        self.display_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.display_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.image_label = tk.Label(self.display_frame, bg="#ecf0f1")
        self.image_label.pack(expand=True)

        # Title
        tk.Label(
            sidebar,
            text="Edits",
            bg="#2c3e50",
            fg="black",
            font=("Helvetica", 18, "bold"),
        ).pack(pady=20)

        # Sections
        self.create_section(sidebar, "FILE")
        self.create_button(sidebar, "Load Image", self.load_image)

        self.create_section(sidebar, "BASIC")
        self.create_button(sidebar, "Grayscale", self.grayscale)
        self.create_button(sidebar, "Blur", self.blur)
        self.create_button(sidebar, "Edge Detection", self.edge)

        self.create_section(sidebar, "ADJUST")
        self.brightness = self.create_slider(
            sidebar, "Brightness", -100, 100, self.adjust_brightness
        )
        self.contrast = self.create_slider(
            sidebar, "Contrast", 1, 30, self.adjust_contrast
        )

        self.create_section(sidebar, "TRANSFORM")
        self.create_button(sidebar, "Rotate 90°", lambda: self.rotate(90))
        self.create_button(sidebar, "Rotate 180°", lambda: self.rotate(180))
        self.create_button(sidebar, "Rotate 270°", lambda: self.rotate(270))
        self.create_button(sidebar, "Flip Horizontal", lambda: self.flip(1))
        self.create_button(sidebar, "Flip Vertical", lambda: self.flip(0))

        self.create_section(sidebar, "OTHER")
        self.create_button(sidebar, "Resize 50%", self.resize)
        self.create_button(sidebar, "Reset", self.reset)

    def create_section(self, parent, text):
        tk.Label(
            parent,
            text=text,
            bg="#2c3e50",
            fg="#bdc3c7",
            font=("Helvetica", 10, "bold"),
        ).pack(anchor="w", padx=20, pady=(20, 5))

    def create_button(self, parent, text, command):
        tk.Button(
            parent,
            text=text,
            command=command,
            bg="#34495e",
            fg="black",
            activebackground="#1abc9c",
            relief="flat",
            font=("Helvetica", 11),
            height=2,
        ).pack(fill="x", padx=20, pady=5)

    def create_slider(self, parent, label, frm, to, command):
        tk.Label(parent, text=label, bg="#2c3e50", fg="black").pack(
            padx=20, pady=(10, 0)
        )
        slider = tk.Scale(
            parent,
            from_=frm,
            to=to,
            orient=tk.HORIZONTAL,
            bg="#2c3e50",
            fg="black",
            troughcolor="#7f8c8d",
            highlightthickness=0,
            command=command,
        )
        slider.pack(fill="x", padx=20)
        return slider

    def load_image(self):
        path = filedialog.askopenfilename()
        if path:
            self.image = cv2.imread(path)
            self.processed_image = self.image.copy()
            self.show_image(self.image)

    def show_image(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img.thumbnail((750, 550))
        img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img)
        self.image_label.image = img

    def grayscale(self):
        gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        self.processed_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        self.show_image(self.processed_image)

    def blur(self):
        self.processed_image = cv2.GaussianBlur(self.processed_image, (9, 9), 0)
        self.show_image(self.processed_image)

    def edge(self):
        gray = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        self.processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        self.show_image(self.processed_image)

    def adjust_brightness(self, val):
        self.processed_image = cv2.convertScaleAbs(self.image, alpha=1, beta=int(val))
        self.show_image(self.processed_image)

    def adjust_contrast(self, val):
        alpha = int(val) / 10
        self.processed_image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=0)
        self.show_image(self.processed_image)

    def rotate(self, angle):
        if angle == 90:
            self.processed_image = cv2.rotate(
                self.processed_image, cv2.ROTATE_90_CLOCKWISE
            )
        elif angle == 180:
            self.processed_image = cv2.rotate(self.processed_image, cv2.ROTATE_180)
        else:
            self.processed_image = cv2.rotate(
                self.processed_image, cv2.ROTATE_90_COUNTERCLOCKWISE
            )
        self.show_image(self.processed_image)

    def flip(self, direction):
        self.processed_image = cv2.flip(self.processed_image, direction)
        self.show_image(self.processed_image)

    def resize(self):
        self.processed_image = cv2.resize(self.processed_image, None, fx=0.5, fy=0.5)
        self.show_image(self.processed_image)

    def reset(self):
        self.processed_image = self.image.copy()
        self.show_image(self.processed_image)


# ---------------- Run ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
