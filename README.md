# MQTT心電図波形表示プログラム　概要
## 何をするものか？
MQTTを使って送信される12誘導心電図の波形を表示するプログラムです。

## 動作環境
Pythonが動作する環境で動作します。

## インストールの方法（Windows）
1. Pythonと必要なパッケージのインストール

 - Pythonのインストール
https://www.python.org/downloads/ よりインストーラーをダウンロードして案内に従ってインストールします。pythonをPATHに加えるチェックを付けておきます。

 - Windows PowerShell またはコマンドプロンプト（cmd.exe）を起動します。

 - NumPy (Python の数値計算ライブラリ)  のインストール
コマンドラインに
py -m pip install numpy
と入力してenter を押下

 - Paho (Python で MQTTのクライアント(Publisher/Subscriber)を実装するためのライブラリ) のインストール
コマンドラインに
py -m pip install paho-mqtt
と入力してenter を押下

 - DearPyGui (Python のグラフィカルインタフェースを実装するためのライブラリ) のインストール
コマンドラインに
py -m pip install dearpygui
と入力してenter を押下

2. ファイルの設定
テキストエディタにてmonitor_ecg12.py の最初を編集します。

IP="127.0.0.1"
PORT=1883
TOPIC="Undefined"
ID="YourID"
PW="PassWord"
SEC=10

の部分をpublisherなどから情報を得て適切に変更します。

3. 実行
コマンドラインから
python monitor_ecg12.py
と入力してenter を押下。すると画面が開いてデータを受信し、表示を始めます。


## インストールの方法（Ubuntu）
Python3がイントールされているUbuntu23.04を例にとって説明します。
補助ライブラリとして、dearpyguiとnumpyとGLFW libraryが必要です。

1. 次を順に実行します。
pip3 install dearpygui
pip3 install numpy
pip3 install paho-mqtt
pip3 install pyglfw

2. 「インストールの方法（Windows）」の2を実行します。

3. コマンドラインから
python3 monitor_ecg12.py
と入力してenter を押下。すると画面が開いてデータを受信し、表示を始めます。
Screenshot.pngのような表示が得られれば成功です。

