import os
import shutil
from tkinter import filedialog
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.pyffmpeg import Pyffmpeg
from lib.confighandler import ConfigHandler
from lib.VERSION import Version

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
        self.__version = Version()

    def create_instance_rife(self):
        self.rife = Pyrife_ncnn_vulkan(self.__pyrife_ncnn_vulkan_config)
        self.rife.apply_all_from_config()
    
    def create_instance_ffmpeg(self):
        self.ffmpeg = Pyffmpeg(self.__pyffmpeg_config)
        self.ffmpeg.apply_all_from_config()

    def run_all_process(self):
        self.ffmpeg.video_to_image()
        self.rife.run()
        self.ffmpeg.image_to_video(str(int(self.ffmpeg.get_framerate())*int(self.rife.ratio)), self.ffmpeg.get_title(False))

    def crean_ffmpeg_folder(self):
        if os.path.exists(self.ffmpeg.input_folder):
            shutil.rmtree(self.ffmpeg.input_folder)
        if os.path.exists(self.ffmpeg.output_folder):
            shutil.rmtree(self.ffmpeg.output_folder)

    def connection_check(self) -> str:
        if self.ffmpeg.output_folder != self.rife.input_folder or self.ffmpeg.input_folder != self.rife.output_folder:
            return (
                "FFmpegとRIFE間でのフォルダの整合性が取れていません\n",
                "FFmpegの\"output_folder\"とRIFEの\"input_folder\"は同一である必要があります\n"
                "FFmpegの\"input_folder\"とRIFEの\"output_folder\"は同一である必要があります\n"
                )
        else:
            return "整合性に関する問題はありませんでした"
        
    def software_check(self):
        list = []
        if not os.path.isfile(self.rife.rifeexe):
            list.append("RIFE-ncnn-Vulkan.exeが見つかりませんでした")
        if not os.path.isfile(self.ffmpeg.ffmpegexe):
            list.append("FFmpeg.exeが見つかりませんでした")
        if not os.path.isfile(self.ffmpeg.ffprobeexe):
            list.append("FFprobe.exeが見つかりませんでした")
        return list if list != [] else "ソフトウェアが確認できました"

    def show_now_setting(self):
        print("\n========現在の設定========\n")
        print(
            f"選択中の動画{self.ffmpeg.input_file}\n",
            "\n-補完処理前の設定-\n",
            f"補完元フレームの保存場所:{self.ffmpeg.output_folder}\n",
            f"補完元フレームの拡張子:{self.ffmpeg.image_extension}\n",
            "\n-補完処理の設定-\n",
            f"使用するRIFEのモデル:{self.rife.rifever}\n",
            f"使用するGPU No.:{self.rife.rifegpu}\n",
            f"RIFEの並行処理数:{self.rife.rifeusage}\n",
            f"補完後フレームの保存場所:{self.rife.output_folder}\n",
            f"補完後フレームの拡張子:{self.rife.output_extension}\n",
            "\n-補完後の設定-\n",
            f"FFmpegエンコード時のオプション:{self.ffmpeg.option}\n",
            f"完成動画の保存場所:{self.ffmpeg.complete_folder}\n",
            f"完成動画の拡張子:{self.ffmpeg.video_extension}"
        )
        print("================================")

    def version(self):
        print("\n================\n")
        print("RIFE AUTOMATION TOOL PYTHON")
        print("copyright 2023 Veludo")
        print(f"Version : {self.__version.version}")
        print(self.__version.date_App)
        print("\n================\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    runner = main(".\\setting\config.ini")
    runner.create_instance_ffmpeg()
    runner.create_instance_rife()
    runner.version()
    while True:
        print("補完する動画を選んでください")
        runner.ffmpeg.input_file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
        if not runner.ffmpeg.input_file == "":
            break
        print("選択されませんでした")
    print(runner.software_check())
    print(runner.connection_check())
    runner.show_now_setting()
    print("以上の条件で処理を開始しますか？(y/n)")
    if not input() in ["y", "Y"]:
        exit()
    runner.run_all_process()
    runner.crean_ffmpeg_folder()
    print("処理が正しく完了しました\nEnterキーを押すと終了します")
    input()