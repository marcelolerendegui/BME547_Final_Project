# BME547_Final_Project [![Build Status](https://travis-ci.com/marcelolerendegui/BME547_Final_Project.svg?token=y2E3CUdmbCCXpxoiT8Pe&branch=master)](https://travis-ci.com/marcelolerendegui/BME547_Final_Project)
Final project for Spring 2019 - BME 547 Medical Software Design

*Due date: Monday, April 29, 2019 9:00 AM EST*

## Project files and functionaliies
* client folder: Contains GUI code and api calls to reach out to the server 
* core folder: Contains image processing algorithm functional code, verification for the functions, SHA256 encryption code and testing folder for the functions
* server folder: Contains server code, database code and function testing folder

## Running the Server Locally
To run the server locally without the VCM for test, go to server/_main_ and 
change api_host, comment `app.run(host="0.0.0.0")` and add the following code 
to use instead: `app.run(host="127.0.0.1")` 

Then, go to client/api_calls, comment `api_host = "http://vcm-8214.vm.duke.edu:5000/"` 
and uncomment `api_host = "http://127.0.0.1:5000"`

Then the user will be able to run code: `python -m server` in python shell 
to deploy a local server.
## Using the Image Processor Interface
In order to run the software properly, fork or clone the repository and ensure you have saved the client and core folder and requirements installed.

*The VM server should already be on as you are reviewing this project.*

To deploy the server remotely in a VM. We comment the local api_host and comment
the VM: `http://vcm-8214.vm.duke.edu:5000/`.

Then start the GUI by running the client folder by running code `python -m client` 
in a python shell. The user can either open a CMD and direct to project folder 
then run the code or open a python interpreter(pycharm for instance) then run 
the code in the terminal window. 

Before you get access to the main window, you will be asked to type in your user name and password for verification. Images are saved for specific users. Entering a none exist user/password will not generate the previous images saved.

After logging in, next window shown will be the main user interface. The table contains items: image ID, Filename, image Format, Size, Description, Timestamp when image upload and Image process time.
Below includes all function buttons as stated in assignment requirement.

For new users, upload a new image by clicking the upload button and either 
upload a single image or a zip file. The images and image information will then appear on the table. 

Begin image processing by selecting on a image* and click on your desire processing algorithm. The process time will pop up. Then go to the end row of table, select the new generated image and click  `Display`
 button to show processed image. Note that your processed image can be traced 
 at the end of table which is as well stored in server.

#####  Note: Image can only be selected successfully  by clicking on the whole row, for selecting multiple images, please click and hold on pressing  `Ctrl` before you choose the next image 

The size, upload timestamp will be shown on table as well.

To display histogram and color histogram, select one or multiple images and 
click on `Display HIST` or `Display Color HIST`.

To compare between multiple images, select the image(s) needed to compare and 
click on display button, a additional image will pop up for comparison.

After processing with the images, the user can download the images locally in
`JPEG`, `PNG`, `TIFF` by clicking either of the three download buttons for 
specific format. By selecting multiple images, user can download the images in
zip file.

## Demonstration video
To watch the demo video, please visit https://www.youtube.com/watch?v=cAMOWa8OCoE&t=119s
*PS:Additional setup files for the project structure and assignees in the project 
can be find in Setup.rst*
