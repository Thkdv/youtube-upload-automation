import os
import pickle
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# 1. THE OOP ARCHITECTURE
class YouTubeVideo:
    """Represents a video with scheduling metadata"""
    def __init__(self, file_path, title, description, tags, publish_time=None, category_id="22"):
        self.file_path = file_path
        self.title = title
        self.description = description
        self.tags = tags          
        self.category_id = category_id  
        self.publish_time = publish_time  # Expects a string timestamp or None

    def to_api_body(self):
        """Converts our data into the JSON format YouTube expects"""
        body = {
            "snippet": {
                "title": self.title,
                "description": self.description,
                "tags": self.tags,
                "categoryId": self.category_id
            },
            "status": {
                "privacyStatus": "private"  # Must be private or unlisted to allow scheduling
            }
        }
        
        # If a schedule time is provided, inject it into the upload rules!
        if self.publish_time:
            body["status"]["publishAt"] = self.publish_time
            
        return body

class AutomationEngine:
    """Handles communications with the YouTube API"""
    def __init__(self, credentials):
        self.youtube_client = build("youtube", "v3", credentials=credentials)

    def upload_single_video(self, video_object: YouTubeVideo):
        """Executes a POST request to upload and schedule the video"""
        print(f"\nPreparing upload for: {video_object.title}")
        if video_object.publish_time:
            print(f"Scheduled Release Time: {video_object.publish_time}")
        else:
            print("Release Mode: Instant Private")
        
        if not os.path.exists(video_object.file_path):
            print(f"ERROR: Video file not found at {video_object.file_path}")
            return None

        media = MediaFileUpload(video_object.file_path, chunksize=-1, resumable=True)

        request = self.youtube_client.videos().insert(
            part="snippet,status",
            body=video_object.to_api_body(),
            media_body=media
        )

        print("Sending bits to YouTube servers...")
        response = request.execute()
        print(f"Success! Video ID: {response.get('id')}")
        return response

# 2. THE OAUTH FLOW
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_credentials():
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)
    return credentials

# 3. SCHEDULE SCHEMING EXECUTION
if __name__ == "__main__":
    #CONFIGURATION NOTE: This automation engine requires a 'client_secret.json' file 
    # generated from the Google Cloud Console to establish secure API handshakes.
    # For security reasons, this file is excluded from GitHub. Authorized users 
    # must obtain their own client secrets or request access credentials directly from the me (developer).
    
    # Authenticate with Google Cloud
    creds = get_authenticated_credentials()
    engine = AutomationEngine(credentials=creds)
    
    print("\n==============================================")
    print("YOUTUBE AUTOMATION UPLOADER & SCHEDULER ACTIVE")
    print("==============================================")
    
    # 1. ASK USER FOR THE TARGET FOLDER DYNAMICALLY
    user_path = input("Paste or type the full path to your video folder: ")
    
    # Clean up any accidental quote marks from copying/pasting paths in Windows
    target_folder = user_path.strip('\'"')
    
    # 2. AUTOMATED FOLDER SCANNING
    if not os.path.exists(target_folder):
        print(f"Error: The directory '{target_folder}' does not exist! Check the path and try again.")
        exit()
        
    raw_files = os.listdir(target_folder)
    # Gathers only valid .mp4 video files
    stacked_videos = [os.path.join(target_folder, file) for file in raw_files if file.lower().endswith('.mp4')]
    
    if not stacked_videos:
        print(f"Folder found, but it's empty! Drop some .mp4 files inside '{target_folder}' and re-run.")
        exit()
        
    print(f"\nDetected {len(stacked_videos)} videos inside the folder. Commencing scheduling pipeline...")

    # 3. SCHEDULING CONFIGURATION
    videos_per_day = 3
    start_date = datetime.now() + timedelta(days=1)  # Starts scheduling starting tomorrow
    hours_to_post = [9, 13, 17]  # 9:00 AM, 1:00 PM, 5:00 PM
    
    # 4. LOOP AND UPLOAD
    for index, file_path in enumerate(stacked_videos):
        # Calculate calendar slots
        day_offset = index // videos_per_day       
        time_slot = index % videos_per_day         
        
        target_date = start_date + timedelta(days=day_offset)
        scheduled_hour = hours_to_post[time_slot]
        
        release_datetime = target_date.replace(hour=scheduled_hour, minute=0, second=0, microsecond=0)
        iso_timestamp = release_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Format a clean title from the filename
        clean_title = os.path.splitext(os.path.basename(file_path))[0].replace("_", " ").title()
        
        # Build the OOP video object
        video_obj = YouTubeVideo(
            file_path=file_path,
            title=clean_title,
            description="Automated upload managed entirely by a Python script backend pipeline.",
            tags=["automation", "shorts"],
            publish_time=iso_timestamp
        )
        
        # Fire it off to the YouTube API!
        engine.upload_single_video(video_obj)
        
    print("\nAll uploads inside the folder have been fully processed and scheduled!")
