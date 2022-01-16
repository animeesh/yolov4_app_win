import sys
from cx_Freeze import setup, Executable

setup(name="Person detector",
      version='0.1',
      description = "this  app will detect person in realtime",
      executables= [Executable("main.py")]
      )