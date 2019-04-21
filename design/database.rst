Database
========

We are going to use MongoDB online as the database for our server.

MongoDB Model Image
--------------------

.. list-table:: Image
   :widths: 5 30 10
   :header-rows: 1

   * - Name
     - Description
     - Field Type
   * - ID
     - Unique id for each image
     - numeric string / integer
   * - Filename
     - Name of the file
     - string
   * - Format
     - encoding of the image. Can be either: PNG, JPEG, TIFF
     - string
   * - Size
     - size of the image in pixels expressed in IxJ, with numbers I,J representing width and height
     - string
   * - Timestamp
     - Date and time at which the image was stored in the server
     - timestamp format/string
   * - Description
     - User description of the image.
     - string
   * - User Hash
     - A hash that identifies a unique user who is the owner of the image
     - string
   * - Data
     - Actual information in the file containing ALL bytes (including image format metadata)
     - string coded in base64
