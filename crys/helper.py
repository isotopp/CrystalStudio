import os
import platform
import subprocess
import sys

try:
	from crys.crystal import *
except (ImportError, ModuleNotFoundError):
	os.system("python3 -m pip install PyQt6")
	os.system("python3 -m pip install requests")
	print("\nPlease restart CrystalStudio!")
	sys.exit(0)

version = "1.3.0-SNAPSHOT [public-18]"


def open_file(path: str) -> None:
	if platform.system() == "Windows":
		os.startfile(path)
	elif platform.system() == "Darwin":
		subprocess.Popen(["open", path])
	else:
		subprocess.Popen(["xdg-open", path])


def translate_builder(text: str) -> BuilderType:
	if text.lower().startswith(("js", "javascript", "web app")):
		return BuilderType.JavaScript
	else:
		raise ValueError(f"Not translatable: {text}")


def install_requirements() -> None:
	os.system("python3 -m pip install PyQt6")
	os.system("python3 -m pip install requests")


def settings_filepath() -> str:
	return "crys/storage/settings.json"


def get_settings() -> dict:
	settings_file = open(settings_filepath(), "r")
	try:
		settings = json.load(settings_file)
	except json.decoder.JSONDecodeError:
		file = open(settings_filepath(), "w")
		json.dump({"ui_scale": [1, 1.0], "theme": [1, "dark"], "custom_theme": "",
				   "bookmarked_projects": [], "icon": [0, "new_icon"]}, file)
		file.close()
		settings_file2 = open(settings_filepath(), "r")

		settings = json.load(settings_file2)
		print("Settings were corrupted. Settings have been reset")
	return settings


def get_scaled_size(size: int) -> int:
	return int(size * get_settings()["ui_scale"][1])


def generate_stylesheet() -> str:
	settings = get_settings()

	custom_theme = settings["custom_theme"]

	rv = "".join(
		open("crys/storage/themes/" + settings["theme"][1] + ".theme", "r").readlines())  # rv means return value
	rv = rv.split("*** CUSTOM THEME SETTINGS BELOW ***")
	rv = rv[0]
	rv += " " + custom_theme
	rv += " QTabBar::tab {font-size: " + str(int(16 * settings["ui_scale"][1])) + "px;}"
	rv += " QLabel {font-size: " + str(int(16 * settings["ui_scale"][1])) + "px;}"
	rv += " QComboBox {font-size: " + str(int(16 * settings["ui_scale"][1])) + "px;}"
	rv += " QComboBox {font-size: " + str(int(16 * settings["ui_scale"][1])) + "px;}"
	rv += " QLineEdit {font-size: " + str(int(14 * settings["ui_scale"][1])) + "px;}"
	rv += " QPushButton {font-size: " + str(int(16 * settings["ui_scale"][1])) + "px;}"
	rv += " QTextEdit {font-size: " + str(int(14 * settings["ui_scale"][1])) + "px;}"

	return rv


def generate_extra_style() -> dict:
	settings = get_settings()

	rv = "".join(
		open("crys/storage/themes/" + settings["theme"][1] + ".theme", "r").readlines())  # rv means return value
	rv = rv.split("*** CUSTOM THEME SETTINGS BELOW ***")
	rv = rv[1]
	rv = json.loads(rv)

	return rv
