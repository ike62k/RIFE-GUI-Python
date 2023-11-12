import subprocess
import glob
import os
from lib.confighandler import ConfigHandler

class Pyffmpeg:
    def __init__(self, config_path: str) -> None:
        self.__config_path: str = config_path
        self.config = ConfigHandler(self.__config_path)
        self.__config_data: dict = self.config.read_all()

    #コンフィグの変更と確認とロード(ファイルパス/中身)
    @property
    def config_path(self) -> str:
        return self.__config_path
    @config_path.setter
    def config_path(self, config_path: str):
        self.__config_path: str = config_path
        self.config = ConfigHandler(self.__config_path)
        self.__config_data: dict = self.config.read_all()
    @property
    def config_data(self) -> dict:
        return self.__config_data

    #inputファイルの変更と確認
    @property
    def input_file(self) -> str:
        return self.__input_file
    @input_file.setter
    def input_file(self, input_file: str):
        self.__input_file = input_file

    #outputファイルの変更と確認
    @property
    def output_file(self) -> str:
        return self.__output_file
    @output_file.setter
    def output_file(self, output_file: str):
        self.__output_file = output_file
    
    #ffmpeg.exeの場所の変更と確認
    @property
    def ffmpegexe(self) -> str:
        return self.__ffmpegexe
    @ffmpegexe.setter
    def ffmpegexe(self, ffmpegexe: str):
        self.__ffmpegexe = ffmpegexe

    #動画→画像処理時拡張子の変更と確認
    @property
    def image_extension(self) -> str:
        return self.__image_extension
    @image_extension.setter
    def image_extension(self, image_extension: str):
        self.__image_extension = image_extension

    #補間画像→動画処理時のffmpegオプション
    @property
    def option(self) -> str:
        return self.__option
    @option.setter
    def option(self, option: str):
        self.__option = option

    def apply_input_file_from_config(self):
        if self.config_data["USER"]["input_file"] == "":
            self.input_file = self.config_data["DEFAULT"]["input_file"]
        else:
            self.input_file = self.config_data["USER"]["input_file"]

    def apply_output_file_from_config(self):
        if self.config_data["USER"]["output_file"] == "":
            self.output_file = self.config_data["DEFAULT"]["output_file"]
        else:
            self.output_file = self.config_data["USER"]["output_file"]

    def apply_ffmpegexe_from_config(self):
        if self.config_data["USER"]["ffmpegexe"] == "":
            self.ffmpegexe = self.config_data["DEFAULT"]["ffmpegexe"]
        else:
            self.ffmpegexe = self.config_data["USER"]["ffmpegexe"]

    def apply_image_extension_from_config(self):
        if self.config_data["USER"]["image_extension"] == "":
            self.image_extension = self.config_data["DEFAULT"]["image_extension"]
        else:
            self.image_extension = self.config_data["USER"]["image_extension"]

    def apply_option_from_config(self):
        if self.config_data["USER"]["option"] == "":
            self.option = self.config_data["DEFAULT"]["option"]
        else:
            self.option = self.config_data["USER"]["option"]


    def video_to_image(self):
        self._errorcheck_all()
        subprocess.run(
            f"{self.ffmpegexe} -i {self.input_file} -an {self.output_file}",
            shell=True
            )
        
    def image_to_video(self):
        self._errorcheck_all()
        subprocess.run(
            f"{self.ffmpegexe} -i {self.input_file}",
            shell=True
        )

    def search_framerate(self):
        #self._errorcheck_all()
        self.__ffprobe = subprocess.run(
            f"ffprobe -i {self.input_file} -v error -select_streams v:0 -show_entries stream=r_frame_rate -print_format csv",
            shell=True,
            capture_output=True,
            text=True
        )
        print(self.__)
        return self.__ffprobe.stdout.split(",")[1]

    class FFmpegError(Exception):
        pass

    def _errorcheck_setinputfile(self):
        try:
            self.input_file
        except:
            raise self.FFmpegError("\"input_file\" is not set. \"input_file\"が設定されていません")
        
    def _errorcheck_setoutputfile(self):
        try:
            self.output_file
        except:
            raise self.FFmpegError("\"output_file\" is not set. \"output_file\"が設定されていません")
        
    def _errorcheck_setffmpegexe(self):
        try:
            self.ffmpegexe
        except:
            raise self.FFmpegError("\"ffmpegexe\" is not set. \"ffmpegexe\"が設定されていません")
        
    def _errorcheck_setimageextension(self):
        try:
            self.image_extension
        except:
            raise self.FFmpegError("\"image_extension\" is not set. \"image_extension\"が設定されていません")
        
    def _errorcheck_setoption(self):
        try:
            self.option
        except:
            raise self.FFmpegError("\"option\" is not set. \"option\"が設定されていません")
        
    def _errorcheck_all(self):
        self._errorcheck_setinputfile()
        self._errorcheck_setoutputfile()
        self._errorcheck_setffmpegexe()
        self._errorcheck_setimageextension()
        self._errorcheck_setoption()