import os
from pathlib import Path
from pytube import YouTube

def ytvideo_download(LINKS,
         PROJECT_NAME='yt-videos-download',
         MAX_RESOLUTION='720p',
         MIME_TYPE='video/mp4',
         ONLY_VIDEO=False):

    # create project folder (if not present) in local directory for video storing
    VIDEO_SAVE_PATH = f'./yt_videos/{PROJECT_NAME}'
    Path(VIDEO_SAVE_PATH).mkdir(parents=True, exist_ok=True)
    # check for duplicate links
    link_list_len = len(LINKS)
    LINKS = set(LINKS)
    link_set_len = len(LINKS)
    print(f'[*] {link_list_len - link_set_len} duplicates were found - handled.')

    for index, link in enumerate(LINKS, 1):
        print(f'[+] -------- video {index} of {link_set_len} -------------')
        # output filename will be the unique videoID
        output_filename = link.split('=')[-1] + '.mp4'
        # check if video already downloaded
        if os.path.isfile(os.path.join(VIDEO_SAVE_PATH, output_filename)):
            print(f'[*] {output_filename} already downloaded.')
            continue
        yt = YouTube(link)
        avail_res_and_mime = [(stream.resolution, stream.mime_type) for stream in yt.streams.filter(progressive=True, mime_type=MIME_TYPE, only_video=ONLY_VIDEO)] #  progressive = True (searches for audio and video stream)
        res_numbs_with_correct_mime = [int(res_mime[0][:-1]) for res_mime in avail_res_and_mime if res_mime[1] == MIME_TYPE]
        highest_pos_res = 0
        for res in res_numbs_with_correct_mime:
            if res <= int(MAX_RESOLUTION[:-1]) and res > highest_pos_res:
                highest_pos_res = res
        # code to print MIME types of video available for download
        print(f'        [*] available RES and MIME:')
        for index, res in enumerate(avail_res_and_mime, 1):
            print(f'                  ({index}) {res[0]}, {res[1]}')
        print(f'        [*] {highest_pos_res}p and {MIME_TYPE} chosen since largest below MAX RES of {MAX_RESOLUTION}')
        print(f'        [+] {link} downloading..')
        target_video = yt.streams.filter(progressive=True, mime_type=MIME_TYPE, res=f'{highest_pos_res}p') \
            .desc() \
            .first()
        max_tries = 3
        tries = 0
        while (tries < max_tries):
            try:
                target_video.download(VIDEO_SAVE_PATH, filename=output_filename)
                break
            except Exception as e:
                print(f'[!!] video download error: {e}')
                print(f'[!!] try {tries} of {max_tries}')
                tries += 1
        print(f'        [+] Done. {output_filename} saved.')
    return VIDEO_SAVE_PATH


if __name__ == '__main__':
    # -------------- CHANGE HERE -------------------
    PROJECT_NAME = 'Paris_walk_test'  # generates a project folder that stores all videos from the same session
    MAX_RESOLUTION = '720p'  # will select the stream that comes closest to this parameter but will not exceed it
    MIME_TYPE = 'video/mp4'
    ONLY_VIDEO = False  # sole video streams are available in higher resolution. Coupled video and audio streams are capped at 720p!

    LINKS = [
        'https://www.youtube.com/watch?v=P7nu60agIO0',
        'https://www.youtube.com/watch?v=qezUjVNQOT8'
    ]
    # -----------------------------------------------
    ytvideo_download(LINKS, PROJECT_NAME=PROJECT_NAME,
                MAX_RESOLUTION=MAX_RESOLUTION,
                MIME_TYPE=MIME_TYPE,
                ONLY_VIDEO=ONLY_VIDEO)
