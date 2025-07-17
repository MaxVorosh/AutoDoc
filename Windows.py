import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from Doc import Doc, DocGroup

import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

class GeneralSettigns(QWidget):
    def __init__(self, names=None, date=None):
        super().__init__()
        self.initUI(names, date)

    def initUI(self, names, date):
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
        if date is not None:
            self.dateEdit.setDate(date)

        self.windowLbl = QLabel(self)
        self.windowLbl.setText("Члены комиссии")
        self.windowLbl.setAlignment(Qt.AlignCenter)
        self.windowLbl.setGeometry(90, 70, widgetX, widgetY)

        self.comissionList = QTextEdit(self)
        self.comissionList.setGeometry(30, 110, 240, 250)
        self.comissionList.setPlaceholderText("Впишите членов комиссии по одному в строке")
        if names is not None:
            self.comissionList.setText('\n'.join(names))

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
        self.setFixedSize(300, 90)
        self.lbl = QLabel(self)
        self.lbl.setGeometry(20, 20, 260, 50)
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

        self.nonPersonReasons = ["представление вице-президента Адвокатской палаты Санкт-Петербурга"]
        self.reason = QComboBox(self)
        self.reason.addItems(["жалоба", "жалоба адвоката",
                              "представление вице-президента Адвокатской палаты Санкт-Петербурга",
                              "представление ГУ МЮ по СПб и ЛО", "обращение судьи"])
        self.reason.setGeometry(20, 100, 260, widgetY)
        self.reason.currentTextChanged.connect(self.reasonChanged)

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

    def reasonChanged(self, text):
        if text in self.nonPersonReasons:
            self.initiator.hide()
            self.addBtn.setGeometry(90, 140, 120, 30)
        else:
            self.initiator.show()
            self.addBtn.setGeometry(210, 140, 70, 30)

    def addDoc(self):
        target = self.targetName.toPlainText()
        reason = self.reason.currentText()
        number = self.number.toPlainText()
        initiator = None
        if reason not in self.nonPersonReasons:
            initiator = self.initiator.toPlainText()
        if target == "":
            self.ew = ErrorWindow("Введите имя адвоката")
            self.ew.show()
            return
        if number == "":
            self.ew = ErrorWindow("Введите реестровый номер")
            self.ew.show()
            return
        if initiator is not None and initiator == "":
            self.ew = ErrorWindow("Введите имя инициатора")
            self.ew.show()
            return
        if initiator is None:
            initiator = ""
        newRecord = "--".join([target, number, reason, initiator])
        currentRecords = self.docs.toPlainText()
        currentRecords += newRecord + "\n"
        self.docs.setText(currentRecords)


    def back(self):
        self.gs = GeneralSettigns(names=self.comissionNames, date=self.date)
        self.gs.show()
        self.close()

    def save(self):
        months = {'Январь': 'января', 'Февраль': 'февраля', 'Март': 'марта', 'Апрель': 'апреля', 'Май': 'мая',
                  'Июнь': 'июня', 'Июль': 'июля', 'Август': 'августа', 'Сентябрь': 'сентября', 'Октябрь': 'октября',
                  'Ноябрь': 'ноября', 'Декабрь': 'декабря'}
        try:
            filename = self.saveName.toPlainText()
            if filename == "":
                self.ew = ErrorWindow("Введите имя сохраняемого файла")
                self.ew.show()
                return
            day, month, year = self.date.strftime("%d %B %Y").split()
            longDate = day + ' ' + months[month] + ' ' + year + " года"
            docs = DocGroup()
            records = self.docs.toPlainText().split('\n')
            records = [record for record in records if record]
            if len(records) == 0:
                self.ew = ErrorWindow("Добавьте дела")
                self.ew.show()
                return
            for i in range(len(records)):
                record = records[i]
                parts = record.split("--")
                if len(parts) != 4:
                    self.ew = ErrorWindow(f"Неверный формат в строке {i + 1}.\nУдалите строку и добавьте данные заново")
                    self.ew.show()
                    return
                target, number, reason, initiator = parts
                if reason in self.nonPersonReasons and initiator != "":
                    self.ew = ErrorWindow("Данная причина не требует ФИО. Следуйте инструкциям в верхней части окна")
                    self.ew.show()
                    return
                for voter in self.comissionNames:
                    docs.addDoc(Doc(longDate, voter, target, number, reason, initiator))
            docs.save(filename)
            self.back()
        except Exception as e:
            self.ew = ErrorWindow("Ошибка при создании файла.\nУбедитесь, что файл с таким названием \nне существует или закрыт")
            self.ew.show()
            return
