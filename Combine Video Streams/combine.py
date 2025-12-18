from pathlib import Path
import subprocess, os

folder_name = "Videos" #Name of folder with videos
script_dir = Path(__file__).resolve().parent
video_directory = script_dir / folder_name

#Extract video stream data
for file in video_directory.iterdir():
    if file.is_file():
        file_dir = str(file)
        file_without_extension = str(file_dir).rsplit('.', 1)[0]
        print(file_without_extension)
        subprocess.run(f'ffmpeg -i "{file_dir}" "{file_without_extension}.h264"', shell=True)
    else:
        continue

#Combine video streams
video_streams = []
for file in video_directory.iterdir():
    file_dir = str(file)
    if file.is_file():
        if file_dir.endswith(".h264"):
            video_streams.append(file_dir)
        else:
            continue

with open("Videos/all_parts_combined.h264", "wb") as out:
    for f in video_streams:
        with open(f, "rb") as part:
            out.write(part.read())
    path_to_video_streams = video_directory / "all_parts_combined.h264"
    subprocess.run(f'ffmpeg -i "{path_to_video_streams}" -c:v copy final_video.mp4')

#Cleaning up video stream files
for file in video_directory.iterdir():
    file_dir = str(file)
    if file.is_file():
        if file_dir.endswith(".h264"):
            os.remove(file_dir)