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
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton

from client.encryption import get_userhash


class GUILoginDialog(QMainWindow):
    login = QtCore.pyqtSignal(str)

    def __init__(self):
        # Main Window
        super().__init__()
        QtCore.QObject.__init__(self)
        self.resize(988, 505)
        self.centralWidget = QWidget(self)
        self.setGeometry(500, 500, 300, 100)
        self.setFixedSize(300, 100)
        self.setWindowTitle("Log In")
        # Username Label
        self.lbl_username = QLabel()
        self.lbl_username.setText("Username:")

        # Username Input
        self.txt_username = QLineEdit()

        # Password Label
        self.lbl_password = QLabel()
        self.lbl_password.setText("Password:")

        # Password Input
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)

        # Submit Button
        self.btn_submit = QPushButton()
        self.btn_submit.setText("Submit")
        self.btn_submit.clicked.connect(self.submit_username_password)

        # Layout
        self.hlay_username = QHBoxLayout()
        self.hlay_username.addWidget(self.lbl_username)
        self.hlay_username.addWidget(self.txt_username)

        self.hlay_password = QHBoxLayout()
        self.hlay_password.addWidget(self.lbl_password)
        self.hlay_password.addWidget(self.txt_password)

        self.vlay_general = QVBoxLayout(self.centralWidget)

        self.vlay_general.setContentsMargins(0, 0, 0, 0)

        self.vlay_general.addLayout(self.hlay_username)
        self.vlay_general.addLayout(self.hlay_password)
        self.vlay_general.addWidget(self.btn_submit)

        self.setCentralWidget(self.centralWidget)

        self.setWindowModality(QtCore.Qt.ApplicationModal)

    def submit_username_password(self):
        user_hash = get_userhash(
            self.txt_username.text(),
            self.txt_password.text()
        )
        self.login.emit(user_hash)
        self.close()
