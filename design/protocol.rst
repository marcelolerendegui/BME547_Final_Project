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
   * - 'user_hash'
     - A String with the user hash
   * - 'data'
     - The WHOLE file converted to a 64base string.

The return value is a dictionary with following information:

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
     - String with the name of the zip file
   * - 'user_hash'
     - A String with the user hash
   * - 'data'
     - The WHOLE zip file converted to a 64base string.

The return value is a dictionary with the following information

.. list-table:: Upload Multiple Images Return Value
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
To get information about all the images stored in the server, the user must generate a GET request to *server:port/api/image_info/<User Hash>*.

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

To Download a single image, the user must generate a GET request to *server:port/api/download/* with a dictionary with the following info:

.. list-table:: Download Images Dictionary
   :widths: 20 40
   :header-rows: 1

   * - Key
     - Description
   * - 'image_ids'
     - List of Image IDs of the images to download
   * - 'format'
     - Image format to download
   * - 'user_hash'
     - A String with the user hash

If only one image ID is provided, the return value will be a string with the image coded in base64
If many image IDs are provided, the return value will be a string with a zip file with the images coded in base64

.. list-table:: Downlaod Image Return Value
   :widths: 10 40
   :header-rows: 1

   * - Key
     - Description
   * - 'sucess'
     - True / False
   * - 'error_msg'
     - String with the error message
   * - 'data'
     -  The WHOLE file converted to a 64base string.


Image Processing
------------------------

To apply any processing algorithm to an image, the user must generate a POST request to *server:port/api/img_proc/* with a dictionary the following info:

.. list-table:: Process Image Input
   :widths: 20 40
   :header-rows: 1

   * - Key
     - Description
   * - 'image_id'
     - Image IDs of the images to process
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
   * - No Algorithm

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
   * - 'processing_time'
     - Time it took to process the image
