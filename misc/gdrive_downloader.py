from pydrive.auth import GoogleAuth
import sys, os
sys.path.append(os.path.split(os.getcwd())[0])
import utils

gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.

from pydrive.drive import GoogleDrive

drive = GoogleDrive(gauth)

gdrive_ids = utils.read_file("seniors.csv", "|").split("|")
for row in gdrive_ids:
    name, drive_id = row.split(",")
    print ("Downloading resume for %s id=%s" %(name, drive_id))
    # Initialize GoogleDriveFile instance with file id.
    file_obj = drive.CreateFile({'id': drive_id})
    file_obj.GetContentFile('gdrive/%s.pdf' % name)  