# RIFE AUTOMATION TOOL PYTHON
copyright 2023 びろーど(Veludo)

## はじめに
このプログラムは趣味の一環として作成されたものです。本ソフトウェアを使用したいかなる結果についても作者は責任を負いません。<br>
このソフトウェアはMIT LICENSEにて提供されています。MIT LICENSEは添付しているLICENSEを参照してください。<br>
本ソフトウェアはffmpeg及びffprobeを使用しています。使用しているのはLGPL版であり、動的リンクでの使用としているため本ソフトウェア自体はMIT LICENSEにて公開しています。<br>
ffmpeg及びffprobeのライセンスは.\lib\ffmpeg\LGPL_LICENSE_for_ffmpeg.txtを参照してください。

## 動作(確認済み)環境
- windows10 or windows11
- Python 3.12(以前のVerでも動く可能性はあります※未検証)
- (あったらいいな)Intel,AMD,NVIDIAの外付けGPU

## 使用させていただいているソフトウェア
- [FFmpeg(LGPL)](https://github.com/BtbN/FFmpeg-Builds/releases/tag/autobuild-2023-11-11-12-54)
- [FFprobe(LGPL)](https://github.com/BtbN/FFmpeg-Builds/releases/tag/autobuild-2023-11-11-12-54)
- [RIFE-ncnn-Vulkan](https://github.com/nihui/rife-ncnn-vulkan/releases/tag/20221029)

## どんなソフトウェア？
映像の前後コマから間のコマを生成するソフトウェア[RIFE-ncnn-Vulkan](https://github.com/nihui/rife-ncnn-vulkan)をより便利に活用するためのソフトウェアです。<br>
FFmpegとRIFE-ncnn-Vulkanを組み合わせて、元動画を2倍補完したものを生成します。<br>
動作にはWindows環境とそこで動作するPythonが必要です。Pythonの外部ライブラリは使用していません。<br>
お好みのFFmpeg,FFProbeビルドを代わりに使用することも可能です。(ライセンスにはご注意ください)<br>

## 使用出来る元動画ファイル
- お使いのFFmpegにて映像streamを画像へとエンコードできるもの
- 音声streamが含まれているもの(今後のアップデートで音声を含まない動画にも対応予定)
- 映像総フレーム数が2~5000000000であるもの
- 映像が極度に低ビットレートでないもの(効果が薄れます)

## 使い方
1. Pythonをインストールします。
2. 本プロジェクトのReleaseページからソースコードをダウンロードします。
3. 適当な場所で展開します
4. App.pyを実行します

## 各種設定について
本ソフトウェアでは、ユーザーごとの環境に合わせて柔軟に設定を操作できるよう、configファイルを設定しています。<br>
全てのconfigファイルは.\setting内に存在します。

### pyrife-ncnn-vulkan.ini
RIFE-ncnn-Vulkan用のconfigです。
- `input_folder` RIFEが処理する対象となる、補完処理前のフレームのあるフォルダを指定します。
- `output_folder` RIFEが処理したあとの、補完処理後のフレームのあるフォルダを指定します。
- `output_extension` RIFEが処理したフレームのファイル形式を指定します。
- `rifeexe` RIFE-ncnn-Vulkan.exeの場所を指定します。
- `rifever` RIFEの補完に使用するモデルのバージョンを指定します。
- `rifeusage` RIFEの動作スレッド数を指定します(多いとメモリ使用量が増えます)
- `rifegpu` RIFEが使用するGPUのナンバーを指定します(-1でCPU処理)
- `ratio` 補完倍率を指定します **※注：現段階では`ratio`に関わらず2倍で動作します**

## 注意事項
- FFmpeg,FFprobe,RIFE-ncnn-Vulkanは全て実行ファイルを`subprocess`で呼び出しています。
    その際に、`shell=True`を使用しています。設定値にシェルがコマンドと誤認識する値があると、シェルインジェクションなどの危険性があります。
- 著作権で保護された映像の加工及び公開は法律に反する場合があります。作者は責任を負いかねますので、使用方法にはお気をつけください。

## 既知の不具合
- 音声streamを含まない動画が処理できない問題
- `subprocess`において`shell=True`を使用していることによる誤作動のリスク

## 修正及び機能追加予定
- 音声streamを含まない動画への対応
- (時期未定)`subproces`sの`shell=True`を使用しない設計へのリファクタリング
- 補完倍率`ratio`の実装
- PysimpleGUIを使用したGUIの実装
- fletを使用したGUIの実装

