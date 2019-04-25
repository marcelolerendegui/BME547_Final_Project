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

from client.GUIMain import GUIMain
from client.GUILoginDialog import GUILoginDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject


class GUI(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.dlg_login = GUILoginDialog()
        self.dlg_login.login.connect(self.on_login)
        self.dlg_login.show()
        self.client_gui = GUIMain()

    @pyqtSlot(str)
    def on_login(self, user_hash):
        user_hash = 'willy'
        self.user_hash = user_hash
        self.client_gui.user_hash = user_hash
        self.client_gui.show()
        print("login signal received: ", self.user_hash)
