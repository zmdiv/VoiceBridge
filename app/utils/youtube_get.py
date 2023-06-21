import os
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from pytube import YouTube

def get_video_details(video_id):
    """
    Retrieves the details of a YouTube video using the video ID.
    Returns a dictionary containing the video title, description, transcript, and video file path.
    """
    api_key = os.getenv('YOUTUBE_API_KEY')  # Replace with your YouTube Data API key

    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    try:
        response = youtube.videos().list(
            part='snippet, contentDetails',
            id=video_id
        ).execute()

        video_info = response['items'][0]['snippet']
        video_title = video_info['title']
        video_description = video_info['description']

        transcript = get_video_transcript(video_id)

        # Download the video file
        video_file_path = download_video(video_id)

        return {
            'title': video_title,
            'description': video_description,
            'transcript': transcript,
            'video_file_path': video_file_path
        }
    except HttpError as e:
        print(f'An error occurred: {e}')
        return None

def get_video_transcript(video_id):
    """
    Retrieves the transcript of a YouTube video using the video ID.
    Returns a string containing the video's transcript.
    """
    api_key = os.getenv('YOUTUBE_API_KEY')  # Replace with your YouTube Data API key

    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

    try:
        captions = youtube.captions().list(
            part='id',
            videoId=video_id
        ).execute()

        caption_id = captions['items'][0]['id']

        caption_request = youtube.captions().download(
            id=caption_id
        )

        caption_response = caption_request.execute()

        transcript = caption_response['body']

        return transcript
    except HttpError as e:
        print(f'An error occurred: {e}')
        return None

def download_video(video_id):
    """
    Downloads the YouTube video using the video ID.
    Returns the file path of the downloaded video.
    """
    youtube_link = f'https://www.youtube.com/watch?v={video_id}'
    save_directory = 'videos'  # Set the directory where you want to save the video

    try:
        yt = YouTube(youtube_link)
        video = yt.streams.get_highest_resolution()

        # Create the save directory if it doesn't exist
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Download the video
        video_file = video.download(output_path=save_directory, filename=video_id)

        return video_file
    except Exception as e:
        print(f'An error occurred: {e}')
        return None
