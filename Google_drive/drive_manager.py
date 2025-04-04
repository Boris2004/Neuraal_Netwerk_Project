from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

def authorize():
    try:
        orginele_dir = os.getcwdb()
        
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
        file = drive.CreateFile({'title': file_name})
        file.SetContentFile(path)
        file.Upload()
        
        print(f"Bestand '{file_name}' geüpload naar Google Drive met ID: {file['id']}")
        
    except Exception as e:
        print(f"Fout opgetreden bij uploaden: {e}")
        raise
        
def download_bestand(drive, file_id, path):
    try:
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(path)
        
        if os.path.exists(path):
            print(f"Bestand succesvol gedownload naar: {path}")
        else:
            raise(Exception(f"Path '{path}' niet gevonden."))
            
    except Exception as e:
        print(f"Fout opgetreden bij downloaden van bestand: {e}")
        raise