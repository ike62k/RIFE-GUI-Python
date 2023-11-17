import os
import shutil
from tkinter import filedialog
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.pyffmpeg import Pyffmpeg
from lib.confighandler import ConfigHandler
from lib.VERSION import Version


class config():
    def __init__(self, path: str):
        self.__config = ConfigHandler(path)
        self.configdata = self.__config.read_all()

class ver():
    def __init__(self):
        self.__version = Version()

    def show(self):
        print("\n================\n")
        print("RIFE AUTOMATION TOOL PYTHON")
        print("copyright 2023 Veludo")
        print(f"Version : {self.__version.version}")
        print(self.__version.date_App)
        print("\n================\n")

class rife():
    def __init__(self, config_path: str):
        self.__config_path = config_path
        self.rife = Pyrife_ncnn_vulkan(config_path)
        self.rife.apply_all_from_config()

    def status(self):
        print("\n====RIFE STATUS====\n")
        print(f"input_folder:  {self.rife.input_folder}")
        print(f"output_folder:  {self.rife.output_folder}")
        print(f"output_extension:  {self.rife.output_extension}")
        print(f"rifeexe:  {self.rife.rifeexe}")
        print(f"rifever:  {self.rife.rifever}")
        print(f"rifeusage:  {self.rife.rifeusage}")
        print(f"rifegpu:  {self.rife.rifegpu}")
        print(f"times:  {self.rife.times}")
        print("\n================\n")

    def reload(self):
        self.rife.config_path = self.__config_path
        self.rife.apply_all_from_config()

    def interpolate(self):
        self.rife.run()


class ffmpeg():
    def __init__(self, config_path: str):
        self.__config_path = config_path
        self.ffmpeg = Pyffmpeg(config_path)
        self.ffmpeg.apply_all_from_config()

    def status(self):
        print("\n====FFmpeg STATUS====\n")
        print(f"input_file:  {self.ffmpeg.input_file}")
        print(f"input_folder:  {self.ffmpeg.input_folder}")
        print(f"output_folder:  {self.ffmpeg.output_folder}")
        print(f"complete_folder:  {self.ffmpeg.complete_folder}")
        print(f"ffmpegexe:  {self.ffmpeg.ffmpegexe}")
        print(f"ffprobeexe:  {self.ffmpeg.ffprobeexe}")
        print(f"image_extension:  {self.ffmpeg.image_extension}")
        print(f"video_extension:  {self.ffmpeg.video_extension}")
        print(f"option:  {self.ffmpeg.option}")
        print("\n================\n")

    def reload(self):
        self.ffmpeg.config_path = self.__config_path
        self.ffmpeg.apply_all_from_config()

    def vid2img(self):
        self.ffmpeg.video_to_image()
    
    def img2vid(self,times):
        self.ffmpeg.image_to_video(str(int(self.ffmpeg.get_framerate())*(2**int(times))), self.ffmpeg.get_title(False))

class main():
    def __init__(self, path):
        self.config = config(path)
        self.rife = rife(self.config.configdata["USER"]["pyrife_ncnn_vulkan_config"])
        self.ffmpeg = ffmpeg(self.config.configdata["USER"]["pyffmpeg_config"])
        self.version = ver()

    def wait(self):
        while True:
            now_input = input("入力してください> ")
            if now_input == "-help":
               self.help() 
            elif now_input == "-version":
                self.version.show()
            elif now_input == "-file":
                self.file()
                self.status()
            elif now_input == "-reload":
                self.reload()
                self.status()
            elif now_input == "-status":
                self.status()
            elif now_input == "-run":
                self.run()
                self.endcheck()
            elif now_input == "-exit":
                exit() 
            else:
                print("存在しないコマンドです。コマンド一覧は\"-help\"を参照してください")
                
    def help(self):
        print("\n====COMMAND====\n")
        print("-help: show command\n",
              "-version: show version\n"
              "-file: select file\n"
              "-reload: reload all config parameter\n",
              "-status: show all config status\n",
              "-exit: exit this software"
              )
        print("\n===============\n")
        
    def file(self):
        self.ffmpeg.ffmpeg.input_file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))

    def reload(self):
        self.rife.reload()
        self.ffmpeg.reload()
        print("Config has been reloaded!")

    def status(self):
        self.rife.status()
        self.ffmpeg.status()

    def run(self):
        print("処理を開始します")
        self.ffmpeg.vid2img()
        self.rife.interpolate()
        self.ffmpeg.img2vid(self.rife.rife.times)

    def endcheck(self):
        print("処理が完了しました")
        if input("続けて処理しますか？ [y or n]> ") in ["Y", "y"]:
            pass
        else:
            exit()
    

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    App = main(".\\setting\config.ini")
    App.wait()