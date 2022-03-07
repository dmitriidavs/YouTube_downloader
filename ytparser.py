import json
from yt_dlp import YoutubeDL
import os
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def best_format_selector(ctx):
    formats = ctx.get('formats')[::-1]
    best_video = next(f for f in formats if f['vcodec'] != 'none' and f['acodec'] == 'none')
    audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
    best_audio = next(f for f in formats if (f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))
    yield {
        'format_id': f'{best_video["format_id"]} + {best_audio["format_id"]}',
        'ext': best_video['ext'],
        'requested_formats': [best_video, best_audio],
        'protocol': f'{best_video["protocol"]} + {best_audio["protocol"]}'
    }

def custom_hook(d):
    if d['status'] == 'finished':
        print('\nDone downloading, next video ...')

try:
    with open('yt_config.json', encoding = 'utf-8') as file:
        yt_content_dict = json.load(file)
        yt_content_dict.popitem()

    for content_key in yt_content_dict:
        if content_key in ["channels", "playlists", "videos"]:
            content_dict = yt_content_dict[content_key]
            CONTENT_list = content_dict["content_by_name"]
            CONTENT_dir = content_dict["config"][0]
            CONTENT_res = content_dict["config"][1]
        else:
            print(f'Unsupported Content Type: {bcolors.FAIL}{content_key}{bcolors.ENDC}')
            continue

        if CONTENT_res == "best":
            CONTENT_res = best_format_selector
        else:
            CONTENT_res = f'[height <= {CONTENT_res}]'

        if content_key in ["channels", "playlists"]:
            for key, value in CONTENT_list.items():
                current_dir = os.path.join(CONTENT_dir, key)
                if not os.path.exists(current_dir):
                    os.makedirs(current_dir)

                print(f'\nDownloading {content_key}: {bcolors.OKGREEN}{key}{bcolors.ENDC}')
                if value[1] != 69:
                    ydl_opts = {
                        "format": CONTENT_res,
                        'progress_hooks': [custom_hook],
                        'outtmpl': f'{current_dir}/%(title)s.%(ext)s',
                        'max_downloads': value[1]
                    }
                else:
                    ydl_opts = {
                        "format": CONTENT_res,
                        'progress_hooks': [custom_hook],
                        'outtmpl': f'{current_dir}/%(title)s.%(ext)s'
                    }

                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.cache.remove()
                        ydl.download([value[0]])
                except KeyboardInterrupt:
                    break
                except:
                    print(f'Download Error: {value[0]}, next video ...')

        elif content_key == 'videos':
            for video_url in CONTENT_list:
                if not os.path.exists(CONTENT_dir):
                    os.makedirs(CONTENT_dir)

                print(f'\nDownloading {content_key}: {bcolors.OKGREEN}{video_url}{bcolors.ENDC}')
                ydl_opts = {
                    "format": CONTENT_res,
                    'progress_hooks': [custom_hook],
                    'outtmpl': f'{CONTENT_dir}/%(title)s.%(ext)s'
                }
                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        ydl.cache.remove()
                        ydl.download([video_url])
                except KeyboardInterrupt:
                    break
                except:
                    print(f'Download Error: {value[0]}, next video ...')
except Exception as e:
    print(str(e))
    time.sleep(10)

"""
    если не хватит места - сами виноваты ;-)
"""
