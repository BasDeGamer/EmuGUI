from PySide6.QtWidgets import *
from PySide6 import QtGui
from uiScripts.ui_Update import Ui_Dialog
import webbrowser
import platform
import platformSpecific.windowsSpecific
import platformSpecific.unixSpecific
import sqlite3
import translations.de
import translations.uk
import translations.en
import locale

class UpdateAvailable(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("EmuGUI Update")
        self.langDetect()
        
        try:
            self.setWindowIcon(QtGui.QIcon("EmuGUI.png"))

        except:
            pass
        
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.redirectToWebsite)
        self.pushButton_2.clicked.connect(self.close)

    def redirectToWebsite(self):
        if platform.system() == "Windows":
            connection = platformSpecific.windowsSpecific.setupWindowsBackend()
        
        else:
            connection = platformSpecific.unixSpecific.setupUnixBackend()

        select_update_mirror = """
        SELECT name, value FROM updater
        WHERE name = "updatemirror";
        """

        cursor = connection.cursor()

        try:
            cursor.execute(select_update_mirror)
            connection.commit()
            result = cursor.fetchall()

            try:
                qemu_img_slot = str(result[0])
                
                if result[0][1] == "GitHub":
                    webbrowser.open("https://github.com/Tech-FZ/EmuGUI")
                
                elif result[0][1] == "Codeberg":
                    webbrowser.open("https://codeberg.org/lucien-rowan/EmuGUI")

                print("The query was executed successfully.")
                self.close()

            except:
                print("The query was executed successfully but the mirror couldn't be retrieved. Please check one of the following mirrors:")
                print("https://github.com/Tech-FZ/EmuGUI or")
                print("https://codeberg.org/lucien-rowan/EmuGUI")
        
        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")

    def langDetect(self):
        select_language = """
        SELECT name, value FROM settings
        WHERE name = "lang";
        """

        if platform.system() == "Windows":
            connection = platformSpecific.windowsSpecific.setupWindowsBackend()
        
        else:
            connection = platformSpecific.unixSpecific.setupUnixBackend()

        cursor = connection.cursor()

        try:
            cursor.execute(select_language)
            connection.commit()
            result = cursor.fetchall()

            # Language modes
            # system: language of OS
            # en: English
            # de: German
            langmode = "system"

            try:
                qemu_img_slot = str(result[0])

                i = 0
                
                if result[0][1] == "en":
                    langmode = "en"

                elif result[0][1] == "de":
                    langmode = "de"

                elif result[0][1] == "uk":
                    langmode = "uk"

                self.setLanguage(langmode)
                print("The query was executed successfully. The language slot already is in the database.")

            except:
                langmode = "system"
                self.setLanguage(langmode)
                print("The query was executed successfully. The language slot has been created.")
        
        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")

    def setLanguage(self, langmode):
        if langmode == "system":
            languageToUse = locale.getlocale()[0]

        else:
            languageToUse = langmode

        if languageToUse.startswith("de"):
            translations.de.translateUpdateAvailableDE(self)

        elif languageToUse.startswith("uk"):
            translations.uk.translateUpdateAvailableUK(self)

        else:
            translations.en.translateUpdateAvailableEN(self)