import os
from django.conf import settings


def mk_gif_ffmpeg(params):
    path = settings.MEDIA_ROOT / f'{params["pk"]}'
    temp = settings.TEMP_ROOT / f'{params["pk"]}'

    args = params["params"]

    command_mkdir = f'mkdir -p {temp}'
    command_ffmpeg = f'ffmpeg -framerate {args["framerate"]} -pattern_type glob -y -i "{path}/*.png" -r 15 -vf scale=512:-1 {temp}/out.gif'
    command_del_files = f'rm {path}/*.png'
    command_move = f'mv {temp}/out.gif {path}'

    print(path, params)
    print(command_mkdir)
    os.system(command_mkdir)
    print(command_ffmpeg)
    os.system(command_ffmpeg)
    print(command_del_files)
    os.system(command_del_files)
    print(command_move)
    os.system(command_move)