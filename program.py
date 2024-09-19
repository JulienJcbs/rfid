from gpiozero import Button
from signal import pause

broche = Button(17)

def signal_detecte():
    print("Signal détecté")

broche.when_pressed = signal_detecte

pause()