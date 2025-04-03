from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def authorize():
    
   gauth = GoogleAuth()
   gauth.LocalWebserverAuth()
   
   drive = GoogleDrive(gauth)
   print("Succesvol verbonden met google drive")
   return drive

def upload_naar_drive(drive, path, remote_name=None):
    if not os.path.exists(path):
        print(f"Bestand niet gevonden: {path}")
        return
    
    file_name = remote_name if remote_name else os.path.basename(path)
    file = drive.CreateFile({'title': file_name})
    file.SetContentFile(path)
    file.Upload()
    print(f"Bestand '{file_name}' geüpload naar Google Drive met ID: {file['Id']}")
    
def download_bestand(drive, file_id, path):
    file = drive.CreateFile({'Id': file_id})
    file.GetContentFile(path)
    if not os.path.exists(path):
        print(f"Bestand {file} niet gevonden")
        return
    print(f"Bestand gedownload naar: {path}")
