import subprocess
import glob
import os
import shutil
from lib.confighandler import ConfigHandler

class Pyrife_ncnn_vulkan():
    #コンフィグの初回ロードと適用
    def __init__(self, config_path: str) -> None:
        self.__config_path: str = config_path
        self.config = ConfigHandler(self.__config_path)
        self.__config_data: dict = self.config.read_all()

    
    #↓各パラメーターをコード上から操作する(ゲッターセッター)↓
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

    #出力ファイルの拡張子の変更と確認
    @property
    def output_extension(self) -> str:
        return self.__output_extension
    @output_extension.setter
    def output_extension(self, output_extension: str):
        self.__output_extension = output_extension
    
    #rife.exeの変更と確認
    @property
    def rifeexe(self) -> str:
        return self.__rifeexe
    @rifeexe.setter
    def rifeexe(self, rifeexe: str):
        self.__rifeexe = rifeexe

    #rifeのモデルVerの変更と確認
    @property
    def rifever(self) -> str:
        return self.__rifever
    @rifever.setter
    def rifever(self, rifever: str):
        self.__rifever = rifever

    #rifeの並列処理数の変更と確認
    @property
    def rifeusage(self) -> str:
        return self.__rifeusage
    @rifeusage.setter
    def rifeusage(self, rifeusage: str):
        self.__rifeusage = rifeusage

    #rifeの使用するGPUの変更と確認
    @property
    def rifegpu(self) -> str:
        return self.__rifegpu
    @rifegpu.setter
    def rifegpu(self, rifegpu: str):
        self.__rifegpu = rifegpu

    #補完倍率の変更と確認
    @property
    def riferatio(self) -> str:
        return self.__riferatio
    @riferatio.setter
    def riferatio(self, riferatio: str):
        self.__riferatio = riferatio
    
    #↓各パラメーターをconfigファイルから操作する↓
    #configファイルからの適応
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

    def apply_output_extension_from_config(self):
        if self.config_data["USER"]["output_extension"] == "":
            self.output_extension = self.config_data["DEFAULT"]["output_extension"]
        else:
            self.output_extension = self.config_data["USER"]["output_extension"]

    def apply_rifeexe_from_config(self):
        if self.config_data["USER"]["rifeexe"] == "":
            self.rifeexe = self.config_data["DEFAULT"]["rifeexe"]
        else:
            self.rifeexe = self.config_data["USER"]["rifeexe"]

    def apply_rifever_from_config(self):
        if self.config_data["USER"]["rifever"] == "":
            self.rifever = self.config_data["DEFAULT"]["rifever"]
        else:
            self.rifever = self.config_data["USER"]["rifever"]

    def apply_rifeusage_from_config(self):
        if self.config_data["USER"]["rifeusage"] == "":
            self.rifeusage = self.config_data["DEFAULT"]["rifeusage"]
        else:
            self.rifeusage = self.config_data["USER"]["rifeusage"]

    def apply_rifegpu_from_config(self):
        if self.config_data["USER"]["rifegpu"] == "":
            self.rifegpu = self.config_data["DEFAULT"]["rifegpu"]
        else:
            self.rifegpu = self.config_data["USER"]["rifegpu"]

    def apply_ratio_from_config(self):
        if self.config_data["USER"]["ratio"] == "":
            self.ratio = self.config_data["DEFAULT"]["ratio"]
        else:
            self.ratio = self.config_data["USER"]["ratio"]

    #configから各パラメータの全適用
    def apply_all_from_config(self):
        self.apply_input_folder_from_config()
        self.apply_output_folder_from_config()
        self.apply_output_extension_from_config()
        self.apply_rifeexe_from_config()
        self.apply_rifever_from_config()
        self.apply_rifeusage_from_config()
        self.apply_rifegpu_from_config()
        self.apply_ratio_from_config()


    #rife-ncnn-vulkanを実行
    def run(self):
        self._errorcheck_all()
        subprocess.run(
            f"{self.rifeexe} -i {self.input_folder}/ -o {self.output_folder}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}", 
            shell=True
            )
        if self.ratio == "4":
            self._chenge_inout()
            self._delete_output_folder_contents()
            subprocess.run(
                f"{self.rifeexe} -i {self.input_folder}/ -o {self.output_folder}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}", 
                shell=True
                )
        
    def _chenge_inout(self):
        os.rename(self.input_folder, f"{self.input_folder}_temp")
        os.rename(self.output_folder, self.input_folder)
        os.rename(f"{self.input_folder}_temp", self.output_folder)

    def  _delete_input_folder_contents(self):
        shutil.rmtree(self.input_folder)
        os.makedirs(self.input_folder)

    def _delete_output_folder_contents(self):
        shutil.rmtree(self.output_folder)
        os.makedirs(self.output_folder)

    #↓変数の存在チェックとそれに伴うエラー↓
    #エラー用クラス
    class RifeError(Exception):
        pass

    def _errorcheck_setinputfolder(self):
        try:
            self.input_folder
        except:
            raise self.RifeError("\"input_folder\" is not set. \"input_folder\"が設定されていません")
        
    def _errorcheck_setoutputfolder(self):
        try:
            self.output_folder
        except:
            raise self.RifeError("\"output_folder\" is not set. \"output_folder\"が設定されていません")

    def _errorcheck_setoutputextension(self):
        try:
            self.output_extension
        except:
            raise self.RifeError("\"output_extension\" is not set. \"output_extension\"が設定されていません")

    def _errorcheck_setrifeexe(self):
        try:
            self.rifeexe
        except:
            raise self.RifeError("\"rifeexe\" is not set. \"rifeexe\"が設定されていません")
        
    def _errorcheck_setrifever(self):
        try:
            self.rifever
        except:
            raise self.RifeError("\"rifever\" is not set. \"rifever\"が設定されていません")
        
    def _errorcheck_setrifeusage(self):
        try:
            self.rifeusage
        except:
            raise self.RifeError("\"rifeusage\" is not set. \"rifeusage\"が設定されていません")
        
    def _errorcheck_setrifegpu(self):
        try:
            self.rifegpu
        except:
            raise self.RifeError("\"rifeexe\" is not set. \"rifeexe\"が設定されていません")
        
    def _errorcheck_setratio(self):
        try:
            self.ratio
        except:
            raise self.RifeError("\"ratio\" is not set. \"ratio\"が設定されていません")
    
    #全変数の存在チェック
    def _errorcheck_all(self):
        self._errorcheck_setinputfolder()
        self._errorcheck_setoutputfolder()
        self._errorcheck_setoutputextension()
        self._errorcheck_setrifeexe()
        self._errorcheck_setrifever()
        self._errorcheck_setrifeusage()
        self._errorcheck_setrifegpu()
        self._errorcheck_setratio()