import os
import glob
import shutil
import PySimpleGUI as sg
from lib.pyrife_ncnn_vulkan_GUI import Pyrife_ncnn_vulkan
from lib.pyffmpeg_GUI import Pyffmpeg
from lib.confighandler import ConfigHandler
from lib.VERSION import Version

class Work:
    def __init__(self, path: str):
        self.__config = ConfigHandler(path)
        self.config_data = self.__config.read_all()
        self.rife = Pyrife_ncnn_vulkan(self.config_data["USER"]["pyrife_ncnn_vulkan_config"])
        self.ffmpeg = Pyffmpeg(self.config_data["USER"]["pyffmpeg_config"])
        self.rife.apply_all_from_config()
        self.ffmpeg.apply_all_from_config()

        self.list_rifever = [os.path.basename(i.rstrip("\\")) for i in glob.glob(f"{os.path.dirname(self.rife.rifeexe)}\\*\\")]


class GUI:
    def __init__(self, list_rifever, rifeconfig, ffmpegconfig, version):

        self.column_inputfile = sg.Frame("ファイル選択", expand_x=True, layout=[
            [sg.Text("ファイルを指定してください:"), sg.InputText(expand_x=True, key = "-inputfile-", enable_events=True), sg.FileBrowse(button_text="参照", enable_events=True)],
            [sg.Text("選択されたファイル:"), sg.Text("", key="-nowselectfile-", expand_x=True)]])
        
        self.column_ffmpeg_in = sg.Frame("FFmpegによる前処理の設定", expand_x=True, layout=[
            [sg.Text("画像の拡張子:", (18,1)), sg.Combo(["png", "jpg"],ffmpegconfig["image_extension"], (10,1), key="-imageextension-")]
        ])
        
        self.column_rife = sg.Frame("RIFEの設定", expand_x=True, layout=[
            [sg.Text("RIFEのバージョン:", (18,1)), sg.Combo(list_rifever, rifeconfig["rifever"], (9,1), key="-rifever-"), sg.Text("RIFEの並行処理数:", (18,1)), sg.InputText(rifeconfig["rifeusage"], (10,1), key="-rifeusage-")],
            [sg.Text("RIFEの使用GPUNo.:", (18,1)), sg.InputText(rifeconfig["rifegpu"], (10,1), key="-rifegpu-"), sg.Text("補完処理の回数:", (18,1)), sg.InputText(rifeconfig["times"], (10,1), key="-times-")]
        ])

        self.column_ffmpeg_out = sg.Frame("出力の設定", expand_x=True, layout=[
            [sg.Text("ffmpegの動画出力オプション:"), sg.InputText(ffmpegconfig["option"], expand_x=True, key="-option-")],
            [sg.Text("動画の保存先:"), sg.FolderBrowse(button_text="参照", enable_events=True, target="-completefolder-"), sg.InputText(ffmpegconfig["complete_folder"], expand_x=True, key="-completefolder-"),sg.Text("\\"), sg.InputText("ファイル名", key="-videotitle-", size=(20,1)),sg.Text("."),sg.InputText(ffmpegconfig["video_extension"], (10,1), key="-videoextension-")]
        ])

        self.debugmode = True

        self.console = sg.Output(expand_x=True, expand_y=True, echo_stdout_stderr=self.debugmode)

        self.versiondata = sg.Text(f"Version:{version}", key="-version-", expand_x=True)

        self.debug = sg.Column(layout=[
            [sg.Text("status:", visible=self.debugmode), sg.Input("home", visible=self.debugmode, disabled=True, size=(12,1), key="-debug_status-")]
        ])

        self.column_startstop = sg.Column(justification="RIGHT", layout=[
            [sg.Button("中止", disabled=True, key="-cancel-"), sg.Button("実行", key="-run-")]
        ])
        
        self.layout = [
            [self.column_inputfile],
            [sg.Column([[self.column_ffmpeg_in, self.column_rife]], justification="CENTER")],
            [self.column_ffmpeg_out],
            [self.console],
            [self.versiondata, self.debug, self.column_startstop]
            ]
        self.window = sg.Window("RIFE", self.layout, size=(800,600), resizable=True)


