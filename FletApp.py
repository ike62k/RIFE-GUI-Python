import os
import shutil
from tkinter import filedialog
import flet as ft
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.pyffmpeg import Pyffmpeg
from lib.confighandler import ConfigHandler
from lib.VERSION import Version

class Work():
    def __init__(self, path: str):
        self.__config = ConfigHandler(path)
        self.config_data = self.__config.read_all()
        self.rife = Pyrife_ncnn_vulkan(self.config_data["USER"]["pyrife_ncnn_vulkan_config"])
        self.ffmpeg = Pyffmpeg(self.config_data["USER"]["pyffmpeg_config"])
        self.rife.apply_all_from_config()
        self.ffmpeg.apply_all_from_config()

class GUI():
    def __init__(self):
        pass

    def main(self, page: ft.Page):
        page.title = "test"

        def pick_files_result(e: ft.FilePickerResultEvent):
            self.selected_files.value = e.files[0].path if e.files else "キャンセルされました"
            self.selected_files.update()  
        self.pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        self.selected_files = ft.Text()      
        page.overlay.append(self.pick_files_dialog)

        self.file_button = ft.ElevatedButton(
                                            "ファイルを選択",
                                            icon=ft.icons.UPLOAD_FILE,
                                            on_click=self.pick_files_dialog.pick_files,
                                             )

        page.add(
            ft.Row(
                [
                    self.file_button,
                    self.selected_files,
                ],
            

            )
        )
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.update()

    def run(self):
        ft.app(target=self.main)

class Contololler():
    def __init__(self):
        self.work = Work(".\\setting\\config.ini")
        self.GUI = GUI()

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    App = Contololler()
    App.GUI.run()