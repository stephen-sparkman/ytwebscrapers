from pytube import YouTube
from pytube import Playlist
from pytube import Channel
import os

#Creating playlist downloader
def playlist(url):
    playlist_caller = Playlist(url)
    print(f'Number of videos in playlist: %s' % len(playlist.video_urls))
    print('Downloading...\n-----\n')
    for video in playlist.videos:
      playlist_caller.streams.filter(progressive=True,
      file_extension='mp4').order_by(
        'resolution').desc().first().download()
      print('Done!!')
        
#Creating video downloader
def video(url):
    video_caller = YouTube(url)
    print('-----\n',video_caller.title,'\nDownloading...\n')
    print()
    video_caller.streams.filter(progressive=True,
                                file_extension='mp4').order_by(
        'resolution').desc().first().download()
    print('-----\nDone!\n=====')

#Creating channel downloader
def channel(url):
    channel_videos = Channel(url)
    print(f'-----\nDownloading videos by: {channel_videos.channel_name}\nDownloading...\n-----')
    for video in channel_videos.videos:
        video.streams.first().download()
        print('Done!!')

#Creating audio downloader
def video_voice_only(url):
    video_caller = YouTube(url)
    print(video_caller.title)
    print('Downloading...')
    audio = video_caller.streams.filter(only_audio=True).first()
    out_path = audio.download(output_path=video_caller.title)
    new_name = os.path.splitext(out_path)
    os.rename(out_path,new_name[0] + '.mp3')
    print('Done!!')

#Creating image downloader
def picture_only(url):
    video_caller = YouTube(url)
    print(video_caller.title)
    print('Downloading...')
    video = video_caller.streams.filter(only_video=True).first()
    out_path = video.download(output_path=video_caller.title)
    new_name = os.path.splitext(out_path)
    os.rename(out_path,new_name[0] + 'mp4')
    print('Done!!')

#Function caller
if __name__ == '__main__':
    while True: # Keep asking for input
        required = input('''=====\nEnter...
'playlist' to download an entire playlist;
'video' to download a video;
'channel' to download all videos from a channel;
'voice' to download only the voice file;
'picture' to download the thumbnail for a video\n And 'q' to quit\n=====\n''')
        if required=='playlist':
            url = input('Enter the url for whole playlist\n')
            playlist(url=url)
            break # Exit loop
        elif required=='video':
            url = input('-----\nEnter the url of the video\n')
            video(url=url)
            break
        elif required=='channel':
            url = input('-----\nEnter the url of the channel\n')
            channel(url=url)
            break
        elif required == 'voice':
            url = input('Enter the url of the video\n')
            video_voice_only(url)
            break
        elif required == 'picture':
            url = input('Enter the url of the video\n')
            picture_only(url)
            break
        elif required == 'q':
            print("Thank you!")
            print("=====")
            exit()
        else:
            print('\n=====\n\nInvalid\n\nPlease follow instructions clearly\n')
