from form_add_event_UI import Ui_Dialog
from schedule_class import Event, Busy

from PyQt5.QtWidgets import QMainWindow, QApplication
from form_day_UI import Ui_MainWindow

import sys


class Main_Window(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.busy = Busy()
		self.busy.load()
		self.click_calendar()


	def run_menu_hand_add_item(self):
		date = date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
		ev = Event("Встреча", date, "09:00")
		self.show_form_add_event("Добавить событие", ev, self.busy)

	def show_form_add_event(self, action, event, busy):
		self.form = Ui_Dialog(action, event, busy, parent = self)
		self.form.show()
		print("Диалоговое окно")
		self.click_calendar()

	def click_calendar(self):
		user_day = self.calendarWidget.selectedDate()
		events = self.busy.filter_day(user_day)
		self.add_events(events)

	def click_tableWidget(self):
		time = self.tableWidget.currentRow() + 9
		date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")
		self.show_form_add_event("Добавить событие", Event("Встреча", date, str(time) + ":00"), self.busy)


App = QApplication(sys.argv)
window = Main_Window()
window.show()
sys.exit(App.exec())
