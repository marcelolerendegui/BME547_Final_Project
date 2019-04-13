REST API Methods
====================


Upload Image
------------

To upload a single image, the user must generate a POST request to *server:port/api/upload/image* with the following info in a dictionary:

.. list-table:: Upload Image Dictionary
   :widths: 20 40
   :header-rows: 1

   * - Key
     - Description
   * - 'filename'
     - String with the name of the file
   * - 'format'
     - String with the format of the file: PNG, JPEG or TIFF
   * - 'description'
     - String with any user description of the image
   * - 'data'
     - The WHOLE file converted to a 64base string.

The return value is a tuple with the status and string:

.. list-table:: Upload Image Return Value
   :widths: 10 40
   :header-rows: 1

   * - Key
     - Description
   * - 'sucess'
     - True / False
   * - 'error_msg'
     - String with the error message


Upload Multiple Images
------------------------

To upload multiple images, the user must generate a POST request to *server:port/api/upload/zip* with the following info in a dictionary:

.. list-table:: Upload Images Zip Dictionary
   :widths: 20 40
   :header-rows: 1

   * - Key
     - Description
   * - 'filename'
     - List of strings with the name of the files
   * - 'format'
     - List of strings with the format of the files: PNG, JPEG or TIFF
   * - 'description'
     - List of strings with any user description of the images
   * - 'data'
     - The WHOLE zip file converted to a 64base string.

The return value is a tuple with the status and string:

.. list-table:: Upload Image Return Value
   :widths: 10 40
   :header-rows: 1

   * - Key
     - Description
   * - 'sucess'
     - True / False
   * - 'error_msg'
     - String with the error message


Get Images Info
---------------
To get information about all the images stored in the server, the user must generate a GET request to *server:port/api/image_info/all*.

The return value is a dictionary with a key for each image in the server. That key is the Image ID, and each value is a dictionary with the following information:

.. list-table:: Image Info Return Dictionary
   :widths: 10 40
   :header-rows: 1

   * - Key
     - Description
   * - "filename"
     - Filename of the image
   * - "format"
     - Format of the image
   * - "timestamp"
     - Timestamp of the image
   * - "size"
     - Size of the image
   * - "description"
     - Description of the image


Download Image
----------------

To Download a single image, the user must generate a GET request to *server:port/api/download/* with a dictionary with a key (image ID) for each image to download, each value must be dictionary with the following info:

.. list-table:: Download Images Dictionary
   :widths: 20 40
   :header-rows: 1

   * - Key
     - Description
   * - 'format'
     - Image format to download

If only one image ID is provided, the return value will be a string with the image coded in base64
If many image IDs are provided, the return value will be a string with a zip file with the images coded in base64


Image Processing
------------------------


To apply any processing algorithm to an image, the user must generate a POST request to *server:port/api/hist_eq/* with a dictionary with a key (image ID) for each image to process. Each value must have the following info:

.. list-table:: Process Image Input
   :widths: 20 40
   :header-rows: 1

   * - Key
     - Description
   * - 'algorithm'
     - Algorithm to apply to the image
   * - 'out_image_format'
     - Format of the output processed image
   * - 'out_image_filename'
     - Filename of the output processed image

The algorithm can be any of the following:

.. list-table:: Algorithms

   * - Histogram Equalization
   * - Contrast Stretching
   * - Log Compression
   * - Contrast Invert
   * - Just Convert
   * - Rename

The return value is a list with a dictionary with a key (image ID) for each image the user sent to proces. Each element has the following info:

.. list-table:: Process Image Return
   :widths: 20 40
   :header-rows: 1

   * - Key
     - Description
   * - 'success'
     - True / False
   * - 'error_msg'
     - String with the error message
   * - 'image_id'
     - Image ID of the output processed image
