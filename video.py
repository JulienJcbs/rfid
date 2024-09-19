import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk
import threading

class VideoPlayer:
    def __init__(self, window, video_source):
        self.window = window
        self.window.title("Video Player")
        
        # Ouvrir la vidéo
        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)
        
        # Créer un widget Label pour afficher la vidéo
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), 
                                height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        
        # Démarrer la lecture de la vidéo dans un thread séparé
        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.start()

    def update(self):
        while True:
            ret, frame = self.vid.read()
            if not ret:
                break
            
            # Convertir l'image de BGR (OpenCV) à RGB (Pillow)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            
            # Convertir l'image en format compatible avec Tkinter
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.image = imgtk
            
            # Pause pour éviter de surcharger le processeur
            self.window.update_idletasks()
            self.window.update()
    
    def __del__(self):
        self.vid.release()

# Créer une fenêtre Tkinter
root = tk.Tk()
video_source = "votre_video.mp4"  # Remplacez par le chemin vers votre vidéo
player = VideoPlayer(root, video_source)

# Démarrer la boucle principale Tkinter
root.mainloop()
