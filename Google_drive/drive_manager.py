from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def authorize():
    try:
        orginele_dir = os.getcwdb()
        os.chdir("Google_drive")
        
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("credentials.txt")
        
        if gauth.credentials is None:
            print("Geen credentials gevonden. Opnieuw inloggen vereist...")
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            print("Token verlopen. Vernieuwen...")
            gauth.Refresh()
        else:
            print("Credentials gevonden. Autorisatie succesvol.")
            gauth.Authorize()
        
        gauth.SaveCredentialsFile("credentials.txt")
        drive = GoogleDrive(gauth)
        print("Succesvol verbonden met Google Drive!")
        os.chdir(orginele_dir) #Directory terugzetten naar originele
        return drive
    except Exception as e:
        print(f"Fout bij autorisatie: {e}")
        return None

def upload_naar_drive(drive, path, remote_name=None):
    try:
        if not os.path.exists(path):
            print(f"Bestand niet gevonden: {path}")
            return
        
        file_name = remote_name if remote_name else os.path.basename(path)
        file = drive.CreateFile({'title': file_name})
        file.SetContentFile(path)
        file.Upload()
        
        print(f"Bestand '{file_name}' geüpload naar Google Drive met ID: {file['id']}")
        
    except Exception as e:
        print(f"Fout opgetreden bij uploaden: {e}")
        
def download_bestand(drive, file_id, path):
    try:
        file = drive.CreateFile({'id': file_id})
        file.GetContentFile(path)
        
        if os.path.exists(path):
            print(f"Bestand succesvol gedownload naar: {path}")
        else:
            print(f"Path '{path}' niet gevonden.")
            
    except Exception as e:
        print(f"Fout opgetreden bij downloaden van bestand: {e}")