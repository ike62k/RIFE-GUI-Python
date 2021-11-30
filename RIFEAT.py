#RIFE AutomationTool Python Ver1.0.1 2021/11/30

def mainfunc (douga,gui_hantei,rifemode,bairitsu,bitto,gazou,hinsitsu,sureddo,kodekku):

    import os
    import subprocess as sp
    import math
    import glob
    import csv
    import configparser


    P_filepath = os.path.dirname(__file__)
    os.chdir(P_filepath)


    config_ini = configparser.ConfigParser()
    config_ini.read("RATconfig.ini", encoding="utf-8")

    read_default = config_ini["DEFAULT"]


    #以下、初期設定
    P_codec = str(read_default.get("CODEC")) #動画エンコードに使うコーデック、使用環境に応じて決定
    P_picture = str(read_default.get("PICTURE")) #処理中に使う画像の拡張子
    P_jpgquality= str(read_default.get("JPGQUALITY")) #jpg処理時に使用する画像品質の設定
    P_bitrate= str(read_default.get("BITRATE")) #動画エンコード後のビットレート
    P_rifemode= str(read_default.get("RIFEVER")) #RIFEの処理モード
    P_rifeusage= str(read_default.get("RIFEUSAGE")) #RIFEの補完時の並列処理数
    P_interpolation= str(read_default.get("INTERPOLATION")) #補完の倍率(初期値)

    P_end_menu = bool(int(read_default.get("END_M"))) #終了時に終了したことを伝えるか、str型ではなくbool型で
    P_delete_menu = bool(int(read_default.get("DELETE_M"))) #データを削除するかしないかのチェックをするか、str型ではなくbool型で
    P_defaultdelete = bool(int(read_default.get("DELETE"))) #チェックをスルーした際自動で削除するか、str型ではなくbool型で
    P_interpolation_menu = bool(int(read_default.get("INTERPOLATION_M"))) #倍率を確認するか、str型ではなくbool型で
    P_guimode = gui_hantei #GUIで起動しているかCUIで起動しているか


    #P_framerate #元の動画のフレームレート
    #P_Aframerate #元の動画のフレームレート*補完の倍率
    # P_base 取り込む元のファイル(相対パス)
    #P_base_filename 元のファイルの名前
    # P_base_less 取り込む元のファイルの拡張子を抜いたもの
    # P_menu YesかNoか記憶
    # P_interpolation_int 補完倍率のint型
    # directory_number_flt 補完番号とディレクトリの番号を一致させる途中経過
    # directory_number ディレクトリの番号
    # P_check 画像ファイルに他のファイルが残っているか
    # P_check_inside 音声ストリームが動画に含まれており、それが音声ファイル化されたか
    # P_check_wav 動画ファイルとは別にwav形式の音声ファイルが追加されたか
    # P_check_m4a 動画ファイルとは別にm4a形式の音声ファイルが追加されたか
    # delete_list 作業ファイル削除時に作成されたデータの一覧を取得


    #===以下 csvmaker内 ===
    #framerate_csv,framerate_csv_d,framerate_base_framerate.cutはすべてフレームレート関係(CSV->str)
    #======


    #directory内は[元動画の画像変換後フォルダ,2倍補完後の画像フォルダ,4倍補完後の画像フォルダ,音声フォルダ,一時フォルダ]、デフォルトではメインファイル直下
    directory = ["video_data","video_data_2x","video_data_4x","audio_data","temp"]

    if P_guimode == True:
        P_bitrate = bitto

        if rifemode == "無印":
            P_rifemode =""
        else:
            P_rifemode ="-" + rifemode

        P_base = douga

        P_interpolation = bairitsu

        P_picture = gazou

        P_jpgquality = hinsitsu

        P_rifeusage = sureddo

        P_codec = kodekku


    def  interpolationchecker(b):
        if b =="2" or b =="4":
            return True
        else:
            return False

    def csvmaker(c,d,e):
        sp.run(f"ffprobe -v error -i {c} -select_streams v:0 -show_entries stream=r_frame_rate -of csv > {e}\{d}_framerate_data.csv", shell=True)
        framerate_csv = open(f".\{e}\{d}_framerate_data.csv")
        framerate_csv_d = csv.reader(framerate_csv, delimiter=",")
        framerate_base = next(framerate_csv_d)
        framerate_cut = (framerate_base[1]).split("/")[0]
        return(framerate_cut)

    if P_picture =="png" :
        P_jpgquality = ""

    if P_guimode == False:
        if not P_rifemode == "":
            P_rifemode = "-" + P_rifemode

    P_check = glob.glob(f".\{directory[0]}\\*")
    if not P_check == []:
        print("前回の作業時のファイルが残っています")
        print("ファイルを削除してからEnterキーを押して続行してください")
        input()


    for i in range(len(directory)):
        os.makedirs(directory[i], exist_ok=True)

    if P_guimode == False:
        P_base = input("変換するファイルの名前を入力してください(このファイルの場所からの相対パス) >")


    if P_interpolation_menu == True and P_guimode == False:
        while True:
            P_interpolation = input("補完の倍率を入力してください (2/4) >")
            if interpolationchecker(P_interpolation) == False:
                print("倍率は2倍もしくは4倍で指定してください")
                continue
            P_menu = input(f"{P_interpolation}でよろしいですか? (y/n) >")
            if P_menu == "y" or P_menu == "Y" :
                break
            print("2もしくは4を入力してください")



    try:
        P_base_filename = P_base.split("\\")[-1]
    except:
        P_base_filename = P_base
    P_base_less = P_base_filename.split(".")[-2]
    P_interpolation_int = int(P_interpolation)
    directory_number_flt = math.log2(P_interpolation_int)
    directory_number = int(directory_number_flt)
    P_framerate = csvmaker(P_base,P_base_less,directory[4])
    P_Aframerate = float(P_framerate)*2

    sp.run(f"ffmpeg -y -i {P_base} {P_jpgquality} .\{directory[0]}\{P_base_less}_v%010d.{P_picture}" ,shell=True)
    sp.run(f"ffmpeg -y -i {P_base} -vn -acodec copy .\{directory[3]}\{P_base_less}_a_inside.wav" ,shell=True)


    P_check_inside = glob.glob(f".\{directory[3]}\\{P_base_less}_a_inside.wav")
    P_check_wav = glob.glob(f".\{directory[3]}\\{P_base_less}_a.wav")
    P_check_m4a = glob.glob(f".\{directory[3]}\\{P_base_less}_a.m4a")


    sp.run(f"rife-ncnn-vulkan -i {directory[0]}/ -o {directory[1]}/ {P_rifeusage}/ -m rife{P_rifemode}/ -f {P_base_less}_v2x%010d.{P_picture}")
    if P_interpolation == "4":
        sp.run(f"rife-ncnn-vulkan -i {directory[1]}/ -o {directory[2]}/ {P_rifeusage}/ -m rife{P_rifemode}/ -f {P_base_less}_v4x%010d.{P_picture}")
        P_Aframerate = float(P_framerate)*4


    if P_check_inside == [] and P_check_wav == [] and P_check_m4a == []:
        sp.run(f"ffmpeg -y -framerate {P_Aframerate} -i .\{directory[directory_number]}\{P_base_less}_v{P_interpolation}x%010d.{P_picture} -vcodec {P_codec} -b:v {P_bitrate} -tune zerolatency -pix_fmt yuv420p -r {P_Aframerate} {P_base_less}_{P_interpolation}x.mov")
    elif not P_check_inside == []:
        sp.run(f"ffmpeg -y -framerate {P_Aframerate} -i .\{directory[directory_number]}\{P_base_less}_v{P_interpolation}x%010d.{P_picture} -i .\{directory[3]}\{P_base_less}_a_inside.wav -c:v {P_codec} -c:a copy -b:v {P_bitrate} -pix_fmt yuv420p -r {P_Aframerate} {P_base_less}_{P_interpolation}x.mov")
    elif not P_check_wav == []:
        sp.run(f"ffmpeg -y -framerate {P_Aframerate} -i .\{directory[directory_number]}\{P_base_less}_v{P_interpolation}x%010d.{P_picture} -i .\{directory[3]}\{P_base_less}_a.wav -c:v {P_codec} -c:a copy -b:v {P_bitrate} -pix_fmt yuv420p -r {P_Aframerate} {P_base_less}_{P_interpolation}x.mov")
    else:
        sp.run(f"ffmpeg -y -framerate {P_Aframerate} -i .\{directory[directory_number]}\{P_base_less}_v{P_interpolation}x%010d.{P_picture} -i .\{directory[3]}\{P_base_less}_a.m4a -c:v {P_codec} -c:a copy -b:v {P_bitrate} -pix_fmt yuv420p -r {P_Aframerate} {P_base_less}_{P_interpolation}x.mov")


    P_menu=''

    if P_guimode == False and P_delete_menu == True:
        print("作業時に生成したファイルを削除しますか?\n手動で音声ファイルを挿入した場合はそのファイルは削除されません")
        P_menu=input("y/n >")
    elif P_guimode == True:
        P_menu = "y"
    elif P_guimode == False and P_defaultdelete == True:
        P_menu = "y"


    if P_menu == "y" or P_menu == "Y":
        delete_list = glob.glob(f".\{directory[0]}\\{P_base_less}_v*")
        count = len(delete_list)
        for i in range(count):
            os.remove(delete_list[i])

        delete_list = glob.glob(f".\{directory[1]}\\{P_base_less}_v2x*")
        count = (len(delete_list))
        for i in range(count):
            os.remove(delete_list[i])

        os.remove(f".\{directory[4]}\\{P_base_less}_framerate_data.csv")

        if P_interpolation == "4":
            delete_list = glob.glob(f".\{directory[2]}\\{P_base_less}_v4x*")
            count = (len(delete_list))
            for i in range(count):
                os.remove(delete_list[i])

        if not P_check_inside == []:
            delete_list = glob.glob(f".\{directory[3]}\\{P_base_less}_a_inside.wav")
            count = (len(delete_list))
            for i in range(count):
                os.remove(delete_list[i])


    if P_end_menu == True:
        print("プログラムは正常に完了しました\nなにかキーを押して終了します")
        input()
    
    if P_guimode == True:
        return "Success"


if __name__ == "__main__":
    mainfunc("",False,"","","","","","")