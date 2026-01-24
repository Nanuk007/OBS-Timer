' OBS Timer Server - Silent Launcher (runs in background)
' Run this from OBS Scripts section to start timer without console window

Set objShell = CreateObject("WScript.Shell")
strPath = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\"))
objShell.Run "python """ & strPath & "timer.py""", 0, False
