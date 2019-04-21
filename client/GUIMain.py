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
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QDialog

from client.GUIImageTable import GUIImageTable
from client.GUILoginDialog import GUILoginDialog


class GUIMain(QMainWindow):

    def __init__(self):
        # Setup main window
        super().__init__()
        self.resize(988, 505)
        self.centralWidget = QWidget(self)
        self.setGeometry(100, 100, 650, 500)

        # Table
        self.tbl_images = GUIImageTable(self.centralWidget)

        # Buttons
        self.create_button_block()
        self.setup_button_block()

        # Setup Layout
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.tbl_images)
        self.verticalLayout.addLayout(self.lay_button_block)
        self.setCentralWidget(self.centralWidget)

        self.dlg_login = GUILoginDialog()
        self.dlg_login.show()

    def create_button_block(self):
        self.btn_compare = QPushButton(self.centralWidget)
        self.btn_display = QPushButton(self.centralWidget)
        self.btn_display_hist = QPushButton(self.centralWidget)
        self.btn_display_color_hist = QPushButton(self.centralWidget)

        self.btn_equalize_hist = QPushButton(self.centralWidget)
        self.btn_contrast_stretch = QPushButton(self.centralWidget)
        self.btn_log_compress = QPushButton(self.centralWidget)
        self.btn_contrast_invert = QPushButton(self.centralWidget)

        self.btn_dload_jpeg = QPushButton(self.centralWidget)
        self.btn_dload_tiff = QPushButton(self.centralWidget)
        self.btn_dload_png = QPushButton(self.centralWidget)
        self.btn_upload = QPushButton(self.centralWidget)

        self.lay_button_block = QGridLayout()

        self.lay_button_block.addWidget(self.btn_compare, 0, 0)
        self.lay_button_block.addWidget(self.btn_display, 1, 0,)
        self.lay_button_block.addWidget(self.btn_display_hist, 2, 0)
        self.lay_button_block.addWidget(self.btn_display_color_hist, 3, 0)

        self.lay_button_block.addWidget(self.btn_equalize_hist, 0, 1)
        self.lay_button_block.addWidget(self.btn_contrast_stretch, 1, 1)
        self.lay_button_block.addWidget(self.btn_log_compress, 2, 1)
        self.lay_button_block.addWidget(self.btn_contrast_invert, 3, 1)

        self.lay_button_block.addWidget(self.btn_dload_jpeg, 0, 2)
        self.lay_button_block.addWidget(self.btn_dload_tiff, 1, 2)
        self.lay_button_block.addWidget(self.btn_dload_png, 2, 2)
        self.lay_button_block.addWidget(self.btn_upload, 3, 2)

    def setup_button_block(self):
        self.btn_contrast_invert.setText("Contrast Invert")
        self.btn_display.setText("Display")
        self.btn_display_hist.setText("Display HIST")
        self.btn_display_color_hist.setText("Display Color HIST")
        self.btn_compare.setText("Compare")
        self.btn_equalize_hist.setText("Equalize Histogram")
        self.btn_contrast_stretch.setText("Contrast Stretch")
        self.btn_log_compress.setText("Log Compress")
        self.btn_dload_jpeg.setText("Download JPEG")
        self.btn_dload_tiff.setText("Download TIFF")
        self.btn_dload_png.setText("Download PNG")
        self.btn_upload.setText("Upload")
        self.btn_upload.clicked.connect(self.upload_callback)

    def upload_callback(self):

        # Create File Select Dialog
        dialog = QFileDialog(parent=self, caption='Images')
        dialog.setMimeTypeFilters(["image/jpeg", "image/png", "image/tiff"])
        dialog.setFileMode(QFileDialog.ExistingFiles)

        if dialog.exec_() == QDialog.Accepted:
            print(dialog.selectedFiles())
            # Call API upload Files

    def on_receive_image_info(self):

        self.tbl_images.load_data_from_dict(
            {
                "1": {
                    "ID": "1",
                    "Filename": "mega_image.jpg",
                    "Format": "jpeg",
                    "Size": "640x480",
                    "Description": "Description",
                    "Timestamp": "Today",
                }
            }
        )

    def on_equalize_histogram(self):
        pass

    def get_table_selection(self):
        indexes = self.tbl_images.selectionModel().selectedRows()
        for index in sorted(indexes):
            print('Row %d is selected' % index.row())
