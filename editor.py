import json
import os
import sys
import copy
import time

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Creator(QMainWindow):
	def __init__(self):
		super().__init__()
		self.build_ui()
		self.w = None  # no extra window yet

	def build_ui(self):
		self.setWindowTitle("CrystalStudio Editor")

		self.label = QLabel("No recent projects found...")
		self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

		self.setCentralWidget(self.label)

		toolbar = QToolBar("Toolbar")
		toolbar.setIconSize(QSize(16, 16))
		self.addToolBar(toolbar)

		new_project = QAction("New project", self)
		new_project.setStatusTip("Create a new project")
		new_project.triggered.connect(self.new_project_fnc)
		toolbar.addAction(new_project)

		toolbar.addSeparator()

		open_project = QAction("Open Project", self)
		open_project.setStatusTip("Open a project that is saved")
		open_project.triggered.connect(self.open_project_fnc)
		toolbar.addAction(open_project)

		toolbar.addAction(open_project)

		self.setStatusBar(QStatusBar(self))

		self.setMinimumSize(960, 540)

	def new_project_fnc(self):
		self.np_dlg = QDialog(self)
		self.np_dlg.setWindowTitle("New project")

		layout = QGridLayout(self.np_dlg)
		label = QLabel(self.np_dlg)
		label.setText("Project name:")
		input_name = QLineEdit(self.np_dlg)

		label2 = QLabel(self.np_dlg)
		label2.setText("Authors:")
		input_authors = QLineEdit(self.np_dlg)
		label2_help = QLabel(self.np_dlg)
		label2_help.setText("(seperate by comma)")

		label3 = QLabel(self.np_dlg)
		label3.setText("Out folder:")
		input_out = QLineEdit(self.np_dlg)
		input_out.setText("out/")
		input_out.setDisabled(True)
		checkbox = QCheckBox(self.np_dlg)

		btn = QPushButton(self.np_dlg)
		btn.setText("Create project")
		btn.clicked.connect(lambda: self.create_project(input_name.text(), input_authors.text(), input_out.text()))

		layout.addWidget(label, 0, 0)
		layout.addWidget(input_name, 0, 1)
		layout.addWidget(label2, 1, 0)
		layout.addWidget(input_authors, 1, 1)
		layout.addWidget(label2_help, 1, 2)
		layout.addWidget(label3, 2, 0)
		layout.addWidget(input_out, 2, 1)
		layout.addWidget(checkbox, 2, 2)
		layout.addWidget(btn, 3, 2)

		self.np_dlg.setLayout(layout)

		self.np_dlg.setFixedSize(int(960 / 2), int(540 / 2))

		self.name_label = QLabel(self)
		self.name_label.setText("Name")

		checkbox.toggled.connect(input_out.setEnabled)

		self.np_dlg.exec()

	def open_project_fnc(self):
		print("Coming soon!")

	def create_project(self, name, author, out):
		if name:
			if author:
				if out:
					allow = True
				else:
					allow = False
			else:
				allow = False
		else:
			allow = False

		if allow:
			self.np_dlg.hide()
			# print(name, author, out)
			self.hide()

		try:
			os.mkdir("editor/" + name)
			os.mkdir("editor/" + name + "/" + out)

			if self.w is None:
				self.w = Editor(name, author, out)
			self.w.show()

			self.hide()

		except FileExistsError as err:
			print("ERROR:", err, "| Please pick a different name.")
			sys.exit(1)


