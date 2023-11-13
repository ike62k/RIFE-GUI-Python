"""
バージョンに関するファイルです。書き換えないでください。
ファイル更新日:20231113
"""
class Version:
    def __init__(self):
        self.__version = 2.0
        self.__date_App = 20231113
        self.__date_confighandler = 20231113
        self.__date_pyffmpeg = 20231113
        self.__date_pyrife_ncnn_vulkan = 20231113

    @property
    def version(self):
        return self.__version
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
    