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

from core.files import *
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
import core.img_proc_core as img_proc


class GUIMain(QMainWindow):
    """Main window of the client
    """

    def __init__(self):
        # Setup main window
        super().__init__()
        self.setWindowTitle("Image Processing Client")

        self.centralWidget = QWidget(self)
        self.setGeometry(100, 100, 1000, 500)

        self.img_displayer = ImageDisplayer()

        # Table
        self.tbl_images = GUIImageTable(self.centralWidget)
        self.tbl_images.cellChanged.connect(
            self.tbl_images_cell_changed_callback
        )
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
        """creates a grid of 3 by 3 buttons
        """
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
        """Setup all button properties for the button block
        """
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
        """Callback for the button UPLOAD

        Asks the user to select a file and calls the api to send it
        to the server.
        """
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
            else:
                ret = api.upload_image(
                    file_b64s,
                    nameext_from_path(filename),
                    self.user_hash
                )
            if ret.get('success') is False:
                self.show_error(ret['error_msg'])
        self.update_table()

    def update_table(self):
        self.show_as_waiting(True)
        ret = api.get_images_info(self.user_hash)
        if ret.get('success') is False:
            self.show_error(ret['error_msg'])
            return

        self.tbl_images.blockSignals(True)
        self.tbl_images.load_data_from_dict(ret)
        self.tbl_images.blockSignals(False)
        self.show_as_waiting(False)

    def btn_display_callback(self):
        """Callback for the button DISPLAY

        for each selected row:
        calls the api to get the image from the server
        displays the image in a new window
        """
        self.show_as_waiting(True)
        ids = self.tbl_images.get_selected_ids()
        names = self.tbl_images.get_selected_names()
        for id, name in zip(ids, names):
            ret = api.get_single_image(id, self.user_hash)
            if ret.get('success') is False:
                self.show_error(ret['error_msg'])
            else:
                image_fio = b64s_to_fio(ret['data'])
                self.img_displayer.new_display(image_fio, name)
        self.show_as_waiting(False)

    def btn_compare_callback(self):
        """Callback for the button COMPARE

        for the two most recently selected rows
        calls the api to get the image from the server
        displays the image in a new window
        """
        self.show_as_waiting(True)
        mrs2_ids = self.tbl_images.get_mrs_ids(2)
        mrs2_names = self.tbl_images.get_mrs_names(2)

        for id, name in zip(mrs2_ids, mrs2_names):
            ret = api.get_single_image(id, self.user_hash)
            if ret.get('success') is False:
                self.show_error(ret['error_msg'])
            else:
                image_fio = b64s_to_fio(ret['data'])
                self.img_displayer.new_display(image_fio, name)
        self.show_as_waiting(False)

    def btn_display_hist_callback(self):
        """Callback for the button DISPLAY HISTOGRAM

        for each selected row:
        calls the api to get the image from the server
        calculates the gray histogram
        displays the histogram in a new window
        """
        self.show_as_waiting(True)
        ids = self.tbl_images.get_selected_ids()
        names = self.tbl_images.get_selected_names()

        for id, name in zip(ids, names):
            ret = api.get_single_image(id, self.user_hash)
            if ret.get('success') is False:
                self.show_error(ret['error_msg'])
            else:
                image_fio = b64s_to_fio(ret['data'])
                img_hist_fio = img_proc.fio_hist_fio(image_fio)
                self.img_displayer.new_display(
                    img_hist_fio, name + ' Histogram')
                del image_fio
                del img_hist_fio
        self.show_as_waiting(False)

    def btn_display_color_hist_callback(self):
        """Callback for the button DISPLAY COLOR HISTOGRAM

        for each selected row:
        calls the api to get the image from the server
        calculates the color histogram
        displays the histogram in a new window
        """
        self.show_as_waiting(True)
        ids = self.tbl_images.get_selected_ids()
        names = self.tbl_images.get_selected_names()

        for id, name in zip(ids, names):
            ret = api.get_single_image(id, self.user_hash)
            if ret.get('success') is False:
                self.show_error(ret['error_msg'])
            else:
                image_fio = b64s_to_fio(ret['data'])
                img_hist_fio = img_proc.fio_color_hist_fio(image_fio)
                self.img_displayer.new_display(
                    img_hist_fio, name + ' Histogram')
        self.show_as_waiting(False)

    def image_proc_selected(self, algorithm: str):
        """Apply algorithm to all selected images

        :param algorithm: name of the algorithm
        :type algorithm: str
        """
        self.show_as_waiting(True)
        rows = self.tbl_images.get_selected_rows()
        ids = []
        names = []
        for r in rows:
            ids.append(self.tbl_images.item(r, 0).text())
            names.append(self.tbl_images.item(r, 1).text())
        for id, name in zip(ids, names):
            ret = api.apply_algorithm(
                id,
                algorithm,
                'JPEG',
                name,
                self.user_hash
            )
            if ret.get('success') is False:
                self.show_error(ret['error_msg'])
        self.update_table()
        self.show_as_waiting(False)

    def btn_contrast_invert_callback(self):
        """Callback for the button CONTRAST INVERT
        """
        self.show_as_waiting(True)
        self.image_proc_selected('Contrast Invert')
        self.show_as_waiting(False)

    def btn_equalize_hist_callback(self):
        """Callback for the button EQUALIZE HISTOGRAM
        """
        self.show_as_waiting(True)
        self.image_proc_selected('Histogram Equalization')
        self.show_as_waiting(False)

    def btn_contrast_stretch_callback(self):
        """Callback for the button CONTRAST STRETCH
        """
        self.show_as_waiting(True)
        self.image_proc_selected('Contrast Stretching')
        self.show_as_waiting(False)

    def btn_log_compress_callback(self):
        """Callback for the button LOG COMPRESS
        """
        self.show_as_waiting(True)
        self.image_proc_selected('Log Compression')
        self.show_as_waiting(False)

    def show_error(self, message: str):
        """Display error message in a window

        :param message: error message to display
        :type message: str
        """
        QMessageBox.about(self, 'Error!', message)

    def download_images_jpg(self):
        """Callback for button DOWNLOAD JPEG
        """
        self.show_as_waiting(True)
        self.download_images('JPEG')
        self.show_as_waiting(False)

    def download_images_png(self):
        """Callback for button DOWNLOAD PNG
        """
        self.show_as_waiting(True)
        self.download_images('PNG')
        self.show_as_waiting(False)

    def download_images_tiff(self):
        """Callback for button DOWNLOAD TIFF
        """
        self.show_as_waiting(True)
        self.download_images('TIFF')
        self.show_as_waiting(False)

    def download_images(self, im_format: str):
        """Download all selected images in a specified format

        If many images were selected, they are downloaded as a zip
        If only one image is selected, it is downloaded as an image

        :param im_format: format of the output images
        :type im_format: str
        """
        rows = self.tbl_images.get_selected_rows()
        ids = []
        names = []
        for r in rows:
            ids.append(self.tbl_images.item(r, 0).text())
            names.append(self.tbl_images.item(r, 1).text())

        if len(ids) == 1:

            # Create File Save Dialog
            dialog = QFileDialog(parent=self, caption='Save As..')

            dialog.setMimeTypeFilters(["image/"+im_format.lower()])
            dialog.setFileMode(QFileDialog.AnyFile)

            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.selectedFiles()[0]
                ret = api.get_download_images(ids, im_format, self.user_hash)
                if ret.get('success') is False:
                    self.show_error(ret['error_msg'])
                else:
                    image_b = b64s_to_b(ret['data'])
                    with open(filename, 'wb+') as f:
                        f.write(image_b)

        elif len(ids) >= 1:

            # Create File Save Dialog
            dialog = QFileDialog(parent=self, caption='222Save As..')
            dialog.setMimeTypeFilters(['application/zip'])
            dialog.setFileMode(QFileDialog.AnyFile)

            if dialog.exec_() == QDialog.Accepted:
                filename = dialog.selectedFiles()[0]
                ret = api.get_download_images(ids, im_format, self.user_hash)
                if ret.get('success') is False:
                    self.show_error(ret['error_msg'])
                else:
                    image_b = b64s_to_b(ret['data'])
                    with open(filename, 'wb+') as f:
                        f.write(image_b)
        else:
            return

    def tbl_images_cell_changed_callback(self, row: int, col: int):
        """This is the callback from editing any of the table cells

        :param row: edited cell row number
        :type row: int
        :param col: edited cell col number
        :type col: int
        """
        editable_cols = {
            'filename': 1,
            'description': 4
        }

        if col not in editable_cols.values():
            return

        image_id = self.tbl_images.item(row, 0).text()
        filename = self.tbl_images.item(row, 1).text()
        description = self.tbl_images.item(row, 4).text()

        if col == editable_cols['filename']:
            ret = api.edit_filename(image_id, filename, self.user_hash)
            if ret.get('success') is False:
                self.show_error(ret['error_msg'])

        elif col == editable_cols['description']:
            ret = api.edit_description(image_id, description, self.user_hash)
            if ret.get('success') is False:
                self.show_error(ret['error_msg'])

    def show_as_waiting(self, show: bool):

        if show is True:
            self.setEnabled(False)
            self.setWindowTitle('WAITING FOR SERVER')
            self.update()
            self.repaint()
        else:
            self.setEnabled(True)
            self.setWindowTitle('Image Processing Client')
