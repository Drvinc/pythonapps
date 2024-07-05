# pythonapps
py to exe apps

to create a single executable file exe from ipynb, use the following commands:
```bash
jupyter nbconvert --to script name-of-app.ipynb 
python -m nuitka --onefile --enable-plugin=pyside6 --windows-icon-from-ico=appicon.ico --windows-console-mode=disable name-of-app.py
```

* Nuitka 2.3.11
* Python 3.12

## PDF splitter
* Load PDF with pypdf and export selected pages without bloating the PDF size. Simple drag-and-drop UI.