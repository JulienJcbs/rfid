import RPi.GPIO as GPIO
import time

# Configurer le mode des broches
GPIO.setmode(GPIO.BCM)

# Définir le numéro de la broche GPIO que vous souhaitez surveiller
BROCHE = 17

# Configurer la broche comme entrée
GPIO.setup(BROCHE, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # Lire l'état de la broche
        if GPIO.input(BROCHE) == GPIO.HIGH:
            print("Signal détecté")
        else:
            print("Pas de signal")
        
        # Attendre un peu avant de vérifier à nouveau
        time.sleep(1)

except KeyboardInterrupt:
    print("Arrêt du programme")

finally:
    # Nettoyer les configurations GPIO
    GPIO.cleanup()
