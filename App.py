import os
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.confighandler import ConfigHandler

os.chdir(os.path.dirname(__file__))
rife = Pyrife_ncnn_vulkan(".\\setting\\pyrife_ncnn_vulkan.ini")
print(rife.config_data)
print(rife.config_path)
print(rife.config_data["DEFAULT"]["rifeexe"])
rife.input_folder = ".\\target"
rife.output_folder = "testout"
print(rife.input_folder_nunber)
print(f"{rife.config_data['DEFAULT']['rifeexe']} -i {rife.input_folder}/ -o {rife.output_folder}")