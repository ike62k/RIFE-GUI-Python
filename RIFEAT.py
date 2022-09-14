#RIFE AutomationTool Python Ver1.2 2022/9/14

def mainfunc (video,gui_mode,GUIsetting):
    import os
    import subprocess as sp
    import configparser
    import shutil

    os.chdir(os.path.dirname(__file__))

    class configreader:
        def __init__(self,configdata):
            self.codec = str(configdata.get("CODEC"))
            self.bitrate = str(configdata.get("BITRATE"))
            self.rifever = str(configdata.get("RIFEVER"))
            self.rifeusage = str(configdata.get("RIFEUSAGE"))
            self.interpolation = str(configdata.get("INTERPOLATION"))
            self.picture = str(configdata.get("PICTURE"))
            if self.picture == "png":
                self.jpgquality = ""
            else:
                self.jpgquality = str(configdata.get("JPGQUALITY"))
            self.interpolation_menu = bool(int(configdata.get("INTERPOLATION_M")))
            self.defaultdelete = bool(int(configdata.get("DELETE")))
            self.delete_menu = bool(int(configdata.get("DELETE_M")))
            self.end_menu = bool(int(configdata.get("END_M")))

    class configgui:
        def __init__(self,GUIsetting):
            self.codec = GUIsetting[0]
            self.bitrate = GUIsetting[1]
            self.rifever = GUIsetting[2]
            self.rifeusage = GUIsetting[3]
            self.interpolation = GUIsetting[4]
            self.picture = GUIsetting[5]
            if self.picture == "png":
                self.jpgquality = ""
            else:
                self.jpgquality = GUIsetting[6]
            self.interpolation_menu = False
            self.defaultdelete = True
            self.delete_menu = False
            self.end_menu = False

    if gui_mode == True:
        setting = configgui(GUIsetting)
    else:
        configdata = configparser.ConfigParser()
        configdata.read("RATconfig.ini", encoding="utf-8")
        configdata = configdata["DEFAULT"]
        setting = configreader(configdata)

    directory = ["video_data","video_data_2x","video_data_4x","audio_data","temp"]
    for name in directory:
        if setting.defaultdelete == True:
            shutil.rmtree(name, ignore_errors=True)
        os.makedirs(name, exist_ok=True)

    if gui_mode == False:
        while True:
            video = input("変換するファイルの名前を入力してください(絶対パス) >")
            if os.path.isfile(video) == True:
                break
            else:
                print("ファイルが存在しません")
                continue
        if setting.interpolation_menu == True:
            while True:
                setting.interpolation = input("補完の倍率を入力してください (2/4) >")
                if setting.interpolation != "2" and setting.interpolation != "4":
                    print("2もしくは4で指定してください")
                    continue
                else:
                    setting.interpolation = int(setting.interpolation)
                    break

    sp.run(f"ffprobe -i \"{video}\" -select_streams v:0 -show_entries stream=r_frame_rate -of csv > \"{os.path.dirname(__file__)}\\{directory[4]}\\framerate_data.txt\"", shell=True)
    framerate = open(f"{os.path.dirname(__file__)}\\{directory[4]}\\framerate_data.txt")
    framerate = (framerate.read()).split(",")[1]
    framerate_child = framerate.split("/")[0]
    framerate_parent = framerate.split("/")[1]
    framerate = int(framerate_child) / int(framerate_parent)
    Aframerate = float(framerate)*int(setting.interpolation)

    videodir = os.path.dirname(video)
    title = os.path.basename(video)
    title_no_extension = title.rsplit(".", 1)[0]
    extension = title.rsplit(".", 1)[-1]

    sp.run(f"ffmpeg -i \"{video}\" -an {setting.jpgquality} .\\{directory[0]}\\{title_no_extension}_v%010d.{setting.picture}", shell=True)

    sp.run(f"rife-ncnn-vulkan -i {directory[0]}/ -o .\\{directory[1]}/ {setting.rifeusage}/ -m rife{setting.rifever}/ -f {title_no_extension}_2x_%010d.{setting.picture}", shell=True)
    if setting.interpolation == 4:
        sp.run(f"rife-ncnn-vulkan -i {directory[1]}/ -o .\\{directory[2]}/ {setting.rifeusage}/ -m rife{setting.rifever}/ -f {title_no_extension}_4x_%010d.{setting.picture}", shell=True)

    sp.run(f"ffmpeg -i \"{video}\" -r {Aframerate} -i .\\{directory[int(int(setting.interpolation)/2)]}\\{title_no_extension}_{setting.interpolation}x_%010d.{setting.picture} -map 0:1 -map 1:0 -c:a copy -c:v {setting.codec} -b:v {setting.bitrate} -r {Aframerate} \"{videodir}\\{title_no_extension}_{setting.interpolation}x.{extension}\"", shell=True)

    if setting.defaultdelete ==True:
        for name in directory:
            shutil.rmtree(name)

if __name__ == "__main__":
    mainfunc("",False,[])