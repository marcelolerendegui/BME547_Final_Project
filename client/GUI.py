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
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot


class GUI(QObject):
    """This GUI class is in charge of opening the other windows
    """

    def __init__(self):
        QObject.__init__(self)
        self.dlg_login = GUILoginDialog()
        self.dlg_login.login.connect(self.on_login)
        self.dlg_login.show()

    @pyqtSlot(str)
    def on_login(self, user_hash: str):
        """Slot to be called after having the user hash

        :param user_hash: hash that identifies a user
        :type user_hash: str
        """
        self.user_hash = user_hash
        self.client_gui = GUIMain()
        self.client_gui.user_hash = user_hash
        self.client_gui.show()
        self.client_gui.update_table()
