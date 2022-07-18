import os
from pytube import YouTube

def download(LINKS,
         PROJECT_NAME='yt-videos-download',
         MAX_RESOLUTION='720p',
         MIME_TYPE='video/mp4',
         VIDEO_AND_AUDIO=True):

    # create project folder (if not present) in local directory for video storing
    VIDEO_SAVE_PATH = f'./{PROJECT_NAME}'
    if not os.path.isdir(VIDEO_SAVE_PATH):
        os.mkdir(VIDEO_SAVE_PATH)
        print(f'[+] created project folder: {VIDEO_SAVE_PATH}')
    else:
        print(f'[*] project folder: {VIDEO_SAVE_PATH} already exists.')

    # check for duplicate links
    link_list_len = len(LINKS)
    LINKS = set(LINKS)
    link_set_len = len(LINKS)
    print(f'[*] {link_list_len - link_set_len} duplicates were found - handled.')

    for index, link in enumerate(LINKS, 1):
        print(f'[+] -------- video {index} of {link_set_len} -------------')
        yt = YouTube(link)
        avail_res_and_mime = [(stream.resolution, stream.mime_type) for stream in yt.streams.filter(progressive=VIDEO_AND_AUDIO)] #  progressive = True (searches for audio and video stream)
        res_numbs_with_correct_mime = [int(res_mime[0][:-1]) for res_mime in avail_res_and_mime if res_mime[1] == MIME_TYPE]
        highest_pos_res = 0
        for res in res_numbs_with_correct_mime:
            if res <= int(MAX_RESOLUTION[:-1]) and res > highest_pos_res:
                highest_pos_res = res
        print(f'        [*] available RES and MIME:')
        for index, res in enumerate(avail_res_and_mime, 1):
            print(f'                  ({index}) {res[0]}, {res[1]}')
        print(f'        [*] {highest_pos_res}p and {MIME_TYPE} chosen since largest below MAX RES of {MAX_RESOLUTION}')
        print(f'        [+] {link} downloading..')
        target_video = yt.streams.filter(progressive=False, mime_type=MIME_TYPE, res=f'{highest_pos_res}p') \
            .desc() \
            .first()
        output_fileame = "".join(x for x in target_video.default_filename
                                 if ord(x) < 128 and
                                    x not in '{}[]()`~:;,*"+-!?=$£@¦|').replace(' ', '_')
        target_video.download(VIDEO_SAVE_PATH, filename=output_fileame)
        print(f'        [+] Done. {output_fileame} saved.')


if __name__ == '__main__':
    # -------------- CHANGE HERE -------------------
    PROJECT_NAME = 'quality_content_videos'  # generates a project folder that stores all videos from the same session
    MAX_RESOLUTION = '1080p'  # will select the stream that comes closest to this parameter but will not exceed it
    MIME_TYPE = 'video/mp4'
    VIDEO_AND_AUDIO = True  # sole video streams are available in higher resolution. Coupled video and audio streams are capped at 720p!

    LINKS = [
        'https://www.youtube.com/watch?v=oT3mCybbhf0',
        'https://www.youtube.com/watch?v=68ugkg9RePc'
    ]
    # -----------------------------------------------
    download(LINKS, PROJECT_NAME=PROJECT_NAME,
                MAX_RESOLUTION=MAX_RESOLUTION,
                MIME_TYPE=MIME_TYPE,
                VIDEO_AND_AUDIO=VIDEO_AND_AUDIO)
