import os
import shutil
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.pyffmpeg import Pyffmpeg
from lib.confighandler import ConfigHandler

os.chdir(os.path.dirname(__file__))
rife = Pyrife_ncnn_vulkan(".\\setting\\pyrife_ncnn_vulkan.ini")
rife.apply_all_from_config()
ffmpeg = Pyffmpeg(".\\setting\\pyffmpeg.ini")
ffmpeg.apply_all_from_config()

ffmpeg.video_to_image()
rife.run()
ffmpeg.image_to_video()

shutil.rmtree(ffmpeg.input_folder)
shutil.rmtree(ffmpeg.output_folder)