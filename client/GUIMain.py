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
from PyQt5.QtWidgets import QMessageBox
from client.GUIImageTable import GUIImageTable
from client.GUIShowImage import ImageDisplayer
# form client.GUIShowImage import GUIShowImage
import api_calls
#
# def test(a,b,c):
#     """
#     :param a: 
#     :param b:
#     :param c:
#     :return:
#     """
#     pass


class GUIMain(QMainWindow):

    def __init__(self):
        # Setup main window
        super().__init__()
        self.resize(988, 505)
        self.centralWidget = QWidget(self)
        self.setGeometry(100, 100, 650, 500)

        self.img_displayer = ImageDisplayer()
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
        self.btn_display.clicked.connect(self.btn_display_callback)
        self.btn_contrast_invert.clicked.connect(
            self.btn_contrast_invert_callback)
        self.btn_display_hist.clicked.connect(self.btn_display_hist_callback)
        self.btn_display_color_hist.clicked.connect(
            self.btn_display_color_hist_callback)
        self.btn_compare.clicked.connect(self.btn_compare_callback)
        self.btn_equalize_hist.clicked.connect(self.btn_equalize_hist_callback)
        self.btn_contrast_stretch.clicked.connect(
            self.btn_contrast_stretch_callback)
        self.btn_log_compress.clicked.connect(self.btn_log_compress_callback)
        self.btn_dload_jpeg.clicked.connect(self.btn_dload_jpeg_callback)
        self.btn_dload_png.clicked.connect(self.btn_dload_png_callback)
        self.btn_dload_tiff.clicked.connect(self.btn_dload_tiff_callback)

    def upload_callback(self):

        # Create File Select Dialog
        dialog = QFileDialog(parent=self, caption='Images')
        dialog.setMimeTypeFilters(["image/jpeg", "image/png", "image/tiff"])
        dialog.setFileMode(QFileDialog.ExistingFiles)

        if dialog.exec_() == QDialog.Accepted:
            print(dialog.selectedFiles())
            # Call API upload Files/ multiple?
        self.api_calls.upload_image()

    def on_receive_image_info(self):
        self.api_calls.Get_images_info()
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
        self.api_calls.equalize_histogram()
        pass

    def get_table_selection(self):
        indexes = self.tbl_images.selectionModel().selectedRows()
        for index in sorted(indexes):
            print('Row %d is selected' % index.row())
        return indexes.row()

    def btn_display_callback(self, ):
        rows = self.get_table_selection()
        get_img = self.Get_images_info()
        self.img_displayer.new_display()

    def btn_compare_callback(self):
        # ensure selected row
        # get image IDs
        # request for image data
        # display selected imgs
        selected_rows = self.get_table_selection()
        print(selected_rows)
        self.img_displayer.new_display()
        pass

    def btn_contrast_invert_callback(self, image_id, image_format, filename):
        # get requests contrast_invert func
        # if no selection in get_table_selection()->ErrorMessage
        # input = get_table_selection(self)
        # if input==None:
        #     self.warning_box()
        self.api_calls.contrast_invert(image_id, image_format, filename)
        pass

    def btn_display_hist_callback(self):
        # get requests img histogram

        pass

    def btn_display_color_hist_callback(self):
        # get requests color_histogram image

        pass

    def btn_equalize_hist_callback(self, image_id, image_format, filename):
        # get requests equalize hist image
        self.api_calls.equalize_histogram(image_id, image_format, filename)
        pass

    def btn_contrast_stretch_callback(self, image_id, image_format, filename):
        # get requests contrast stretch
        self.api_calls.contrast_stretch(image_id, image_format, filename)
        pass

    def btn_log_compress_callback(self, image_id, image_format, filename):
        # get requests log compress
        self.api_calls.log_compress(image_id, image_format, filename)
        self.on_process_done()
        pass

    def btn_dload_jpeg_callback(self, image_id, filename, image_format='jpeg'):
        # get requests jpeg img
        self.api_calls.download_images(image_id, filename, image_format)
        pass

    def btn_dload_tiff_callback(self, image_id, filename, image_format='tiff'):
        # get requests tiff img
        self.apicalls.download_images(image_id, filename, image_format)
        pass

    def btn_dload_png_callback(self, image_id, filename, image_format='png'):
        # get requests png img
        self.api_calls.download_images(image_id, filename, image_format)
        pass

    def warning_box(self):
        QMessageBox.about(self, 'Errormessage', 'No image uploaded')

    def on_process_done(self):
        QMessageBox.about(self, 'Process Done', 'Process Done')

