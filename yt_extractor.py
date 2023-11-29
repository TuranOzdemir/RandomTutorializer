from pytube import YouTube

def get_youtube_video_info(video_url):
    try:
        # Create a YouTube object
        youtube_video = YouTube(video_url)

        # Extract main information
        main_info = {
            "video_id": youtube_video.video_id,
            "title": youtube_video.title,
            "channel": youtube_video.author,
            "view_count": youtube_video.views,
            "channel_id": youtube_video.channel_id,
            "duration": youtube_video.length,
            #"categories": youtube_video.category,
            # "tags": youtube_video.keywords,
            # "like_count": youtube_video.likes, I cant get theese infos 
        }

        return main_info

    except Exception as e:
        return {"Error": str(e)}


def download_video(video_url):
    yt_obj = YouTube(video_url)
    yt_obj = yt_obj.streams.get_highest_resolution()
    try:
        yt_obj.download()
    except:
        print("an error has occured")
    print("Download is completed successfully")
    
    
download_video('https://youtu.be/n5gItcGgIkk?si=CS7xNqRA5QlRye-N')    
# Example usage
'''
video_url = "https://www.youtube.com/live/BcbLKjWAj78?si=l-zZh0UyXFqO0gBb"

video_info = get_youtube_video_info(video_url)

if "Error" in video_info:
    print(f"Error: {video_info['Error']}")
else:
    # Access the information as needed
    for key, value in video_info.items():
            print(f"{key} : {value}")
'''        
'''
     for key, value in video_info.items():
        if key != "view_count" and key != "duration":
            print(f"{key}: {value.encode('utf-8').decode('utf-8')}")
        else:
            print(f"{key}: {value}")
'''
# Acsesing one by one
'''
print("Video Information:")
print(f"Title: {video_info['title']}")
print(f"Duration: {video_info['duration']} seconds")
print(f"Author: {video_info['author']}")
print(f"Views: {video_info['views']}")
print(f"Publish Date: {video_info['publish_date']}")
'''