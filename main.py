#!/bin/env python3
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtGui
from PyQt6 import QtCore
import sys
import re
import socket
import os
import psutil
import subprocess
from PyQt6.QtCore import QObject, QThread, pyqtSignal, Qt
from time import *
class RamChecker(QObject):
    finished = pyqtSignal()
    usedram = pyqtSignal(str)
    freeram = pyqtSignal(str)

    def run(self):
        """Long-running task."""
        s = round(psutil.virtual_memory().total)
        while True:
            sleep(0.5)
            self.usedram.emit(str(round(psutil.virtual_memory().used / (1024.0 ** 2))) + "  MiB")
            self.freeram.emit(str(round((s - psutil.virtual_memory().used)  / (1024.0 ** 2))) + "  MiB")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('form.ui', self) # Load the .ui file
        self.toolButton_about.setStyleSheet("background-color: rgb(0, 163, 255);")
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().hide()
        self.hostname.setText(socket.gethostname())
        ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            ip.connect(("8.8.8.8", 80))

        except:
            self.ipaddr.setText("No network found")
        else:
            self.ipaddr.setText(ip.getsockname()[0])
        ip.close()
        self.username.setText(os.getlogin())
        self.totalram.setText(str(round(psutil.virtual_memory().total / (1024.0 ** 2))))
        self.scanfiles()

            
#        for x in range(0, 1000):
#            button = QToolButton()
#            button.setIcon(QtGui.QIcon("assets/iot.png"))
#            button.setText("lol")
#            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
#            button.setFixedSize(150, 100)
#            #button.resize(150, 50)
#            Item = QListWidgetItem(self.listWidget)
#            Item.setSizeHint(button.sizeHint())
#            self.listWidget.addItem(Item)
#            self.listWidget.setItemWidget(Item, button)
#            button.clicked.connect(button.hide)
            #self.gridLayout.addWidget(button)
    def tabchange(self):
        sender = self.sender()
        self.toolButton_help.setStyleSheet("background-color: black;")
        self.toolButton_about.setStyleSheet("background-color: black;")
        self.toolButton_apps.setStyleSheet("background-color: black;")
        self.toolButton_terminal.setStyleSheet("background-color: black;")
        sender.setStyleSheet("background-color: rgb(0, 163, 255);")
        if (sender == self.toolButton_about):
            self.tabWidget.setCurrentIndex(0)
        elif (sender == self.toolButton_apps):
            self.tabWidget.setCurrentIndex(1)
        elif (sender == self.toolButton_terminal):
            self.tabWidget.setCurrentIndex(2)
        elif (sender == self.toolButton_help):
            self.tabWidget.setCurrentIndex(3)
    def set_usedmemory(self, n):
        self.usedram.setText(str(n))
    def set_freememory(self, n):
        self.freeram.setText(str(n))
    def memory_task(self):
        self.thread = QThread()
        self.worker = RamChecker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.usedram.connect(self.set_usedmemory)
        self.worker.freeram.connect(self.set_freememory)
        self.thread.start()
        # Step 6: Start the thread
    def startapp(self, c):
        subprocess.Popen(c.split(" "))
    def scanfiles(self):
        for file in os.listdir("/usr/share/applications/"):
            if file.endswith(".desktop"):
                filer = open(os.path.join("/usr/share/applications/", file), "r")
                for line in filer:
                    if line.find('[') == 0:
                        current_section = line.rstrip("\n")
                    if current_section == """[Desktop Entry]""":
                        splited_line = line.rstrip("\n").split("=")
                        if splited_line[0] == "Name":
                            name = splited_line[1]
                        elif splited_line[0] == "Exec":
                            execute = splited_line[1]
                        elif splited_line[0] == "Icon":
                            icon = splited_line[1]
                button = QToolButton()
                button.setIcon(QtGui.QIcon("assets/iot.png"))
                button.setText(name)
                button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
                button.setFixedSize(150, 100)
                Item = QListWidgetItem(self.listWidget)
                Item.setSizeHint(button.sizeHint())
                self.listWidget.addItem(Item)
                self.listWidget.setItemWidget(Item, button)
                button.clicked.connect(lambda: self.startapp(execute))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.memory_task()
    win.showFullScreen()
    #win.show()
    sys.exit(app.exec())