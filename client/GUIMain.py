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

from client.files import *
import client.api_calls as api
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
from client.GUIShowImage import GUIShowImage
from PIL import Image

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

        self.btn_upload.clicked.connect(self.btn_upload_callback)

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
        self.btn_dload_jpeg.clicked.connect(self.download_images_jpg)
        self.btn_dload_png.clicked.connect(self.download_images_png)
        self.btn_dload_tiff.clicked.connect(self.download_images_tiff)

    def btn_upload_callback(self):

        # Create File Select Dialog
        dialog = QFileDialog(parent=self, caption='Images')
        dialog.setMimeTypeFilters(
            ["image/jpeg", "image/png", "image/tiff", 'application/zip'])
        dialog.setFileMode(QFileDialog.ExistingFile)

        if dialog.exec_() == QDialog.Accepted:

            filename = dialog.selectedFiles()[0]

            with open(filename, 'rb') as f:
                file_b64s = fio_to_b64s(f)

                if ext_from_path(filename) == '.zip':
                    ret = api.upload_zip(
                        file_b64s,
                        nameext_from_path(filename),
                        self.user_hash
                    )
                    print(ret)
                else:
                    ret = api.upload_image(
                        file_b64s,
                        nameext_from_path(filename),
                        self.user_hash
                    )

        self.update_table()

    def update_table(self):
        info_dict = api.get_images_info(self.user_hash)
        self.tbl_images.load_data_from_dict(info_dict)

    def btn_display_callback(self):
        rows = self.tbl_images.get_selected_rows()
        ids = []
        names = []
        for r in rows:
            ids.append(self.tbl_images.item(r, 0).text())
            names.append(self.tbl_images.item(r, 1).text())

        for id, name in zip(ids, names):
            dout = api.get_single_image(id, self.user_hash)
            image_fio = b64s_to_fio(dout['data'])
            self.img_displayer.new_display(image_fio, name)

    def btn_compare_callback(self):
        # ensure selected row
        # get image IDs
        # request for image data
        # display selected imgs
        selected_rows = self.tbl_images.get_selected_rows()
        print(selected_rows)

    def btn_contrast_invert_callback(self, image_id, image_format, filename):
        # get requests contrast_invert func
        # if no selection in tbl_images.get_selected_rows()->ErrorMessage
        # input = tbl_images.get_selected_rows(self)
        # if input==None:
        #     self.warning_box()
        api.contrast_invert(image_id, image_format, filename)
        self.update_table()

    def btn_display_hist_callback(self):
        # get requests img histogram

        pass

    def btn_display_color_hist_callback(self):
        # get requests color_histogram image

        pass

    def btn_equalize_hist_callback(self, image_id, image_format, filename):
        # get requests equalize hist image
        api.equalize_histogram(image_id, image_format, filename)
        self.update_table()
        pass

    def btn_contrast_stretch_callback(self, image_id, image_format, filename):
        # get requests contrast stretch
        api.contrast_stretch(image_id, image_format, filename)
        self.update_table()
        pass

    def btn_log_compress_callback(self, image_id, image_format, filename):
        # get requests log compress
        api.log_compress(image_id, image_format, filename)
        self.on_process_done()
        self.update_table()
        pass

    def btn_dload_jpeg_callback(self, image_id, filename, image_format='jpeg'):
        # get requests jpeg img
        api.download_images(image_id, filename, image_format)
        pass

    def btn_dload_tiff_callback(self, image_id, filename, image_format='tiff'):
        # get requests tiff img
        api.download_images(image_id, filename, image_format)
        pass

    def btn_dload_png_callback(self, image_id, filename, image_format='png'):
        # get requests png img
        api.download_images(image_id, filename, image_format)
        pass

    def warning_box(self):
        QMessageBox.about(self, 'Errormessage', 'No image uploaded')

    def on_process_done(self):
        QMessageBox.about(self, 'Process Done', 'Process Done')

    def download_images_jpg(self):
        self.download_images('JPEG')

    def download_images_png(self):
        self.download_images('PNG')

    def download_images_tiff(self):
        self.download_images('TIFF')

    def download_images(self, im_format):
        rows = self.tbl_images.get_selected_rows()
        ids = []
        names = []
        for r in rows:
            ids.append(self.tbl_images.item(r, 0).text())
            names.append(self.tbl_images.item(r, 1).text())

        if len(ids) == 1:

            # Create File Save Dialog
            dialog = QFileDialog(parent=self, caption='111Save As..')

            dialog.setMimeTypeFilters(["image/"+im_format.lower()])
            dialog.setFileMode(QFileDialog.AnyFile)

            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.selectedFiles()[0]
                dout = api.get_download_images(ids, im_format, self.user_hash)
                image_b = b64s_to_b(dout['data'])
                with open(filename, 'wb+') as f:
                    f.write(image_b)

        elif len(ids) >= 1:

            # Create File Save Dialog
            dialog = QFileDialog(parent=self, caption='222Save As..')
            dialog.setMimeTypeFilters(['application/zip'])
            dialog.setFileMode(QFileDialog.AnyFile)

            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.selectedFiles()[0]
                dout = api.get_download_images(ids, im_format, self.user_hash)
                image_b = b64s_to_b(dout['data'])
                with open(filename, 'wb+') as f:
                    f.write(image_b)
        else:
            return
