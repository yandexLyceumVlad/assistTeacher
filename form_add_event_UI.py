from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QDate
from PyQt5.QtWidgets import QWidget
import schedule_class


class Ui_Dialog(QWidget):

    def __init__(self, action, event, busy, parent=None):
        super().__init__()
        self.setupUi()
        self.parentttt = parent
        #запомнить редактируем или создаем новое событие
        self.action = action
        self.setWindowTitle(self.action)
        self.busy = busy
        self.my_event = event
        #заполнить поля формы
        self.LineEditEvent.setText(event.name)
        self.TimeEdit.setTime(QTime.fromString(event.time, "hh:mm"))
        date = QDate.fromString(event.date, "yyyy-MM-dd")
        self.calendarWidget.setSelectedDate(date)
        self.calendarWidget.showSelectedDate()
        self.TimeEditDuration.setTime(QtCore.QTime(event.duration // 60, event.duration % 60))
        self.LineEditLink.setText(event.link)
        self.LineEditComment.setText(event.comment)

    def setupUi(self):
        #self.setModal(True)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowSystemMenuHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setObjectName("Dialog")
        self.setFixedSize(597, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)

        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(self)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 30, 251, 161))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.Label = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label.setObjectName("Label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.Label)
        self.LineEditEvent = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.LineEditEvent.setObjectName("LineEditEvent")
        self.LineEditEvent.setFocus()
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.LineEditEvent)
        self.Label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_2.setObjectName("Label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Label_2)
        self.TimeEdit = QtWidgets.QTimeEdit(self.formLayoutWidget)
        self.TimeEdit.setObjectName("TimeEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.TimeEdit)
        self.Label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_3.setObjectName("Label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Label_3)
        self.TimeEditDuration = QtWidgets.QTimeEdit(self.formLayoutWidget)
        self.TimeEditDuration.setObjectName("TimeEditDuration")
        self.TimeEditDuration.setTime(QtCore.QTime(1,0))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.TimeEditDuration)
        self.Label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_4.setObjectName("Label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Label_4)
        self.LineEditLink = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.LineEditLink.setObjectName("LineEditLink")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.LineEditLink)
        self.Label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.Label_5.setObjectName("Label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.Label_5)
        self.LineEditComment = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.LineEditComment.setObjectName("LineEditComment")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.LineEditComment)
        self.calendarWidget = QtWidgets.QCalendarWidget(self)
        self.calendarWidget.setGeometry(QtCore.QRect(270, 10, 312, 183))
        self.calendarWidget.setObjectName("calendarWidget")

        self.retranslateUi(self)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        print("end_form")


    def accept(self):
        if self.LineEditEvent.text() != "":
            date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
            time = self.TimeEdit.text()
            duration = schedule_class.Event.encode_time(self.TimeEditDuration.text())
            link = self.LineEditLink.text()
            new_event = schedule_class.Event(self.LineEditEvent.text(), date, time, duration, link, self.LineEditComment.text())
            if self.action == "Добавить событие":
                self.busy.add_event(new_event)
            else:
                self.busy.del_event(self.my_event)
                self.busy.add_event(new_event)
                #print(new_event)
            self.busy.save()
            self.parentttt.click_calendar()
            self.close()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText("Задайте название события")
            msg.setWindowTitle("Error")
            msg.exec_()

    def reject(self):
        self.close()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Добавить событие"))
        self.Label.setText(_translate("Dialog", "Событие"))
        self.Label_2.setText(_translate("Dialog", "Время"))
        self.Label_3.setText(_translate("Dialog", "Продолжительность"))
        self.Label_4.setText(_translate("Dialog", "Ссылка"))
        self.Label_5.setText(_translate("Dialog", "Коммент"))
