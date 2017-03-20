from cx_Freeze import setup, Executable
import sys

executables = [
    Executable("gui.py",base = "Win32GUI"
               )
]


setup(name="jgomas_gui",
      version="0.2",
      description="Interfaz grafica para lanzar agentes",
      executables=executables,
      )