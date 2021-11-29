# RIFEAutomationToolPython
フレーム補間を行うオープンソースソフト、[RIFE-ncnn-Vulkan](https://github.com/nihui/rife-ncnn-vulkan)の使用を「少しだけ」簡略化するPythonツール<br>
外部ライブラリは使用しておらず、Windows10 64bit / Python3.10.0で動作確認しています<br>
ダウンロードは[こちら](https://github.com/ike62k/RIFEAutomationToolPython/releases)から

# 注意事項
1. 補完対象のパスに半角スペース(' ')が含まれているとうまく動作しません
2. 補完対象のパスにドット('.')が含まれているとうまく動作しません
3. 'Shell = True'を使用しているので入力次第で予期しない動作を引き起こす可能性があります
4. 同梱されている'RPCconfig.ini'に初期値の設定があるため、先に環境に応じて設定をしてから使用してください
5. このソフトウェアは趣味で制作されたものです。本ソフトウェアの使用によって引き起こされた一切の結果について作者は一切の責任を負いません

# 必要ソフトウェア
1. [rife-ncnn-vulkan.exeと各種プロファイル](https://github.com/nihui/rife-ncnn-vulkan)
2. [ffmpegとffprobe](https://www.ffmpeg.org/)
3. [Python3](https://www.python.org/)

# 対応動画  
入力ファイル : ffmpegで動画ファイルとして読み込めるほとんどすべての映像/音声形式  
出力ファイル : コンテナフォーマット→mov(Quicktime) / 映像コーデック→ユーザー指定 / 音声コーデック→ユーザー指定
  
 # 使い方
1. ダウンロードしたすべてのファイル、フォルダを同一フォルダ(※)にまとめる
2. このレポジトリで配布されているファイルをPythonで実行
3. 表示の指示に従って動画を指定する(記述は※のファイルからの相対パス)
  
# はしがき
そもそもこのファイルは個人的にめんどくさかった作業を簡略化させただけなのでコードの無駄とかが多いのでそこらへんだけよろです
