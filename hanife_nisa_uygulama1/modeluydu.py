import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QIcon
from uydu import Ui_MainWindow
import sqlite3

conn = sqlite3.connect("uydusql.db")
curs = conn.cursor()

curs.execute('''
    CREATE TABLE IF NOT EXISTS p (
        id INTEGER PRIMARY KEY,
        marka TEXT,
        adet TEXT,
        adet_fiyati TEXT,
        tarih TEXT,
        tur TEXT,
        depolanma_sekli TEXT
    )''')

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Uydu')   #Uygulama Başlığı
        self.label.setPixmap(QPixmap('logo.png'))
        self.setWindowIcon(QIcon('logo.png'))
        self.pushButton.clicked.connect(self.kayit_ekle)
        self.pushButton_4.clicked.connect(self.listele)  # listele butonunu bağla
        
        # QTableWidget üzerinden işlem yap
        self.tableWidget.setColumnCount(7)  # 7 sütunlu bir tablo oluştur
        self.tableWidget.setHorizontalHeaderLabels(['id','Marka', 'Adet', 'Adet Fiyatı', 'Tarih', 'Tür', 'Depolama Şekli'])

        # self.pushButton_2.clicked.connect(self.guncelle)
        self.pushButton_3.clicked.connect(self.sil)
        

    def kayit_ekle(self):
        marka = self.lineEdit.text()
        adet = self.lineEdit_2.text()
        adet_fiyati = self.lineEdit_3.text()
        tarih = self.lineEdit_4.text()
        depolanma_sekli = self.lineEdit_6.text()
        turu = "a"

        if self.radioButton.isChecked():
            turu = 'ithal'
        elif self.radioButton_2.isChecked():
            turu = 'yerel'

        curs.execute('''INSERT INTO p (marka, adet, adet_fiyati, tarih, tur, depolanma_sekli) VALUES (?,?, ?, ?, ?, ?)''',
                    (marka, adet, adet_fiyati, tarih, turu, depolanma_sekli))
        conn.commit()

    def listele(self):
        curs.execute('SELECT * FROM p')
        veriler = curs.fetchall()

        self.tableWidget.setRowCount(len(veriler))  # Satır sayısını ayarla

        for row_num, veri in enumerate(veriler):
            for col_num, deger in enumerate(veri):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(deger)))

    # def guncelle(self):

    #     marka = self.lineEdit.text()
    #     adet = self.lineEdit_2.text()
    #     adet_fiyati = self.lineEdit_3.text()
    #     tarih = self.lineEdit_4.text()
    #     depolanma_sekli = self.lineEdit_6.text()
    #     turu = "a"

    #     if self.radioButton.isChecked():
    #         turu = 'ithal'
    #     elif self.radioButton_2.isChecked():
    #         turu = 'yerel'

    #     secili_hucre = self.tableWidget.currentItem()
    #     yeni_marka = self.marka.tableWidget.text()
    #     yeni_adet = self.adet.text()
    #     yeni_adet_fiyati = self.adet_fiyati.text()
    #     yeni_tarih = self.tarih.text()
    #     yeni_tur = self.tur.text()
    #     yeni_depolanma_sekli = self.depolanma_sekli.text()


    #     if secili_hucre:
            
    #         conn = sqlite3.connect('uydusql.db')
    #         curs= conn.cursor()
    #         secili_id = self.tableWidget.item(secili_hucre.row(), 0).text()
    #         sorgu = "UPDATE p SET marka=?, adet=?, adet_fiyati=?, tarih=?, tur=?, depolanma_sekli=? WHERE id=?"
    #         curs.execute(sorgu, (yeni_marka, yeni_adet, yeni_adet_fiyati, yeni_tarih, yeni_tur, yeni_depolanma_sekli, secili_id))

    #         conn.commit()
            
    def sil(self):

        conn = sqlite3.connect('uydusql.db')
        curs = conn.cursor()

        secili_hucre = self.tableWidget.currentItem()
        if secili_hucre:
            secili_id = self.tableWidget.item(secili_hucre.row(), 0).text()

            sorgu = "DELETE FROM p WHERE id=?"
            curs.execute(sorgu, (secili_id,))

            conn.commit()
            conn.close()
        
            self.listele()


def app():

    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
app()
    
conn.close()
