import os
import winshell
from win32com.client import Dispatch

# Percorsi
desktop = winshell.desktop()
shortcut_path = os.path.join(desktop, "SuperAgent.lnk")
target = r"C:\Users\user\Desktop\AvviaSuperAgentGUI.bat"
icon = r"C:\Users\user\Desktop\m\SuperAgent\icon.ico"

shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = target
shortcut.WorkingDirectory = os.path.dirname(target)
shortcut.IconLocation = icon
shortcut.save()
