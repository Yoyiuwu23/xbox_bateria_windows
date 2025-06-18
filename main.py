# xbox_battery_tray_win.py
import XInput
import pystray
from PIL import Image, ImageDraw
import threading
import time

class XboxBatteryTrayWindows:
    def __init__(self):
        self.icon = None
        self.running = True
        self.battery_icons = {
            "Full": self.create_icon(100),
            "Medium": self.create_icon(65),
            "Low": self.create_icon(30),
            "Empty": self.create_icon(5),
            "Error": self.create_icon(0, error=True)
        }
        
        # Configurar el menú
        menu = pystray.Menu(
            pystray.MenuItem("Salir", self.on_quit)
        )
        
        # Iniciar el ícono en la bandeja
        self.icon = pystray.Icon(
            "xbox_battery_tray",
            icon=self.battery_icons["Full"],
            title="Batería Xbox: Conectando...",
            menu=menu
        )
        
        # Iniciar hilo de actualización
        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def create_icon(self, percent, error=False):
        # Crear ícono dinámico con Pillow
        image = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        
        if error:
            dc.rectangle((0, 0, 31, 31), fill="red")
            dc.text((8, 8), "!", fill="white")
        else:
            dc.rectangle((0, 24, 31, 31), fill="white")
            dc.rectangle((2, 26, 29, 29), fill="black")
            dc.rectangle((2, 26, 2 + int(25 * percent/100), 29), fill="white")
            
        return image

    def get_battery_status(self):
        try:
            controllers = XInput.get_connected()
            if not controllers:
                return "Error", "Control no conectado"
            
            battery_type, battery_level = XInput.get_battery_information(0)
            return battery_level.name, f"Batería: {battery_level.name}"
        except Exception as e:
            return "Error", str(e)

    def update_loop(self):
        while self.running:
            level, tooltip = self.get_battery_status()
            
            if self.icon:
                self.icon.title = tooltip
                self.icon.icon = self.battery_icons.get(level, self.battery_icons["Error"])
            
            time.sleep(3)

    def on_quit(self, icon, item):
        self.running = False
        self.icon.stop()
        print("Aplicación cerrada correctamente")

    def run(self):
        self.icon.run()

if __name__ == "__main__":
    # Esperar a que XInput esté listo
    time.sleep(2)
    
    # Iniciar aplicación
    app = XboxBatteryTrayWindows()
    app.run()
