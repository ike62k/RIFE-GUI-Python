import os
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.confighandler import ConfigHandler

os.chdir(os.path.dirname(__file__))
rife = Pyrife_ncnn_vulkan(".\\setting\\pyrife_ncnn_vulkan.ini")
print(rife.config_data)
print(rife.config_path)
rife.input_file = ".\\target\\*"
print(rife.input_file)
print(rife.input_size)