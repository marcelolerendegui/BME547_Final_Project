# Copyright 2019:
#       Marcelo Lerendegui <marcelo@lerendegui.com>
#       WeiHsien Lee <weihsien.lee@duke.edu>
#       Yihang Xin <yihang.xin@duke.edu>

# This file is part of BME547_Final_Project.
#
# BME547_Final_Project is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or any later version.
#
# BME547_Final_Project is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BME547_Final_Project.
# If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel

from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from client.GUIImageTable import GUIImageTable


class ImageDisplayer(QObject):
    def __init__(self):
        QObject.__init__(self)
        # List of display windows open
        self.img_displays = {}

    def new_display(self):

        if len(self.img_displays.keys()) > 0:
            max_index = max(self.img_displays.keys())
            empty_indices = list(
                set(range(1, max_index+1)) - set(self.img_displays.keys())
            )

            if len(empty_indices) > 0:
                new_index = empty_indices[0]
            else:
                new_index = max_index + 1
        else:
            new_index = 1
        self.img_displays[new_index] = GUIShowImage(new_index)
        self.img_displays[new_index].show()
        self.img_displays[new_index].on_close.connect(
            self.delete_display
        )
        print("New Display Created: ", new_index)

    @pyqtSlot(int)
    def delete_display(self, val):
        print("Display Deleted: ", val)
        del self.img_displays[val]


class GUIShowImage(QMainWindow):
    on_close = QtCore.pyqtSignal(int)

    def __init__(self, display_key):
        # Setup main window
        super().__init__()
        self.centralWidget = QWidget(self)

        self.lbl_image = QLabel(self)
        self.lbl_image.setText("asfafs")
        self.lbl_image.show()
        self.pixmap = QPixmap('client/image.jpg')
        self.lbl_image.setPixmap(self.pixmap)

        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.addWidget(self.lbl_image)

        self.setCentralWidget(self.centralWidget)

        self.dkey = display_key

    def closeEvent(self, evnt):
        self.on_close.emit(self.dkey)
