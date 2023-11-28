"""
バージョンに関するファイルです。書き換えないでください。
ファイル更新日:20231128
"""
class Version:
    def __init__(self):
        self.__version = "2.2-GUI"
        self.__subver = "00001"
        self.__date_App = 20231128
        self.__date_confighandler = 20231118
        self.__date_pyffmpeg = 20231128
        self.__date_pyrife_ncnn_vulkan = 20231128

    @property
    def version(self):
        return self.__version
    @property
    def subver(self):
        return self.__subver
    @property
    def date_App(self):
        return self.__date_App
    @property
    def date_confighandler(self):
        return self.__date_confighandler
    @property
    def date_pyffmpeg(self):
        return self.__date_pyffmpeg
    @property
    def date_pyrife_ncnn_vulkan(self):
        return self.__date_pyrife_ncnn_vulkan
    