class Control:
    def __init__(self):
        self.version = Version()        
        self.work = Work(".\\setting\\config.ini")
        self.GUI = GUI(self.work.list_rifever, self.work.rife.config_data["USER"], self.work.ffmpeg.config_data["USER"], self.version.version)
        self.status = "home"

    def update_status(self, code: str):
        self.status = code
        self.GUI.window["-debug_status-"].update(self.status)

    def calc_framerate(self) -> str:
        child, mother = self.work.ffmpeg.get_framerate()
        if mother != "1":
            return f"{int(child)*(2**int(self.work.rife.times))}/{mother}"
        else:
            return f"{int(child)*(2**int(self.work.rife.times))}"
    
    def isinputfile(self):
        if self.status != "run_change_setting":
            return None
        if not os.path.isfile(self.values["-inputfile-"]):
            sg.popup_error("入力ファイルが存在しません")
            self.update_status("err_inputfile")
        
    def same_name_as_outputfile(self):
        if self.status != "run_change_setting":
            return None
        if os.path.isfile(f"{self.values["-completefolder-"]}\\{self.values["-videotitle-"]}.{self.values["-videoextension-"]}"):
            ans = sg.popup_ok_cancel("出力ファイルと同じ名前を持つファイルが既に存在します\n上書きしますか？")
            if ans != "OK":
                self.update_status("err_samename")

    def check_rifeusage(self):
        if self.status != "run_change_setting":
            return None
        try:
            q1, q2, q3 = map(int, (self.values["-rifeusage-"]).split(":"))
        except:
            sg.popup_error("rifeusageは\"(int):(int):(int)で\"表記する必要があります")
            self.update_status("err_rifeusage")
            return None
        if q1 < 1 & q2 < 1 & q3 < 1:
            sg.popup_error("rifeusageに使用できる数は自然数のみです")
            self.update_status("err_rifeusage")

    def check_rifegpu(self):
        if self.status != "run_change_setting":
            return None
        try:
            number = list(map(int, (self.values["-rifegpu-"]).split(",")))
        except:
            sg.popup_error("rifegpuに使用できる数は-1以上の整数値のみです\n-1→CPU, 0,1,2...→GPU\nスペース抜きカンマ区切りでマルチGPU")
            self.update_status("err_rifegpu")
            return None
        if len(number) != len(set(number)):
            sg.popup_error("同じIDを2回以上指定することはできません")
            self.update_status("err_rifegpu")
            return None
        for i in number:
            if i < -1:
                sg.popup_error("rifegpuに使用できる数は-1以上の整数値のみです\n-1→CPU, 0,1,2...→GPU\nスペース抜きカンマ区切りでマルチGPU")
                self.update_status("err_rifegpu")
                return None
            
    def check_times(self):
        if self.status != "run_change_setting":
            return None
        try:
            number = int(self.values["-times-"])
        except:
            sg.popup_error("timesに使用できる数は自然数のみです")
            self.update_status("err_times")
            return None
        if number < 1:
            sg.popup_error("timesに使用できる数は自然数のみです")
            self.update_status("err_times")
            return None

    def run(self):
        while True:
            self.event, self.values = self.GUI.window.read()

            if self.event == "-inputfile-":
                self.update_status("inputfile")
                self.GUI.window["-nowselectfile-"].update(self.values["-inputfile-"])
                self.update_status("home")

            if self.event == "-run-":
                #GUI上の変更
                self.update_status("run_change_setting")
                self.GUI.window["-run-"].update(disabled=True)
                self.GUI.window["-cancel-"].update(disabled=False)
                #パラメータの妥当性をチェック
                #inputfile
                self.isinputfile()
                #outputfile
                self.same_name_as_outputfile()
                #rifeusage
                self.check_rifeusage()
                #rifegpu
                self.check_rifegpu()
                #times
                self.check_times()
                #各パラメータを変数に代入
                self.work.ffmpeg.input_file = self.values["-inputfile-"]
                self.work.ffmpeg.image_extension = self.values["-imageextension-"]
                self.work.rife.output_extension = self.values["-imageextension-"]
                self.work.rife.rifever = self.values["-rifever-"]
                self.work.rife.rifeusage = self.values["-rifeusage-"]
                self.work.rife.rifegpu = self.values["-rifegpu-"]
                self.work.rife.times = self.values["-times-"]
                self.work.ffmpeg.video_extension = self.values["-videoextension-"]
                self.work.ffmpeg.option = self.values["-option-"]
                #一時フォルダの初期化
                for i in [self.work.ffmpeg.input_folder, self.work.ffmpeg.output_folder]:
                    shutil.rmtree(i, ignore_errors=True)
                    os.makedirs(i, exist_ok=True)
                #処理部分の定義
                def process():
                    if self.status == "run_change_setting":
                        self.update_status("run_vid2img")
                        self.work.ffmpeg.video_to_image()
                    if self.status == "run_vid2img":
                        self.update_status("run_rife")
                        self.work.rife.run()
                    if self.status == "run_rife":
                        self.update_status("run_img2vid")
                        self.work.ffmpeg.image_to_video(self.calc_framerate(), self.values["-videotitle-"])
                #処理部分をプロセス化して実行
                self.GUI.window.start_thread(lambda: process(), end_key="-finish-")

            if self.event == "-finish-":
                self.GUI.window["-run-"].update(disabled=False)
                self.GUI.window["-cancel-"].update(disabled=True)
                print("処理が完了しました")
                self.update_status("home")

            if self.event == "-cancel-":
                if self.status == "run_vid2img":
                    self.update_status("cancel_vid2img")
                    self.work.ffmpeg.running_vid2img.kill()
                if self.status == "run_rife":
                    for _ in range(int(self.work.rife.times)):
                        self.update_status("cancel_rife")
                        self.work.rife.running_rife.kill()
                if self.status == "run_img2vid":
                    self.update_status("cancel_img2vid")
                    self.work.ffmpeg.running_img2vid.kill()
                print("作業を中断しました")
                self.update_status("home")     

            if self.event == sg.WIN_CLOSED:
                break

        self.GUI.window.close()


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    App = Control()
    App.run()