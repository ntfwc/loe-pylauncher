@echo off
REM Add standard Python 3 install paths to the PATH
set PATH=%UserProfile%\AppData\Local\Programs\Python\Python31\;%UserProfile%\AppData\Local\Programs\Python\Python31-31\;C:\Python31;%UserProfile%\AppData\Local\Programs\Python\Python32\;%UserProfile%\AppData\Local\Programs\Python\Python32-32\;C:\Python32;%UserProfile%\AppData\Local\Programs\Python\Python33\;%UserProfile%\AppData\Local\Programs\Python\Python33-32\;C:\Python33;%UserProfile%\AppData\Local\Programs\Python\Python34\;%UserProfile%\AppData\Local\Programs\Python\Python34-32\;C:\Python34;%UserProfile%\AppData\Local\Programs\Python\Python35\;%UserProfile%\AppData\Local\Programs\Python\Python35-32\;C:\Python35;%UserProfile%\AppData\Local\Programs\Python\Python36\;%UserProfile%\AppData\Local\Programs\Python\Python36-32\;C:\Python36;%UserProfile%\AppData\Local\Programs\Python\Python37\;%UserProfile%\AppData\Local\Programs\Python\Python37-31\;C:\Python37;%UserProfile%\AppData\Local\Programs\Python\Python38\;%UserProfile%\AppData\Local\Programs\Python\Python38-31\;C:\Python38;%PATH%

for %%X in (pythonw.exe) do (set FOUND=%%~$PATH:X)
if defined FOUND (
	echo Found Python, running...
	start "" pythonw launcher.py
) else (
	echo Failed to find Python
	echo If you have not done so yet, please install Python 3 from:
	echo https://www.python.org/downloads/
	echo If you have, and you installed Python 3 in a non-standard location, please add that location to your PATH. Alternatively, you can add it in this script if you don't want to do it system wide.
	pause
)