class Editor(QWidget):
	def __init__(self, name: str, author: str, out: str):
		super().__init__()

		self.name = name
		self.author = author
		self.out = out
		self.scene = 0

		self.preview = []

		try:
			file = open(f"editor/{name}/save.json", "r")
			self.mem_data = json.load(file)
			file.close()
		except FileNotFoundError:
			file = open(f"editor/{name}/save.json", "w")

			self.mem_data = {
				"info": {"name": name, "authors": author.split(", "), "out": "out/", "editor": {"current_scene": 0}},
				"scenes": [{"title": "Scene 1", "buttons": [["Go to scene 2", 2], ["Go to scene 3", 3]]},
						   {"title": "Scene 2", "buttons": [["Go to scene 1", 1], ["Go to scene 3", 3]]},
						   {"title": "Scene 3", "buttons": [["Go to scene 1", 1], ["Go to scene 2", 2]]}
						   ]
				}

			json.dump(self.mem_data, file)
			file.close()

		self.save_file = open(f"editor/{name}/save.json", "r")

		self.build_ui()

	def build_ui(self):
		self.layout = QGridLayout(self)
		self.layout.setContentsMargins(200, 200, 200, 200)

		self.setLayout(self.layout)

		self.setFixedSize(1920, 1080)
		self.setWindowTitle("CrystalStudio - " + self.name)

		self.labels = []
		self.lists = []
		self.buttons = []
		self.titles = []

		add_scene_btn = QPushButton(self)
		add_scene_btn.setText("+")

		remove_scene_btn = QPushButton(self)
		remove_scene_btn.setText("-")

		build_btn = QPushButton(self)
		build_btn.setText("Build game")

		self.save_btn = QPushButton(self)
		self.save_btn.setText("Save")

		name = QLabel(self)
		name.setText("Editing " + self.name)
		authors = QLabel(self)
		authors.setText("Made by " + self.author)

		self.scenes_widget = QComboBox(self)
		for i in range(len(self.mem_data["scenes"])):
			self.scenes_widget.insertItem(i, f"Scene {i+1}")

		self.scenes_widget.currentIndexChanged.connect(lambda: self.build_preview())

		self.scenes_widget.setCurrentIndex(self.mem_data["info"]["editor"]["current_scene"])

		self.lists.append(self.scenes_widget)

		self.labels.append(name)
		self.labels.append(authors)

		self.buttons.append(build_btn)
		self.buttons.append(self.save_btn)

		name.move(10, 5)
		authors.move(10, 29)
		self.scenes_widget.move(1780, 10)
		self.scenes_widget.setFixedSize(130, 40)
		add_scene_btn.move(1877, 60)
		add_scene_btn.setStyleSheet(
			'color: white; background-color: rgb(59, 171, 130); font-size: 16px; border: 1px solid rgb(59, 171, 130);')
		add_scene_btn.setFixedSize(32, 32)

		remove_scene_btn.move(1810, 60)
		remove_scene_btn.setStyleSheet(
			'color: white; background-color: rgb(179, 0, 0); font-size: 16px; border: 1px solid rgb(179, 0, 0);')
		remove_scene_btn.setFixedSize(32, 32)

		self.save_btn.move(1740, 1020)
		self.save_btn.setFixedSize(60, 40)
		build_btn.move(1810, 1020)
		build_btn.setFixedSize(100, 40)

		self.save_btn.clicked.connect(lambda: self.save(self.scenes_widget, self.save_btn))

		self.fix_css()
		self.build_preview()


	def build_preview(self):
		# print(self.preview)
		for prev in self.preview:
			try:
				prev.deleteLater()
			except:
				continue

		self.preview = []
		# print(self.preview)
		lab = QLabel(self.mem_data["scenes"][self.scenes_widget.currentIndex()]["title"])
		self.preview.append(lab)
		self.layout.addWidget(lab, 0, 0)
		self.titles.append(lab)
		throw_away = 0
		num = 0
		for i1000 in range(len(self.mem_data["scenes"][self.scenes_widget.currentIndex()]["buttons"])):
			btn = QPushButton(self.mem_data["scenes"][self.scenes_widget.currentIndex()]["buttons"][i1000][0])
			btn.clicked.connect(lambda throw_away, btn=btn, num=num: self.btn_editor(btn, self.scenes_widget.currentIndex(), num))
			self.preview.append(btn)
			self.layout.addWidget(btn)
			self.buttons.append(btn)
			num +=1

		self.fix_css()
		self.save(self.scenes_widget, self.save_btn)

	def fix_css(self):
		self.setStyleSheet('background-color: rgb(37, 37, 37);')
		for i in self.titles:
			try:
				i.setStyleSheet('color: white; font-size: 36px;')
				i.adjustSize()
			except RuntimeError:
				continue

		for i in self.labels:
			try:
				i.setStyleSheet('color: white; font-size: 16px;')
				i.adjustSize()
			except RuntimeError:
				continue

		for i in self.lists:
			try:
				i.setStyleSheet('color: white; background-color: gray; font-size: 18px; border: 0px solid gray;')
				i.adjustSize()
			except RuntimeError:
				continue

		for i in self.buttons:
			try:
				i.setStyleSheet('color: white; background-color: gray; font-size: 16px; border: 1px solid gray;')
				i.adjustSize()
				i.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
			except RuntimeError:
				continue


	def btn_editor(self, btn, scene_id, btn_id):
		dlg = ButtonEditor(self, btn, scene_id, self.mem_data, btn_id)
		dlg.exec()

	def save(self, scenes_widget, save_btn):
		save_btn.setVisible(False)

		self.mem_data["info"]["editor"]["current_scene"] = scenes_widget.currentIndex()

		file = open(f"editor/{self.name}/save.json", "w")
		json.dump(self.mem_data, file)
		file.close()

		save_btn.setVisible(True)


