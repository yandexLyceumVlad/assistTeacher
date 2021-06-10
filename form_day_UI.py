from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QMessageBox, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QDialog

import webbrowser

import schedule_class


class Event_Frame(QFrame):
    def __init__(self, parent, table):
        super().__init__(parent)
        self.setGeometry(33, 66, One_Event.widthSlot, 325)
        self.setFrameStyle(QFrame.Box)
        self.table = table
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored))

    def mousePressEvent(self, event):
        index = self.table.indexAt(event.pos())
        self.table.setCurrentCell(index.row(), 0)

class Link_Image_Label(QLabel):
    def __init__(self, link):
        super().__init__()
        self.link = link
        self.setOpenExternalLinks(True)
        self.setMouseTracking(False)
        self.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.setText("")
        self.setPixmap(QtGui.QPixmap("link.png"))
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setFixedSize(24, 24)

    def mousePressEvent(self, e):
        try:
            webbrowser.open(self.link)
        except:
            print(self.event())

class Popup(QDialog):

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name
        self.label = QLabel(self.name, self)

class One_Event(QFrame):
    widthSlot = 280
    # # # ширина слота в одину минуту
    oneMinSlot = (325 - 66) / (10 * 60)

    def __init__(self, event):
        super().__init__()
        self.event = event
        heightSlot = event.duration * One_Event.oneMinSlot
        self.setFixedHeight(heightSlot)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: rgb(2, 116, 205); border-bottom: 1px solid rgb(128, 128, 255);")
        self.setToolTip(event.comment)

        oneEventLayout = QHBoxLayout()
        oneEventLayout.setContentsMargins(0, 0, 0, 0)
        oneEventLayout.setObjectName("oneEventLayout")
        self.setLayout(oneEventLayout)
        oneEventLayout.setSpacing(0)

        labelNameEvent = QLabel()
        labelNameEvent.setToolTipDuration(10)
        labelNameEvent.setObjectName("labelNameEvent")
        labelNameEvent.setAutoFillBackground(True)
        labelNameEvent.setFixedHeight(heightSlot)

        labelNameEvent.setText("  " + event.name)
        labelNameEvent.setStyleSheet("color: white;")

        oneEventLayout.addWidget(labelNameEvent)
        if (event.link.strip()):
            labelLinkImg = Link_Image_Label(event.link)
            oneEventLayout.addWidget(labelLinkImg)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.parent().parent().show_form_add_event("Редактировать событие", self.event, self.parent().parent().busy)
        else:
            print("удаление события")
            self.dlg = QMessageBox()
            self.dlg.show()
            self.dlg.show()
            self.dlg.cancel = self.dlg.addButton("Нет", QMessageBox.AcceptRole)
            self.dlg.setIcon(QMessageBox.Information)
            self.dlg.setWindowTitle("Предупреждение")
            self.dlg.setInformativeText("Удалить событие " + self.event.name + "?")
            btn = self.dlg.exec()
            if self.dlg.clickedButton().text() == "OK":  # + text()
                self.parent().parent().busy.del_event(self.event)
                self.parent().parent().busy.save()
                self.parent().parent().click_calendar()
                print("Событие удалено")


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(315, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(0, 370, 312, 183))
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.clicked.connect(self.click_calendar)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 321, 371))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.tableWidget.setFont(font)

        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(14)
        for i in range(self.tableWidget.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(i, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("событие")
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(280)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(10)
        self.tableWidget.verticalHeader().setDefaultSectionSize(25)
        self.tableWidget.itemSelectionChanged.connect(self.click_tableWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 319, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionAddHand = QtWidgets.QAction(MainWindow)
        self.actionAddHand.setObjectName("actionAddHand")
        self.actionAddHand.triggered.connect(self.run_menu_hand_add_item)

        self.actionAddText = QtWidgets.QAction(MainWindow)
        self.actionAddText.setObjectName("actionAddText")

        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.menu.addAction(self.actionAddHand)
        self.menu.addAction(self.actionAddText)
        self.menu.addAction(self.action_3)
        self.menubar.addAction(self.menu.menuAction())

        # фрейм для отображения событий
        self.panelEvents = QVBoxLayout(self)
        self.panelEvents.setContentsMargins(0, 0, 0, 0)
        self.panelEvents

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Frame для событий втечении дня
        frame = Event_Frame(self, self.tableWidget)
        frame.setLayout(self.panelEvents)

    def add_events(self, events):
        self.clearPanelEvents()
        if len(events) == 0:
            return
        #9:00 - это начало таблицы времен
        begin_event = schedule_class.Event("", "", time="09:00", duration=0)
        for i in range(len(events)):
            self.add_space_widget(begin_event, events[i])
            event_widget = One_Event(events[i])
            self.panelEvents.addWidget(event_widget)
            begin_event = events[i]
        self.panelEvents.setSpacing(0)
        end_event = schedule_class.Event("", "", time="22:00", duration=0)
        self.add_space_widget(begin_event, end_event)

    def clearLayoutEvent(self, eventLayout):
        frame_temp = eventLayout.widget().findChildren(type(QLabel()))
        frame_temp[0].deleteLater()
        if len(frame_temp) > 1:
            frame_temp[1].deleteLater()
        eventLayout.widget().deleteLater()

    def clearPanelEvents(self):
        while self.panelEvents.count():
            child = self.panelEvents.takeAt(0)
            if isinstance(child, QtWidgets.QWidgetItem):
                self.clearLayoutEvent(child)
            self.panelEvents.removeItem(child)


    def add_space_widget(self, begin_event, end_event):
        dt = schedule_class.Event.time_interval(begin_event, end_event)
        heightSlotSpace = int(dt * One_Event.oneMinSlot)
        spacerItem = QSpacerItem(20, heightSlotSpace)
        self.panelEvents.addSpacerItem(spacerItem)
        #print(dt, "пустота = ",heightSlotSpace)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Личный секретарь"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "время"))

        for i in range(1, self.tableWidget.rowCount()):
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("MainWindow", str(8+i)+":00"))

        self.menu.setTitle(_translate("MainWindow", "Добавить событие"))
        self.actionAddHand.setText(_translate("MainWindow", "Руками"))
        self.actionAddText.setText(_translate("MainWindow", "Из текста"))
        self.action_3.setText(_translate("MainWindow", "Из календаря"))

