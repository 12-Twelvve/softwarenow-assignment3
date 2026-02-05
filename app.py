import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

# --- Class 1: Image Processor (OpenCV Logic) ---
class ImageProcessor:
    def __init__(self):
        self.image = None 

    def load_image(self, path):
        self.image = cv2.imread(path)
        return self.image is not None

    def get_rgb_image(self, img=None):
        target = img if img is not None else self.image
        return cv2.cvtColor(target, cv2.COLOR_BGR2RGB)

    # --- Filtering Methods ---
    def apply_grayscale(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    def apply_blur(self, img, intensity):
        k_size = (intensity * 2 + 1)
        return cv2.GaussianBlur(img, (k_size, k_size), 0)

    def apply_canny(self, img):
        edges = cv2.Canny(img, 100, 200)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # --- Brightness & Contrast Method ---
    def adjust_image(self, img, brightness, contrast):
        """
        brightness: integer (-100 to 100)
        contrast: float (0.5 to 3.0)
        """
        # cv2.convertScaleAbs handles the clipping to [0, 255] automatically
        return cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

    def rotate_image(self, img, angle):
        if angle == 90: return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        if angle == 180: return cv2.rotate(img, cv2.ROTATE_180)
        if angle == 270: return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return img

    def flip_image(self, img, mode):
        return cv2.flip(img, mode)

# --- Class 2: History Manager ---
class HistoryManager:
    def __init__(self):
        self.undo_stack = []
        self.redo_stack = []

    def push(self, state):
        self.undo_stack.append(state.copy())
        self.redo_stack.clear()
        if len(self.undo_stack) > 15: self.undo_stack.pop(0)

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            return self.undo_stack[-1].copy()
        return None

    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.undo_stack.append(state)
            return state
        return None

# --- Class 3: Main Application (GUI) ---
class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HIT137 Assignment - OpenCV Image Processor")
        self.root.geometry("1100x850")

        self.processor = ImageProcessor()
        self.history = HistoryManager()
        
        self.current_img = None
        self.file_path = ""

        self.create_widgets()

    def create_widgets(self):
        # Menu Bar
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo_action)
        edit_menu.add_command(label="Redo", command=self.redo_action)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        self.root.config(menu=menubar)

        # UI Panels
        self.left_panel = tk.Frame(self.root, width=280, bg="#eeeeee", padx=15, pady=10)
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.canvas = tk.Canvas(self.root, bg="#222222")
        self.canvas.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # --- Controls ---
        tk.Label(self.left_panel, text="Filters", font=("Arial", 11, "bold"), bg="#eeeeee").pack(pady=5)
        tk.Button(self.left_panel, text="Grayscale", width=20, command=self.apply_gray).pack(pady=2)
        tk.Button(self.left_panel, text="Canny Edge", width=20, command=self.apply_canny).pack(pady=2)

        # Brightness Slider
        tk.Label(self.left_panel, text="Brightness", bg="#eeeeee").pack(pady=(15, 0))
        self.bright_slider = tk.Scale(self.left_panel, from_=-100, to=100, orient=tk.HORIZONTAL)
        self.bright_slider.set(0)
        self.bright_slider.pack(fill=tk.X)

        # Contrast Slider
        tk.Label(self.left_panel, text="Contrast (Scale)", bg="#eeeeee").pack(pady=(10, 0))
        self.contrast_slider = tk.Scale(self.left_panel, from_=0.5, to=3.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill=tk.X)

        tk.Button(self.left_panel, text="Apply Adjustments", bg="#4CAF50", fg="white", 
                  command=self.apply_bc).pack(pady=10)

        tk.Label(self.left_panel, text="Blur Intensity", bg="#eeeeee").pack(pady=(10,0))
        self.blur_slider = tk.Scale(self.left_panel, from_=0, to=10, orient=tk.HORIZONTAL)
        self.blur_slider.pack(fill=tk.X)
        tk.Button(self.left_panel, text="Apply Blur", command=self.apply_blur).pack(pady=2)

        # Transformations
        tk.Label(self.left_panel, text="Transform", font=("Arial", 11, "bold"), bg="#eeeeee").pack(pady=(20, 5))
        tk.Button(self.left_panel, text="Rotate 90°", width=20, command=lambda: self.rotate(90)).pack(pady=2)
        tk.Button(self.left_panel, text="Flip Horizontal", width=20, command=lambda: self.flip(1)).pack(pady=2)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)

    # --- Functions ---
    def open_file(self):
        path = filedialog.askopenfilename()
        if path:
            if self.processor.load_image(path):
                self.file_path = path
                self.current_img = self.processor.image.copy()
                self.history.push(self.current_img)
                self.display_image()
                self.update_status()

    def save_file(self):
        if self.current_img is not None:
            path = filedialog.asksaveasfilename(defaultextension=".png")
            if path: cv2.imwrite(path, self.current_img)

    def apply_bc(self):
        """Apply Brightness and Contrast together."""
        if self.current_img is not None:
            b = self.bright_slider.get()
            c = self.contrast_slider.get()
            self.current_img = self.processor.adjust_image(self.current_img, b, c)
            self.history.push(self.current_img)
            self.display_image()

    def apply_gray(self):
        if self.current_img is not None:
            self.current_img = self.processor.apply_grayscale(self.current_img)
            self.history.push(self.current_img)
            self.display_image()

    def apply_blur(self):
        if self.current_img is not None:
            self.current_img = self.processor.apply_blur(self.current_img, self.blur_slider.get())
            self.history.push(self.current_img)
            self.display_image()

    def apply_canny(self):
        if self.current_img is not None:
            self.current_img = self.processor.apply_canny(self.current_img)
            self.history.push(self.current_img)
            self.display_image()

    def rotate(self, angle):
        if self.current_img is not None:
            self.current_img = self.processor.rotate_image(self.current_img, angle)
            self.history.push(self.current_img)
            self.display_image()

    def flip(self, mode):
        if self.current_img is not None:
            self.current_img = self.processor.flip_image(self.current_img, mode)
            self.history.push(self.current_img)
            self.display_image()

    def undo_action(self):
        res = self.history.undo()
        if res is not None:
            self.current_img = res
            self.display_image()

    def redo_action(self):
        res = self.history.redo()
        if res is not None:
            self.current_img = res
            self.display_image()

    def display_image(self):
        if self.current_img is not None:
            rgb = self.processor.get_rgb_image(self.current_img)
            img_pil = Image.fromarray(rgb)
            img_pil.thumbnail((800, 600))
            self.tk_img = ImageTk.PhotoImage(image=img_pil)
            self.canvas.delete("all")
            self.canvas.create_image(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, image=self.tk_img)

    def update_status(self):
        h, w, _ = self.current_img.shape
        self.status_var.set(f"Loaded: {self.file_path} | Size: {w}x{h}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()