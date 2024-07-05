# pythonapps
py to exe apps

to create exe from ipynb, use the following commands:
```bash
jupyter nbconvert --to script name-of-app.ipynb
python -m nuitka --onefile --enable-plugin=pyside6 name-of-app.py
```

## PDF splitter
* Load PDF with pypdf and export selected pages without bloating the PDF size.