import os
import shutil
from tkinter import filedialog
import PySimpleGUI as sg
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.pyffmpeg import Pyffmpeg
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

class GUI:
    def __init__(self):

        self.column_inputfile = sg.Frame("ファイル選択", expand_x=True, layout=[
            [sg.Text("ファイルを指定してください:"), sg.InputText(expand_x=True, key = "-inputfile-", enable_events=True), sg.FileBrowse(button_text="参照", enable_events=True)],
            [sg.Text("選択されたファイル:"), sg.Text("", key="-nowselectfile-", expand_x=True)]])
        
        self.column_ffmpeg_in = sg.Frame("FFmpegによる前処理の設定", expand_y=True, layout=[

        ])
        
        self.column_rife = sg.Frame("RIFEの設定", expand_y=True, layout=[

        ])

        self.column_ffmpeg_out = sg.Frame("FFmpegによる後処理の設定", expand_y=True, layout=[
            
        ])
        
        self.layout = [
            [self.column_inputfile],
            [self.column_ffmpeg_in, self.column_rife, self.column_ffmpeg_out]
            ]
        self.window = sg.Window("RIFE", self.layout, size=(700,400), resizable=True)

class Control:
    def __init__(self):
        self.work = Work(".\\setting\\config.ini")
        self.GUI = GUI()

    def run(self):
        while True:
            event, values = self.GUI.window.read()

            if event == "-inputfile-":
                self.GUI.window["-nowselectfile-"].update(values["-inputfile-"])


            if event == sg.WIN_CLOSED:
                break

        self.GUI.window.close()

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    App = Control()
    App.run()