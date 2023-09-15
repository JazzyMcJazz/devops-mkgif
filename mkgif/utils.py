import os
from django.conf import settings


def mk_gif_ffmpeg(params):
    path = settings.MEDIA_ROOT / f'{params["pk"]}'
    temp = settings.TEMP_ROOT / f'{params["pk"]}'

    args = params["params"]

    command_mkdir = f'mkdir -p {temp}'
    command_ffmpeg_images = f'ffmpeg -framerate {args["fps"]} -pattern_type glob -y -i "{path}/*.png" -r 15 -vf scale={args["size"]}:-1 {temp}/out.gif'
    command_ffmpeg_pallette = f'ffmpeg -i "{args["video_path"]}" -filter_complex "[0:v] palettegen" {temp}/palette.png'
    command_ffmpeg_video = f'ffmpeg -i "{args["video_path"]}" -i "{temp}/palette.png" -filter_complex "[0:v] fps={args["fps"]},scale={args["size"]}:-1 [new];[new][1:v] paletteuse" {temp}/out.gif'
    command_del_files = f'rm {path}/*'
    command_move = f'mv {temp}/out.gif {path}'
    command_del_tmp = f'rm -rf {temp}'

    print(path, params)
    print(command_mkdir)
    os.system(command_mkdir)

    if args['type'] == 'video':
        print(command_ffmpeg_pallette)
        os.system(command_ffmpeg_pallette)
        print(command_ffmpeg_video)
        os.system(command_ffmpeg_video)
    else:
        print(command_ffmpeg_images)
        os.system(command_ffmpeg_images)
    print(command_del_files)
    os.system(command_del_files)
    print(command_move)
    os.system(command_move)
    print(command_del_tmp)
    os.system(command_del_tmp)