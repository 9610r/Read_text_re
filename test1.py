# coding: UTF-8

import os
import sys
import time
import hashlib
import threading
import subprocess

from win32con import *
from win32gui import *
from win32process import *

# 共通設定
waitSec = 0.5
windowName = "VOICEROID＋ 結月ゆかり EX"

def talk(inputText):
	# 出力先ディレクトリ作成
	outdir = "./output/"
	try:
		os.mkdir(outdir)
	except:
		pass

	# ファイルが存在してたらやめる
	outfile = outdir + hashlib.md5(inputText.encode("utf-8")).hexdigest() + ".mp3"
	if os.path.exists(outfile):
		return outfile

	# 一時ファイルが存在している間は待つ
	tmpfile = "tmp.wav"
	while True:
		if os.path.exists(outfile):
			time.sleep(waitSec)
		else:
			break

	while True:
		# VOICEROIDプロセスを探す
		window = FindWindow(None, windowName) or FindWindow(None, windowName + "*")

		# 見つからなかったらVOICEROIDを起動
		if window == 0:
			subprocess.Popen(["C:\Program Files (x86)\AHS\VOICEROID+\YukariEX\VOICEROID.exe"])
			time.sleep(3 * waitSec)
		else:
			break

	while True:
		# ダイアログが出ていたら閉じる
		errorDialog = FindWindow(None, "エラー") or FindWindow(None, "注意") or FindWindow(None, "音声ファイルの保存")
		if errorDialog:
			SendMessage(errorDialog, WM_CLOSE, 0, 0)
			time.sleep(waitSec)
		else:
			break

	# 最前列に持ってくる
	SetWindowPos(window, HWND_TOPMOST, 0, 0, 0, 0, SWP_SHOWWINDOW | SWP_NOMOVE | SWP_NOSIZE)

	# 保存ダイアログの操作
	def enumDialogCallback(hwnd, param):
		className = GetClassName(hwnd)
		winText = GetWindowText(hwnd)

		# ファイル名を設定
		if className.count("Edit"):
			SendMessage(hwnd, WM_SETTEXT, 0, tmpfile)

		# 保存する
		if winText.count("保存"):
			SendMessage(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, 0)
			SendMessage(hwnd, WM_LBUTTONUP, 0, 0)

	# 音声の保存
	def save():
		time.sleep(waitSec)

		# ダイアログがあれば操作する
		dialog = FindWindow(None, "音声ファイルの保存")
		if dialog:
			EnumChildWindows(dialog, enumDialogCallback, None)
			return

		# 再試行
		save()

	# VOICEROIDを操作
	def enumCallback(hwnd, param):
		className = GetClassName(hwnd)
		winText = GetWindowText(hwnd)

		# テキストを入力する
		if className.count("RichEdit20W"):
			SendMessage(hwnd, WM_SETTEXT, 0, inputText)

		if winText.count("音声保存"):
			# 最小化解除
			ShowWindow(window, SW_SHOWNORMAL)

			# 保存ダイアログ操作用スレッド起動
			threading.Thread(target=save).start()

			# 保存ボタンを押す
			SendMessage(hwnd, WM_LBUTTONDOWN, MK_LBUTTON, 0)
			SendMessage(hwnd, WM_LBUTTONUP, 0, 0)

	# VOICEROIDにテキストを読ませる
	EnumChildWindows(window, enumCallback, None)

	# プログレスダイアログが表示されている間は待つ
	while True:
		if FindWindow(None, "音声保存"):
			time.sleep(waitSec)
		else:
			break

	# MP3に変換
	subprocess.run(["ffmpeg", "-i", tmpfile, "-acodec", "libmp3lame", "-ab", "128k", "-ac", "2", "-ar", "44100", outfile])

	# 一時ファイルが存在していたら消す
	try:
		os.remove(tmpfile)
		os.remove(tmpfile.replace("wav", "txt"))
	except:
		pass

	return outfile

#print(talk(sys.argv[1]))
