import csv
import json
import requests

channel_id = <CHANNEL ID>
youtube_api_key = <YOUR KEY>

def create_csv(channel_id):
    base = 'https://www.googleapis.com/youtube/v3/search?'
    fields = 'part=snippet&channelID='
    api_key = '&key=' + youtube_api_key
    url = base + fields + channel_id + api_key     
    api_response = requests.get(url)
    videos = json.loads(api_response.text)
    with open('youtube_channel_data.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['publishedAt', 'title', 'description', 'thumbnailurl'])
        has_another_page = True
        while has_another_page: 
            if videos.get('items') is not None:
                for video in videos.get('items'):
                    video_data_row = [
                        video['snippet']['publishedAt'], 
                        video['snippet']['title'],
                        video['snippet']['description'],
                        video['snippet']['thumbnails']['default']['url']]
                    csv_writer.writerow(video_data_row)
            if "nextPageToken" in videos.keys():
                next_page_url = url + '&pageToken=' + videos['nextPageToken']
                next_page_posts = requests.get(next_page_url)
                videos = json.loads(next_page_posts.text)
            else: 
                print('No more videos!') 
                has_another_page = False 

create_csv(channel_id)

"""Based on an exercise in Lam Thuy Vo's "Mining Social Media", No Starch Press, 2020"""
