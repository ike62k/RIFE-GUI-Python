import subprocess
import glob
from lib.confighandler import ConfigHandler

class Pyrife_ncnn_vulkan():
    #コンフィグのロード
    def __init__(self, config_path: str) -> None:
        self.__config_path: str = config_path
        self.config = ConfigHandler(self.__config_path)
        self.__config_data: dict = self.config.read_all()

    #コンフィグの変更と確認(ファイルパス/中身)
    @property
    def config_path(self) -> str:
        return self.__config_path
    @config_path.setter
    def config_path(self, config_path: str):
        self.__config_path: str = config_path
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
    @property
    def input_file_number(self) -> int:
        return len(glob.glob(self.__input_file))
    
    #inputフォルダの変更と確認
    @property
    def input_folder(self) -> str:
        return self.__input_folder
    @input_folder.setter
    def input_folder(self, input_folder: str):
        self.__input_folder = input_folder
    @property
    def input_folder_nunber(self) -> int:
        return len(glob.glob(f"{self.input_folder}\\*"))

    #outputフォルダの変更と確認
    @property
    def output_folder(self) -> str:
        return self.__output_folder
    @output_folder.setter
    def output_folder(self, output_folder: str):
        self.__output_folder = output_folder
    
    def run_file(self):
        subprocess.run(
            f"{self.config_data['DEFAULT']['RIFEEXE']} -i {self.input_file}/ -o {self.output_folder}", 
            shell=True
            )
    
    def run_folder(self):
        subprocess.run(
            f"{self.config_data['DEFAULT']['RIFEEXE']} -i {self.input_folder}/ -o {self.output_folder}", 
            shell=True
            )



