# main.py

import XInput                    # Importa la librería para interactuar con controles Xbox en Windows
import pystray                   # Importa la librería para crear íconos en la bandeja del sistema
from PIL import Image, ImageDraw # Importa PIL para crear imágenes de los íconos
import threading                 # Importa threading para ejecutar tareas en segundo plano
import time                      # Importa time para manejar pausas y temporizadores

class XboxBatteryTrayWindows:
    def __init__(self):
        self.icon = None         # Inicializa el atributo para el ícono de la bandeja
        self.running = True      # Bandera para controlar el bucle de actualización
        self.battery_icons = {   # Diccionario con los íconos según el nivel de batería
            "Full": self.create_icon(100),    # Ícono para batería llena
            "Medium": self.create_icon(65),   # Ícono para batería media
            "Low": self.create_icon(30),      # Ícono para batería baja
            "Empty": self.create_icon(5),     # Ícono para batería vacía
            "Error": self.create_icon(0, error=True) # Ícono para error
        }
        
        # Configurar el menú de la bandeja con una opción para salir
        menu = pystray.Menu(
            pystray.MenuItem("Salir", self.on_quit)
        )
        
        # Crear el ícono de la bandeja con el ícono de batería llena y el menú
        self.icon = pystray.Icon(
            "xbox_battery_tray",                 # Nombre interno del ícono
            icon=self.battery_icons["Full"],      # Imagen inicial del ícono
            title="Batería Xbox: Conectando...",  # Texto inicial del tooltip
            menu=menu                            # Menú contextual
        )
        
        # Iniciar un hilo para actualizar el estado de la batería periódicamente
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True          # El hilo se cierra al cerrar la app
        self.update_thread.start()                # Inicia el hilo

    def create_icon(self, percent, error=False):
        # Crea un ícono dinámico según el porcentaje de batería o error
        image = Image.new('RGBA', (32, 32), (0, 0, 0, 0)) # Imagen transparente de 32x32
        dc = ImageDraw.Draw(image)                        # Permite dibujar sobre la imagen
        
        if error:
            dc.rectangle((0, 0, 31, 31), fill="red")      # Fondo rojo para error
            dc.text((8, 8), "!", fill="white")            # Signo de exclamación blanco
        else:
            dc.rectangle((0, 24, 31, 31), fill="white")   # Base blanca de la batería
            dc.rectangle((2, 26, 29, 29), fill="black")   # Marco negro de la batería
            dc.rectangle((2, 26, 2 + int(25 * percent/100), 29), fill="white") # Nivel de batería
        
        return image                                      # Devuelve la imagen creada

    def get_battery_status(self):
        try:
            controllers = XInput.get_connected()          # Obtiene los controles conectados
            if not controllers:
                return "Error", "Control no conectado"    # Si no hay control, devuelve error
            
            battery_type, battery_level = XInput.get_battery_information(0) # Info de batería del control 0
            return battery_level.name, f"Batería: {battery_level.name}"     # Devuelve nivel y texto
        except Exception as e:
            return "Error", str(e)                        # Si hay error, devuelve mensaje de error

    def update_loop(self):
        while self.running:                               # Bucle mientras la app esté activa
            level, tooltip = self.get_battery_status()    # Obtiene nivel y texto de batería
            
            if self.icon:
                self.icon.title = tooltip                 # Actualiza el tooltip del ícono
                self.icon.icon = self.battery_icons.get(level, self.battery_icons["Error"]) # Actualiza el ícono
            
            time.sleep(3)                                 # Espera 3 segundos antes de actualizar de nuevo

    def on_quit(self, icon, item):
        self.running = False                              # Detiene el bucle de actualización
        self.icon.stop()                                  # Detiene el ícono de la bandeja
        print("Aplicación cerrada correctamente")         # Mensaje en consola

    def run(self):
        self.icon.run()                                   # Inicia el ícono de la bandeja (bloqueante)

if __name__ == "__main__":
    # Espera 2 segundos para asegurar que XInput esté listo
    time.sleep(2)
    
    # Crea la aplicación y la ejecuta
    app = XboxBatteryTrayWindows()
    app.run()
