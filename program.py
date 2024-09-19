from gpiozero import Button
from signal import pause

# Définir la broche GPIO que vous souhaitez surveiller
broche = Button(17)

def signal_detecte():
    print("Signal détecté")

# Attacher une fonction de rappel pour détecter les changements
broche.when_pressed = signal_detecte

# Attendre que l'utilisateur interrompe le programme
pause()
