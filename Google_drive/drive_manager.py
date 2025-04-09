from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def authorize():
    try:        
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("Google_drive/credentials.json")
        
        if gauth.credentials is None:
            print("Geen credentials gevonden. Opnieuw inloggen vereist...")
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            print("Token verlopen. Vernieuwen...")
            gauth.Refresh()
        else:
            print("Credentials gevonden. Autorisatie succesvol.")
            gauth.Authorize()
            
        gauth.SaveCredentialsFile("Google_drive/credentials.json")
        drive = GoogleDrive(gauth)
        print("Succesvol verbonden met Google Drive!")
        return drive
    
    except Exception as e:
        print(f"Fout bij autorisatie: {e}")
        raise

def upload_naar_drive(drive, path, remote_name=None):
    try:
        if not os.path.exists(path):
            raise Exception(f"Bestand '{path}' bestaat niet.")
        
        file_name = remote_name if remote_name else os.path.basename(path)
        folder_id = "1xx9r2EV8LmGnn0XgrRA_Vr-xRjhoN_XI"
        query = f"title = '{file_name}' and trashed = false and '{folder_id}' in parents"
        
        file_list = drive.ListFile({'q': query}).GetList()
        
        if file_list:
            file = file_list[0]
            print(f"Bestand '{file_name}' bestaat al. Bestand wordt overschreven...")
        else:
            file = drive.CreateFile({'title': file_name, 
                                 'parents': [{'id': folder_id}]})
        file.SetContentFile(path)
        file.Upload()
        
        print(f"Bestand '{file_name}' geüpload naar Google Drive met ID: {file['id']}")
        
    except Exception as e:
        print(f"Fout opgetreden bij uploaden: {e}")
        raise
        
def download_bestand(drive, file_name):
    try:
        folder_id = "1xx9r2EV8LmGnn0XgrRA_Vr-xRjhoN_XI"
        query = f"title = '{file_name}' and trashed = false and '{folder_id}' in parents"
        file_list = drive.ListFile({'q': query}).GetList()
        
        if not file_list:
            raise Exception(f"Geen bestand gevonden met naam '{file_name}' in Google Drive.")
        
        print(f"Bestand '{file_name}' gevonden! Wordt gedownload naar geheugen...")
        file = file_list[0]
        
        file_content = file.GetContentFile()
        return file_content
    except Exception as e:
        print(f"Fout opgetreden bij het downloaden: {e}")
        raise