import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--name=main',
    '--onefile',
    '--collect-data=Cython',
    '--hidden-import=Cython.Compiler.Main',
    '--exclude-module=paddleocr',
    '--exclude-module=pydensecrf',
])
