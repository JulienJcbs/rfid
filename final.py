import tkinter as tk
from tkinter import Label
import cv2
from PIL import Image, ImageTk
import threading
from gpiozero import Button

class VideoPlayer:
    def __init__(self, window, video_source1, video_source2):
        self.window = window
        self.window.title("Video Player")

        # Initialisation des vidéos
        self.video_source1 = video_source1
        self.video_source2 = video_source2
        self.current_video = self.video_source1

        # Ouvrir la première vidéo
        self.vid = cv2.VideoCapture(self.current_video)

        # Créer un widget Canvas pour afficher la vidéo
        self.canvas = tk.Canvas(window, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Passer en mode plein écran
        self.window.attributes('-fullscreen', True)
        self.window.bind("<Escape>", self.quit_fullscreen)  # Sortie du plein écran avec la touche Échap

        # Démarrer la lecture de la vidéo dans un thread séparé
        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.start()

        # Détecteur de signal GPIO
        self.broche = Button(17)
        self.broche.when_pressed = self.signal_detecte

    def quit_fullscreen(self, event=None):
        self.window.attributes('-fullscreen', False)
        self.window.quit()

    def update(self):
        while True:
            ret, frame = self.vid.read()
            if not ret:
                if self.current_video == self.video_source1:
                    self.current_video = self.video_source2
                else:
                    self.current_video = self.video_source1
                self.vid.release()
                self.vid = cv2.VideoCapture(self.current_video)
                continue

            # Convertir l'image de BGR (OpenCV) à RGB (Pillow)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Obtenir les dimensions du canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Redimensionner la frame pour correspondre aux dimensions du canvas
            img = Image.fromarray(frame)
            img = img.resize((canvas_width, canvas_height), Image.ANTIALIAS)
            
            # Convertir l'image en format compatible avec Tkinter
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.image = imgtk
            
            # Pause pour éviter de surcharger le processeur
            self.window.update_idletasks()
            self.window.update()
    
    def signal_detecte(self):
        # Fonction appelée lorsqu'un signal est détecté
        print("Signal détecté")
        if self.current_video == self.video_source1:
            self.current_video = self.video_source2
        else:
            self.current_video = self.video_source1
        self.vid.release()
        self.vid = cv2.VideoCapture(self.current_video)

    def __del__(self):
        self.vid.release()

# Créer une fenêtre Tkinter
root = tk.Tk()
video_source1 = "./assets/video1.mp4"  # Remplacez par le chemin vers votre première vidéo
video_source2 = "./assets/video2.mp4"  # Remplacez par le chemin vers votre deuxième vidéo
player = VideoPlayer(root, video_source1, video_source2)

# Démarrer la boucle principale Tkinter
root.mainloop()