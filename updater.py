# This updater updates from 1.1.1 to 1.2.0
# MAKE SURE YOU HAVE INSTALLED THESE TWO LIBRARIES BEFORE USING:
#  - PyQt6
#  - requests
# ALSO MAKE SURE THAT THERE IS NO FOLDER CALLED "CrystalStudioUpdaterFiles"
# If not, just install them with "pip install PyQt6" and "pip install requests"
import io
import json
import os
import shutil
import sys
import zipfile

import requests

from crys.helper import version

print("Starting update to 1.2.0...")

if version == "1.2.0":
	print("You have already updated.")
if version != "1.1.1":
	print(
		"WARNING. You are running a different version than 1.1.1! This updater is made ONLY for 1.1.1 to 1.2.0! Do you want to continue? Y/n")
	action = input("> ")
	if action != "y":
		print("Stopping updater...")
		sys.exit()
	else:
		print("Continuing update to 1.2.0...")

download_url = "https://github.com/JXSnack/CrystalStudio/archive/refs/tags/v1.2.0.zip"  # set the download url
r = requests.get(download_url, allow_redirects=True, stream=True)  # get the download
z = zipfile.ZipFile(io.BytesIO(r.content))  # get the zipfile
csuf = "CrystalStudioUpdaterFiles"  # set the folder name
download_name = "CrystalStudio-main"  # set the downloaded file name
os.mkdir(csuf)  # make the folder
z.extractall(f"{csuf}/")  # extract the zip
csuf = csuf + f"/{download_name}"  # set the new folder name

settings_backup = json.load(open("crys/storage/settings.json"))  # make a settings backup
shutil.rmtree("crys")  # remove the old crystal studio code folder

os.remove("main.py")  # remove the old main.py
os.remove("editor.py")  # remove old editor.py

shutil.move(csuf + "/crys", os.getcwd())  # move the new code folder to the place where the old one was
new_mainfile_content = open(csuf + "/main.py", "r").readlines()  # get new content
new_mainfile = open("main.py", "w").write("\n".join(new_mainfile_content))  # place it there where it belongs

new_editor_content = open(csuf + "/editor.py", "r").readlines()  # get new content
new_editor = open("editor.py", "w").write("\n".join(new_editor_content))  # place it there where it belongs

new_settings = open("crys/storage/settings.json", "w").write("\n".join(settings_backup)) # place the settings backup

shutil.rmtree("CrystalStudioUpdaterFiles")  # clean up the mess that we made

# Finished
print("Finished updating to 1.2.0!")
print("You can now delete this updater")
