''' To automate this press windows+ R. In the run window, type "shell:startup" 
    add this file there, so everytime you start your computer, it's running in the bg
'''

from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# Source_dir is whichever directory or folder you want to organise, add that path here.
# if \ doesn't work then try with \\
source_dir = "C:\\Users\\gauth\\Downloads"
dest_dir_sfx = "C:\\Users\\gauth\\Downloads\\Downloaded sfx"
dest_dir_music = "C:\\Users\\gauth\\Downloads\\Downloaded music"
dest_dir_video = "C:\\Users\\gauth\\Downloads\\Downloaded Vids"
dest_dir_image = "C:\\Users\\gauth\\Downloads\\Downlaoded pics"
dest_dir_documents = "C:\\Users\\gauth\\Downloads\\Downloaded Docs"
dest_dir_installables="C:\\Users\\gauth\\Downloads\\Installables"

# image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd",".mkv"]
# Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

installable_extensions=[".rar", ".zip", ".exe", ".msi"]


def move_file(dest, file_name, name):
    if exists(f"{dest}\\{name}"):
    #    unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        #newName = join(dest, unique_name)
        #rename(oldName, newName)
    move(file_name, dest)


class MoverHandler(FileSystemEventHandler):
    # THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    def on_modified(self, event):
        with scandir(source_dir) as file_names:
            for file_name in file_names:
                name = file_name.name
                self.check_audio_files(file_name, name)
                self.check_video_files(file_name, name)
                self.check_image_files(file_name, name)
                self.check_document_files(file_name, name)

    def check_audio_files(self, file_name, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension):
                if file_name.stat().st_size < 10_000_000 or "SFX" in name:  
                    dest = dest_dir_sfx
                else:
                    dest = dest_dir_music
                move_file(dest, file_name, name)
                logging.info(f"Moved audio file: {name}")

    def check_video_files(self, file_name, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) :
                move_file(dest_dir_video, file_name, name)
                logging.info(f"Moved video file: {name}")

    def check_image_files(self, file_name, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension):
                move_file(dest_dir_image, file_name, name)
                logging.info(f"Moved image file: {name}")

    def check_document_files(self, file_name, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) :
                move_file(dest_dir_documents, file_name, name)
                logging.info(f"Moved document file: {name}")

    def check_document_files(self, file_name, name):  # * Checks all Document Files
        for installable_extension in installable_extensions:
            if name.endswith(installable_extension) :
                move_file(dest_dir_installables, file_name, name)
                logging.info(f"Moved document file: {name}")


# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
