File Unzipper App
A simple and powerful desktop application built with Python to automate the process of unzipping multiple compressed folders into separate, organized directories.

Created by Ismail Ghazi.

Description
This app is a solution for developers, designers, and anyone who downloads a high volume of zip files. It streamlines your workflow, saving you from tedious manual unzipping. The modern UI provides a seamless user experience, making file management effortless.

Features
Intuitive UI: A clean, professional, and easy-to-use graphical interface.

Automated Unzipping: Unzips all .zip files from a selected source folder.

Organized Output: Creates a separate folder for each zip file, using the original filename as the new folder's name.

Smart Management: Includes options to automatically delete the original zip files and overwrite existing folders to prevent errors.

Progress Tracking: Displays a progress bar and detailed log of the unzipping process.

How to Use the Application
Download the latest version of the application from the Releases page.

Run the unzip.exe file.

Click "Select Folder" to choose the folder containing your zip files.

Click "Select Folder" to choose a destination where you want the new folders to be created.

(Optional) Select the checkboxes for additional options.

Click "Unzip All Folders" to start the process.

How to Run from Source (For Developers)
If you are a developer and have Python installed, you can run the application directly from the source code.

Clone this repository to your local machine.

Make sure you have tkinter and pyinstaller installed.

Navigate to the project folder in your terminal.

Run the application with the following command:

python unzip_app.py


Installation and Packaging
This application is packaged as a standalone executable file (.exe) using PyInstaller, which bundles the Python interpreter and all necessary libraries into a single file. This means the end-user does not need to have Python installed.

About the Author
Yourname
, a dedicated developer passionate about creating simple tools that solve real-world problems.

License
This project is licensed under the MIT License. See the LICENSE file for details.
