# Xbox Battery Tray Indicator for Windows

Monitor de batería para control de Xbox en la bandeja del sistema de Windows, desarrollado en Python y apoyado en librerías de terceros para la integración con el sistema y la obtención de información del hardware.

---

## Características

- **Muestra el nivel de batería del control Xbox en la bandeja del sistema de Windows**.
- **Iconos generados dinámicamente según el estado de la batería**.
- **Actualización automática cada pocos segundos**.
- **Interfaz simple y ligera**.
- **Uso de código de terceros para integración con la bandeja y consulta de XInput**.

---

## Código de terceros utilizado

Este proyecto se apoya en varias librerías y utilidades de terceros para su funcionamiento:


| Librería/Utilidad | Descripción | Licencia |
| :-- | :-- | :-- |
| `XInput-Python` | Acceso a la API XInput de Windows para controles Xbox | AGPLv3 |
| `pystray` | Icono y menú en la bandeja del sistema | LGPLv3 |
| `Pillow` | Generación de iconos gráficos en tiempo real | MIT |

Estas dependencias son fundamentales para la integración gráfica y la consulta del estado de batería en sistemas Windows.

---

## Requisitos

- **Windows 10/11**
- **Python 3.7 o superior**
- **Paquetes de Python:**

```
XInput-Python
pystray
Pillow
```


---

## Instalación

1. Instala las dependencias:

```
pip install -r requirements.txt
```

2. Descarga el código y guárdalo, por ejemplo, como `xbox_battery_tray_win.py`.
3. Ejecuta la aplicación:

```
python xbox_battery_tray_win.py
```


---

## Personalización

Puedes personalizar los iconos generados modificando el método `create_icon` en el código fuente para adaptar el aspecto visual a tu gusto.

---

## Licencia

Este proyecto está bajo la licencia GNU General Public License v3.0 o posterior. Consulta el archivo [LICENSE](LICENSE) para más detalles. El uso de librerías de terceros implica que debes respetar también sus respectivas licencias.

---

**¡Disfruta monitoreando la batería de tu control Xbox directamente desde Windows, aprovechando el poder del software libre y las librerías de terceros!**
