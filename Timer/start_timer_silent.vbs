Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd /c """ & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\start_timer.bat""", 0, False
