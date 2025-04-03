from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authorize():
    
   gauth = GoogleAuth()
   gauth.LocalWebserverAuth()
   
   drive = GoogleDrive(gauth)
   print("Succesvol verbonden met de google drive")
   return drive

def upload_naar_drive(drive, file_path, folder_id=None):
    
    file_drive = drive.CreateFile({'title': file_path.split("/")[-1]})
    
    if folder_id:
        file_drive['parents'] = [{'id': folder_id}]
        
    file_drive.Upload()
    print(f"Bestand {file_path} succesvol geüpload naar Google Drive.")
