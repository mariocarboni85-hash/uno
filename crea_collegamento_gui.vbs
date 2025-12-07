Set oWS = WScript.CreateObject("WScript.Shell")
sDesktop = oWS.SpecialFolders("Desktop")
sLinkFile = sDesktop & "\Avvia SuperAgent GUI.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "c:\Users\user\Desktop\m\SuperAgent\Avvia_SuperAgent_GUI.bat"
oLink.WorkingDirectory = "c:\Users\user\Desktop\m\SuperAgent"
oLink.WindowStyle = 1
oLink.Description = "Avvia la GUI di SuperAgent"
oLink.Save