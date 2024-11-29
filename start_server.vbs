Set WShell = CreateObject("WScript.Shell")
WShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WShell.Run "python server.py", 0, False 