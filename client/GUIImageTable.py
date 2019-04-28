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
            self.setRowCount(r+1)

            item = QTableWidgetItem(k)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.setItem(r, 0, item)

            item = QTableWidgetItem(v['filename'])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.setItem(r, 1, QTableWidgetItem(item))

            item = QTableWidgetItem(v['img_format'])
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.setItem(r, 2, QTableWidgetItem(item))

            item = QTableWidgetItem(v['size'])
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.setItem(r, 3, QTableWidgetItem(item))

            item = QTableWidgetItem(v['description'])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
            self.setItem(r, 4, QTableWidgetItem(item))

            item = QTableWidgetItem(v['timestamp'])
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            self.setItem(r, 5, QTableWidgetItem(item))

    def get_selected_rows(self):
        indexes = self.selectionModel().selectedRows()
        rows = []
        for index in sorted(indexes):
            rows.append(index.row())
        return rows

    def get_selected_ids(self):
        rows = self.get_selected_rows()
        ids = []
        for r in rows:
            ids.append(self.item(r, 0).text())
        return ids

    def get_selected_names(self):
        rows = self.get_selected_rows()
        names = []
        for r in rows:
            names.append(self.item(r, 1).text())
        return names

    def get_mrs_rows(self, n: int):
        indexes = self.selectionModel().selectedRows()
        rows = []
        for index in indexes:
            rows.append(index.row())
        return rows[-n::]

    def get_mrs_ids(self, n: int):
        rows = self.get_mrs_rows(n)
        ids = []
        for r in rows:
            ids.append(self.item(r, 0).text())
        return ids

    def get_mrs_names(self, n: int):
        rows = self.get_mrs_rows(n)
        names = []
        for r in rows:
            names.append(self.item(r, 1).text())
        return names
