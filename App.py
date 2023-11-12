import os
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.pyffmpeg import Pyffmpeg
from lib.confighandler import ConfigHandler

os.chdir(os.path.dirname(__file__))
#rife = Pyrife_ncnn_vulkan(".\\setting\\pyrife_ncnn_vulkan.ini")
#rife.apply_all_from_config()
#rife.run()

ffmpeg = Pyffmpeg(".\\setting\\pyffmpeg.ini")
ffmpeg.input_file = ".\\realtest_2x.mov"
print(ffmpeg.search_framerate())