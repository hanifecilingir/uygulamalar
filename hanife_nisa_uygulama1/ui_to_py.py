#from PyQt4 import uic

from PyQt5 import uic

with open('uydu.py', 'w', encoding="utf-8") as fout:
   uic.compileUi('uydui.ui', fout)