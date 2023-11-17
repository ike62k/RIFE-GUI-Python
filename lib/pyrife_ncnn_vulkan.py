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
    def rifetimes(self) -> str:
        return self.__rifetimes
    @rifetimes.setter
    def rifetimes(self, rifetimes: str):
        self.__rifetimes = rifetimes
    
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

    def apply_times_from_config(self):
        if self.config_data["USER"]["times"] == "":
            self.times = self.config_data["DEFAULT"]["times"]
        else:
            self.times = self.config_data["USER"]["times"]

    #configから各パラメータの全適用
    def apply_all_from_config(self):
        self.apply_input_folder_from_config()
        self.apply_output_folder_from_config()
        self.apply_output_extension_from_config()
        self.apply_rifeexe_from_config()
        self.apply_rifever_from_config()
        self.apply_rifeusage_from_config()
        self.apply_rifegpu_from_config()
        self.apply_times_from_config()


    #rife-ncnn-vulkanを実行
    def __run_old(self):
        self._errorcheck_all()
        subprocess.run(
            f"{self.rifeexe} -i {self.input_folder}/ -o {self.output_folder}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}", 
            shell=True
            )
        if self.times == "4" and False:
            os.rename(self.output_folder, "temp_rife")
            print(self.output_folder) # test
            print(f"{self.rifeexe} -i .\\temp_rife/ -o {self.output_folder}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}")
            print(f"{self.rifeexe} -i {self.input_folder}/ -o {self.output_folder}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}")
            input() #testここまで
            subprocess.run(
                f"{self.rifeexe} -i .\\temp_rife/ -o {self.output_folder}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}", 
                shell=True
                )
        
    def run(self):
        self._errorcheck_all()
        for count in range(1,int(self.times)+1):
            print(f"{2**(int(count)-1)}x→{2**int(count)}x work:{count}")

            if int(self.times) == 1: #総補完回数が1回
                subprocess.run(
                f"{self.rifeexe} -i {self.input_folder}/ -o {self.output_folder}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}", 
                shell=True
                )
                shutil.rmtree(self.input_folder, True)
            elif count == 1: #総補完回数が1回でないときの1回目
                os.makedirs(f".\\temp_rife_{count}")
                subprocess.run(
                f"{self.rifeexe} -i {self.input_folder}/ -o .\\temp_rife_{count}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}", 
                shell=True
                )
                shutil.rmtree(self.input_folder, True)
            elif count < int(self.times): #2回目~(最終でない)
                os.makedirs(f".\\temp_rife_{count}")
                subprocess.run(
                f"{self.rifeexe} -i .\\temp_rife_{int(count)-1}/ -o .\\temp_rife_{count}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}", 
                shell=True
                )
                shutil.rmtree(f".\\temp_rife_{int(count)-1}", True)
            else: #最終
                subprocess.run(
                f"{self.rifeexe} -i .\\temp_rife_{int(count)-1}/ -o {self.output_folder}/ -m rife-{self.rifever}/ -j {self.rifeusage}/ -f rife%010d.{self.output_extension}", 
                shell=True
                )
                shutil.rmtree(f".\\temp_rife_{int(count)-1}", True)

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
        
    def _errorcheck_settimes(self):
        try:
            int(self.times)
        except:
            raise self.RifeError("\"times\" is not set. \"times\"が設定されていません")
        if int(self.times) < 0:
            raise self.RifeError("\"times\" is only natural number. \"times\"は自然数のみです")
    
    #全変数の存在チェック
    def _errorcheck_all(self):
        self._errorcheck_setinputfolder()
        self._errorcheck_setoutputfolder()
        self._errorcheck_setoutputextension()
        self._errorcheck_setrifeexe()
        self._errorcheck_setrifever()
        self._errorcheck_setrifeusage()
        self._errorcheck_setrifegpu()
        self._errorcheck_settimes()