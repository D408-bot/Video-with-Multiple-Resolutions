import subprocess
import cv2
import os
#im too lazy to make this code pretty
video_path = 'kermit_falling_2.mp4'
cap = cv2.VideoCapture(video_path)
frame_count_1 = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.release()

output_stream = "combined_stretched_1.h264"
if os.path.exists(output_stream):
    os.remove(output_stream)

for i in range(frame_count_1):
    width = 666 + i * 400
    height = 666 - i * 120
    cmd = [
        "ffmpeg",
        "-y",  # overwrite
        "-i", video_path,
        "-vf", f"select='eq(n\,{i})',scale={width}:{height}",
        "-frames:v", "1",
        "-f", "h264",
        "-vcodec", "libx264",
        "frame_temp.h264"
    ]
    subprocess.run(cmd, check=True)

    with open("frame_temp.h264", "rb") as temp_frame, open(output_stream, "ab") as out_stream:
        out_stream.write(temp_frame.read())

#extract video streams 
subprocess.run("ffmpeg -y -i kermit_falling_1.mp4 -an -c:v copy -f h264 combined_stretched.h264")
#combine video streams 
subprocess.run("copy /b combined_stretched.h264 + combined_stretched_1.h264 all_streams.h264", shell=True)
#wrap video stream in an mp4 container
subprocess.run("ffmpeg -y -i all_streams.h264 -c:v copy kermit_noaudio.mp4")
#add audio to final video
subprocess.run("ffmpeg -y -i kermit_noaudio.mp4 -i kermit_falling_audio.mp3 -c:v copy -c:a aac -strict experimental kermit.mp4")

#cleanup bby 
os.remove("frame_temp.h264")
os.remove("kermit_noaudio.mp4")
os.remove("combined_stretched.h264")
os.remove("combined_stretched_1.h264")
os.remove("all_streams.h264")