import os
import shutil
from tkinter import filedialog
import streamlit as st
from lib.pyrife_ncnn_vulkan import Pyrife_ncnn_vulkan
from lib.pyffmpeg import Pyffmpeg
from lib.confighandler import ConfigHandler
from lib.VERSION import Version

class Work():
    def __init__(self):
        self.config = ConfigHandler(".\\setting\\config.ini")
        self.config_data = self.config.read_all()
        self.rife = Pyrife_ncnn_vulkan(self.config_data["USER"]["pyrife_ncnn_vulkan_config"])
        self.ffmpeg = Pyffmpeg(self.config_data["USER"]["pyffmpeg_config"])
        self.rife.apply_all_from_config()
        self.ffmpeg.apply_all_from_config()

    

class GUI():
    def __init__(self):
        pass
    def main(self):
        st.title("RIFE_ncnn_Vulkan_Python")
        self.filebutton = st.button("ファイルを選んでください")
        self.nowselectfile = ""
        self.filedisp = st.write(st.session_state["file"])

        st.write("RIFEの設定")
        self.rifeleft,self.riferight = st.columns(2)

        if self.filebutton:
            self.nowselectfile = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
            st.session_state["file"] = self.nowselectfile



class contololler:
    def __init__(self):
        self.work = Work()
        self.GUI = GUI()
        self.GUI.main()

    #    if self.GUI.filebutton:
    #        self.file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__))
    #        self.GUI.nowselectfile = self.file if self.file != "" else "ファイルが選択されませんでした"
    #        self.GUI.filedisp = st.write(self.GUI.nowselectfile)

if __name__ == "__main__":
    process = contololler()