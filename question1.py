# You will develop a desktop application that demonstrates your understanding of Object-
# Oriented Programming principles, GUI development using Tkinter, and image
# processing using OpenCV.
# Functional Requirements
# 1. Object-Oriented Programming
# Your application must be structured using at least three classes, and demonstrate the
# following OOP concepts: Encapsulation, Constructor, Methods, Class Interaction

class Image:
    def __init__(self, name):
        self.name = name

    def display_info(self):
        print("Image name:", self.name)

class ImageConverter:
    def __init__(self, image):
        self.image = image

    def convert_grayscale(self):
        print("Converting", self.image.name, "to grayscale")
        
class ImageApp:
    def __init__(self):
        self.image = Image("sample.jpg")
        self.converter = ImageConverter(self.image)

    def run(self):
        self.image.display_info()
        self.converter.convert_grayscale()

app = ImageApp()
app.run()
           

