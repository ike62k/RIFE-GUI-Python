import os
import shutil
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.pyffmpeg import Pyffmpeg
from lib.confighandler import ConfigHandler
from tkinter import filedialog

class main:
    def __init__(self, config_path: str) -> None:
        self.__config_path = config_path
        self.__config = ConfigHandler(self.__config_path)
        self.__config_data: dict = self.__config.read_all()
        if self.__config_data["USER"]["pyrife_ncnn_vulkan_config"] == "":
            self.__pyrife_ncnn_vulkan_config = self.__config_data["DEFAULT"]["pyrife_ncnn_vulkan_config"]
        else:
            self.__pyrife_ncnn_vulkan_config = self.__config_data["USER"]["pyrife_ncnn_vulkan_config"]
        if self.__config_data["USER"]["pyffmpeg_config"] == "":
            self.__pyffmpeg_config = self.__config_data["DEFAULT"]["pyffmpeg_config"]
        else:
            self.__pyffmpeg_config = self.__config_data["USER"]["pyffmpeg_config"]

    def create_instance_rife(self):
        self.rife = Pyrife_ncnn_vulkan(self.__pyrife_ncnn_vulkan_config)
        self.rife.apply_all_from_config()
    
    def create_instance_ffmpeg(self):
        self.ffmpeg = Pyffmpeg(self.__pyffmpeg_config)
        self.ffmpeg.apply_all_from_config()

    def run_all_process(self):
        self.ffmpeg.video_to_image()
        self.rife.run()
        self.ffmpeg.image_to_video()

    def crean_ffmpeg_folder(self):
        shutil.rmtree(self.ffmpeg.input_folder)
        shutil.rmtree(self.ffmpeg.output_folder)

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    runner = main(".\\setting\config.ini")
    runner.create_instance_ffmpeg()
    runner.create_instance_rife()
    while True:
        print("補完する動画を選んでください")
        runner.ffmpeg.input_file = filedialog.askopenfile()
        if not runner.ffmpeg.input_file == None:
            break
    runner.run_all_process()
    runner.crean_ffmpeg_folder()