import subprocess
import glob
import os
import shutil
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

    #inputフォルダの変更と確認
    @property
    def input_folder(self) -> str:
        return self.__input_folder
    @input_folder.setter
    def input_folder(self, input_folder: str, make_directory:bool = True):
        self.__input_folder = input_folder
        if make_directory:
            os.makedirs(input_folder, exist_ok=True)
    @property
    def input_folder_nunber(self) -> int:
        return len(glob.glob(f"{self.input_folder}\\*"))

    #outputフォルダの変更と確認
    @property
    def output_folder(self) -> str:
        return self.__output_folder
    @output_folder.setter
    def output_folder(self, output_folder: str, make_directory: bool = True):
        self.__output_folder = output_folder
        if make_directory:
            os.makedirs(output_folder, exist_ok=True)

    #完成動画ファイルの変更と確認
    @property
    def complete_folder(self) -> str:
        return self.__complete_folder
    @complete_folder.setter
    def complete_folder(self, complete_folder: str, make_directory: bool = True):
        self.__complete_folder = complete_folder
    
    #ffmpeg.exeの場所の変更と確認
    @property
    def ffmpegexe(self) -> str:
        return self.__ffmpegexe
    @ffmpegexe.setter
    def ffmpegexe(self, ffmpegexe: str):
        self.__ffmpegexe = ffmpegexe

    #ffprobe.exeの場所の変更と確認
    @property
    def ffprobeexe(self) -> str:
        return self.__ffprobeexe
    @ffprobeexe.setter
    def ffprobeexe(self, ffprobeexe: str):
        self.__ffprobeexe = ffprobeexe

    #動画→画像処理時拡張子の変更と確認
    @property
    def image_extension(self) -> str:
        return self.__image_extension
    @image_extension.setter
    def image_extension(self, image_extension: str):
        self.__image_extension = image_extension

    #画像→動画処理時拡張子の変更と確認
    @property
    def video_extension(self) -> str:
        return self.__video_extension
    @video_extension.setter
    def video_extension(self, video_extension: str):
        self.__video_extension = video_extension

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
    
    def apply_input_folder_from_config(self):
        if self.config_data["USER"]["input_folder"] == "":
            self.input_folder = self.config_data["DEFAULT"]["input_folder"]
        else:
            self.input_folder = self.config_data["USER"]["input_folder"]

    def apply_output_folder_from_config(self):
        if self.config_data["USER"]["output_folder"] == "":
            self.output_folder = self.config_data["DEFAULT"]["output_folder"]
        else:
            self.output_folder = self.config_data["USER"]["output_folder"]

    def apply_complete_folder_from_config(self):
        if self.config_data["USER"]["complete_folder"] == "":
            self.complete_folder = self.config_data["DEFAULT"]["complete_folder"]
        else:
            self.complete_folder = self.config_data["USER"]["complete_folder"]

    def apply_ffmpegexe_from_config(self):
        if self.config_data["USER"]["ffmpegexe"] == "":
            self.ffmpegexe = self.config_data["DEFAULT"]["ffmpegexe"]
        else:
            self.ffmpegexe = self.config_data["USER"]["ffmpegexe"]

    def apply_ffprobeexe_from_config(self):
        if self.config_data["USER"]["ffprobeexe"] == "":
            self.ffprobeexe = self.config_data["DEFAULT"]["ffprobeexe"]
        else:
            self.ffprobeexe = self.config_data["USER"]["ffprobeexe"]

    def apply_image_extension_from_config(self):
        if self.config_data["USER"]["image_extension"] == "":
            self.image_extension = self.config_data["DEFAULT"]["image_extension"]
        else:
            self.image_extension = self.config_data["USER"]["image_extension"]

    def apply_video_extension_from_config(self):
        if self.config_data["USER"]["video_extension"] == "":
            self.video_extension = self.config_data["DEFAULT"]["video_extension"]
        else:
            self.video_extension = self.config_data["USER"]["video_extension"]

    def apply_option_from_config(self):
        if self.config_data["USER"]["option"] == "":
            self.option = self.config_data["DEFAULT"]["option"]
        else:
            self.option = self.config_data["USER"]["option"]

    def apply_all_from_config(self):
        self.apply_input_file_from_config()
        self.apply_input_folder_from_config()
        self.apply_output_folder_from_config()
        self.apply_complete_folder_from_config()
        self.apply_ffmpegexe_from_config()
        self.apply_ffprobeexe_from_config()
        self.apply_image_extension_from_config()
        self.apply_video_extension_from_config()
        self.apply_option_from_config()


    def get_framerate(self) -> str:
        self._errorcheck_setffprobeexe()
        self._errorcheck_setinputfile()
        self.__ffprobe = subprocess.run(
            f"{self.ffprobeexe} -i {self.input_file} -v error -select_streams v:0 -show_entries stream=r_frame_rate -print_format csv",
            shell=True,            
            stdout=subprocess.PIPE,
            text=True
            )
        #ffprobeの返り値がframerate,24000/1001\nの形のため、整形処理をしている
        self.child, self.mother = (self.__ffprobe.stdout.split(",")[1]).replace("\n", "").split("/")
        return self.child, self.mother
    
    def get_title(self, extension: bool = True) -> str:
        self._errorcheck_setinputfile()
        self.__title = os.path.basename(self.input_file)
        if not extension:
            self.__title = self.__title.split(".")[0]
        return self.__title

    def video_to_image(self):
        self._errorcheck_all()
        print("Video to Image")
        self.running_vid2img = subprocess.Popen(
            f"{self.ffmpegexe} -i {self.input_file} -an {self.output_folder}\\%10d.{self.image_extension}",
            shell=True,
            stdout=subprocess.PIPE
            )
        while True:
            stdout = self.running_vid2img.poll()
            if stdout != None:
                break
        
        
    def image_to_video(self, target_framerate: str, target_title: str):
        self._errorcheck_all()
        print("Image to Video")
        self.running_img2vid = subprocess.Popen(
            f"{self.ffmpegexe} -i {self.input_file} -r {target_framerate} -i \"{self.input_folder}\\rife%10d.{self.image_extension}\" -map 0:1 -map 1:0 -c:a copy {self.option} -r {target_framerate} \"{self.complete_folder}\\{target_title}.{self.video_extension}\"",
            shell=True,
            stdout=subprocess.PIPE
            )
        while True:
            stdout = self.running_img2vid.poll()
            if stdout != None:
                break
        shutil.rmtree(self.input_folder, True)


    class FFmpegError(Exception):
        pass

    def _errorcheck_setinputfile(self):
        try:
            self.input_file
        except:
            raise self.FFmpegError("\"input_file\" is not set. \"input_file\"が設定されていません")
        
        if os.path.isfile(self.input_file):
            pass
        else:
            raise self.FFmpegError("存在しないファイルが\"input_file\"に指定されています")

    def _errorcheck_setinputfolder(self):
        try:
            self.input_folder
        except:
            raise self.FFmpegError("\"input_folder\" is not set. \"input_folder\"が設定されていません")
        os.makedirs(self.input_folder, exist_ok=True)
        
    def _errorcheck_setoutputfolder(self):
        try:
            self.output_folder
        except:
            raise self.FFmpegError("\"output_folder\" is not set. \"output_folder\"が設定されていません")
        os.makedirs(self.output_folder, exist_ok=True)
        
    def _errorcheck_setcompletefolder(self):
        try:
            self.complete_folder
        except:
            raise self.FFmpegError("\"complete_folder\" is not set. \"complete_folder\"が設定されていません")
     
    def _errorcheck_setffmpegexe(self):
        try:
            self.ffmpegexe
        except:
            raise self.FFmpegError("\"ffmpegexe\" is not set. \"ffmpegexe\"が設定されていません")
        
    def _errorcheck_setffprobeexe(self):
        try:
            self.ffprobeexe
        except:
            raise self.FFmpegError("\"ffprobeexe\" is not set. \"ffprobeexe\"が設定されていません")

    def _errorcheck_setimageextension(self):
        try:
            self.image_extension
        except:
            raise self.FFmpegError("\"image_extension\" is not set. \"image_extension\"が設定されていません")

    def _errorcheck_setvideoextension(self):
        try:
            self.video_extension
        except:
            raise self.FFmpegError("\"video_extension\" is not set. \"video_extension\"が設定されていません")
        
    def _errorcheck_setoption(self):
        try:
            self.option
        except:
            raise self.FFmpegError("\"option\" is not set. \"option\"が設定されていません")
        
    def _errorcheck_all(self):
        self._errorcheck_setinputfile()
        self._errorcheck_setinputfolder()
        self._errorcheck_setoutputfolder()
        self._errorcheck_setcompletefolder()
        self._errorcheck_setffmpegexe()
        self._errorcheck_setffprobeexe()
        self._errorcheck_setimageextension()
        self._errorcheck_setvideoextension()
        self._errorcheck_setoption()