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
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTableWidget


class GUIImageTable(QTableWidget):

    header_names = [
        "ID",
        "Filename",
        "Format",
        "Size",
        "Description",
        "Timestamp"
    ]

    def __init__(self, parent=None):

        super().__init__(parent=parent)

        # Create Table
        self.setColumnCount(6)

        # Setup Table
        for i, hname in enumerate(self.header_names):
            item = QTableWidgetItem()
            self.setHorizontalHeaderItem(i, item)
            self.horizontalHeaderItem(i).setText(hname)

    def load_data_from_dict(self, info):
        for r, (k, v) in enumerate(info.items()):
            print(r, k, v)
            self.setRowCount(r+1)
            for c, hn in enumerate(self.header_names):
                self.setItem(r, c, QTableWidgetItem(v[hn]))
                print(r, c, hn, v[hn])
