import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class GeneralSettigns(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        widgetX = 120
        widgetY = 30

        self.setWindowTitle("AutoDoc")
        self.setFixedSize(300, 480)

        self.dateLbl = QLabel(self)
        self.dateLbl.setText("Дата голосования")
        self.dateLbl.setAlignment(Qt.AlignCenter)
        self.dateLbl.setGeometry(20, 20, widgetX, widgetY)

        self.dateEdit = QDateEdit(self)
        self.dateEdit.setGeometry(160, 20, widgetX, widgetY)
        self.dateEdit.setDate(datetime.datetime.now())

        self.windowLbl = QLabel(self)
        self.windowLbl.setText("Члены комиссии")
        self.windowLbl.setAlignment(Qt.AlignCenter)
        self.windowLbl.setGeometry(90, 70, widgetX, widgetY)

        self.comissionList = QTextEdit(self)
        self.comissionList.setGeometry(30, 110, 240, 250)
        self.comissionList.setPlaceholderText("Впишите членов комиссии по одному в строке")

        self.fileLbl = QLabel(self)
        self.fileLbl.setText("Загрузить файл")
        self.fileLbl.setGeometry(20, 380, widgetX, widgetY)
        self.fileLbl.setAlignment(Qt.AlignCenter)

        self.fileBtn = QPushButton(self)
        self.fileBtn.setText("Загрузить")
        self.fileBtn.clicked.connect(self.uploadFile)
        self.fileBtn.setGeometry(160, 380, widgetX, widgetY)

        self.continueBtn = QPushButton(self)
        self.continueBtn.clicked.connect(self.proceed)
        self.continueBtn.setText("Продолжить")
        self.continueBtn.setGeometry(90, 430, widgetX, widgetY)

    def uploadFile(self):
        names = self.comissionList.toPlainText().split('\n')
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Список членов комиссии", "", "Text Files (*.txt)", options=options)
        if filename == "":
            return
        f = open(filename, "r", encoding="utf-8")
        addedNames = f.readlines()
        f.close()
        names += addedNames
        names = list(filter(lambda name: name, map(lambda name: name.strip(), names)))
        self.comissionList.setText('\n'.join(names))

    def proceed(self):
        names = self.comissionList.toPlainText().split('\n')
        names = list(filter(lambda name: name, map(lambda name: name.strip(), names)))
        date = self.dateEdit.date().toPyDate()
        if len(names) == 0:
            self.ew = ErrorWindow("Выберите членов комиссии")
            self.ew.show()
            return
        self.ds = DocumentSettings(date, names)
        self.ds.show()
        self.close()


class ErrorWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Ошибка")
        self.setFixedSize(300, 70)
        self.lbl = QLabel(self)
        self.lbl.setGeometry(20, 20, 260, 30)
        self.lbl.setText(self.text)
        self.lbl.setAlignment(Qt.AlignCenter)


class DocumentSettings(QWidget):
    def __init__(self, date, names):
        super().__init__()
        self.date = date
        self.comissionNames = names
        self.initUI()

    def initUI(self):
        widgetX = 120
        bigX = 170
        smallX = 70
        widgetY = 30

        self.setWindowTitle("AutoDoc")
        self.setFixedSize(300, 480)

        self.targetLbl = QLabel(self)
        self.targetLbl.setText("Производство в отношении адвоката")
        self.targetLbl.setGeometry(20, 20, 260, widgetY)

        self.targetName = QTextEdit(self)
        self.targetName.setPlaceholderText("ФИО")
        self.targetName.setGeometry(20, 60, bigX, widgetY)

        self.number = QTextEdit(self)
        self.number.setPlaceholderText("Номер")
        self.number.setGeometry(210, 60, smallX, widgetY)

        self.reason = QComboBox(self)
        self.reason.addItems(["жалоба", "жалоба адвоката",
                              "представление вице-президента Адвокатской палаты Санкт-Петербурга",
                              "представление ГУ МЮ по СПб и ЛО", "обращение судьи"])
        self.reason.setGeometry(20, 100, 260, widgetY)

        self.initiator = QTextEdit(self)
        self.initiator.setPlaceholderText("ФИО")
        self.initiator.setGeometry(20, 140, bigX, widgetY)

        self.addBtn = QPushButton(self)
        self.addBtn.setText("Добавить")
        self.addBtn.setGeometry(210, 140, smallX, widgetY)
        self.addBtn.clicked.connect(self.addDoc)

        self.docs = QTextEdit(self)
        self.docs.setPlaceholderText(
            "Используйте поле для корректировки и удаления данных. Добавляйте данные через форму выше"
        )
        self.docs.setGeometry(20, 190, 260, 170)

        self.saveName = QTextEdit(self)
        self.saveName.setPlaceholderText("Имя документа")
        self.saveName.setGeometry(20, 380, widgetX, widgetY)

        self.saveBtn = QPushButton(self)
        self.saveBtn.setText("Сохранить")
        self.saveBtn.setGeometry(160, 380, widgetX, widgetY)
        self.saveBtn.clicked.connect(self.save)

        self.backBtn = QPushButton(self)
        self.backBtn.setText("Назад")
        self.backBtn.setGeometry(90, 430, widgetX, widgetY)
        self.backBtn.clicked.connect(self.back)

    def addDoc(self):
        pass

    def back(self):
        pass

    def save(self):
        pass