class ButtonEditor(QDialog):
	def __init__(self, parent, btn: QPushButton, scene_id, memory, btn_id):
		super().__init__(parent)

		labels = []
		lines = []
		buttons = []

		self.setWindowTitle(f"Editing button {btn_id} in scene {scene_id}")

		self.layout = QVBoxLayout()
		self.layout1 = QHBoxLayout()
		self.layout2 = QHBoxLayout()
		self.layout3 = QVBoxLayout()
		self.layout4 = QHBoxLayout()
		message1 = QLabel("Button text:")
		labels.append(message1)
		btn_text = QLineEdit()
		btn_text.setText(btn.text())
		lines.append(btn_text)

		message2 = QLabel("Button action:")
		labels.append(message2)
		scenes_widget = QComboBox(self)
		for i in range(len(memory["scenes"])):
			scenes_widget.insertItem(i, f"Go to {i + 1}")
		scenes_widget.setCurrentIndex(scene_id)
		lines.append(scenes_widget)

		message3 = QLabel("Notes:")
		labels.append(message3)
		notes = QTextEdit()
		lines.append(notes)

		cancel = QPushButton("Cancel")
		save = QPushButton("Save")
		buttons.append(cancel)
		buttons.append(save)

		self.layout1.addWidget(message1)
		self.layout1.addWidget(btn_text)
		self.layout2.addWidget(message2)
		self.layout2.addWidget(scenes_widget)
		self.layout3.addWidget(message3)
		self.layout3.addWidget(notes)
		self.layout4.addWidget(cancel)
		self.layout4.addWidget(save)

		self.layout.addLayout(self.layout1)
		self.layout.addLayout(self.layout2)
		self.layout.addLayout(self.layout3)
		self.layout.addLayout(self.layout4)

		self.setLayout(self.layout)

		self.setFixedSize(800, 300)

		for label in labels:
			label.setStyleSheet("color: white; font-size: 16px;")
			label.adjustSize()

		for line in lines:
			line.setStyleSheet("color: white; font-size: 12px; border: 1px solid white;")
			line.adjustSize()

		for button in buttons:
			button.setStyleSheet("color: white; font-size: 12px; border: 1px solid white;")
			button.adjustSize()

		# for line in lines:
		# 	line.setStyleSheet("color: white; font-size: 12px; border: 1px solid white;")
		# 	line.adjustSize()

def restart_editor(name, authors, out):
	w = Editor(name, authors, out)
	w.show()

if __name__ == "__main__":
	app = QApplication(sys.argv)

	window = Editor("test", "JX_Snack", "out/")
	# window = Creator()
	window.show()

	app.exec()
