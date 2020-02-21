#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello		# tello.pyをインポート
import time			# time.sleepを使いたいので
import cv2			# OpenCVを使うため
import zbar			# QRコードの認識

# メイン関数
def main():
	# Telloクラスを使って，droneというインスタンス(実体)を作る
	drone = tello.Tello('', 8889, command_timeout=10.0)  

	time.sleep(0.5)		# 通信が安定するまでちょっと待つ

	# zbarによるQRコード認識の準備
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')

	pre_qr_msg = None	# 前回見えたQRコードのテキストを格納
	count = 0			# 同じID番号が見えた回数を記憶する変数
	commands = None		# 認識したQRコードをTelloのコマンドとして使う
	command_index = 0	# 実行するコマンドの番号
	flag = 0			# 自動制御のフラグは初期0

	current_time = time.time()	# 現在時刻の保存変数
	pre_time = current_time		# 5秒ごとの'command'送信のための時刻変数

	#Ctrl+cが押されるまでループ
	try:
		while True:

			# (A)画像取得
			frame = drone.read()	# 映像を1フレーム取得
			if frame is None or frame.size == 0:	# 中身がおかしかったら無視
				continue 

			# (B)ここから画像処理
			image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)		# OpenCV用のカラー並びに変換する
			small_image = cv2.resize(image, dsize=(480,360) )	# 画像サイズを半分に変更


			# 自動制御フラグが0FF(=0)のときには，QRコード認識処理を行う
			if flag == 0:
				# QRコード認識のための処理
				gray_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)		# zbarで認識させるために，グレイスケール画像にする 
				rows, cols = gray_image.shape[:2]		# 画像データから画像のサイズを取得(480x360)
				image = zbar.Image(cols, rows, 'Y800', gray_image.tostring())	# zbarのイメージへ変換
				scanner.scan(image)		# zbarイメージをスキャンしてQRコードを探す

				# 一度に２つ以上のQRコードを見せるのはNG
				for symbol in image:
					qr_msg = symbol.data

					# 50回同じQRコードが見えたらコマンド送信する処理
					try:
						if qr_msg != None:	# qr_msgが空(QRコードが１枚も認識されなかった)場合は何もしない

							if qr_msg == pre_qr_msg:	# 今回認識したqr_msgが前回のpre_qr_msgと同じ時には処理
								count+=1			# 同じQRコードが見えてる限りはカウンタを増やす

								if count > 50:		# 50回同じQRコードが続いたら，コマンドを確定する
									print('QR code 認識 : %s' % (qr_msg) )
									commands = qr_msg
									command_index = 0
									flag = 1	# 自動制御を有効にする

									count = 0	# コマンド送信したらカウント値をリセット
							else:
								count = 0

							pre_qr_msg = qr_msg	# 前回のpre_qr_msgを更新する

						else:
							count = 0	# 何も見えなくなったらカウント値をリセット

					except ValueError, e:	# if ids != None の処理で時々エラーが出るので，try exceptで捕まえて無視させる
						print("ValueError")

				del image



			# 自動制御フラグがON(=1)のときは，コマンド処理だけを行う
			if flag == 1:
				print commands[command_index]
				key = commands[command_index]	# commandsの中には'TLudcwflrW'のどれかの文字が入っている
				if key == 'T':
					drone.takeoff()				# 離陸
					time.sleep(5)
				elif key == 'L':
					flag = 0
					drone.land()				# 着陸
					time.sleep(4)
				elif key == 'u':
					drone.move_up(0.5)			# 上昇
				elif key == 'd':
					drone.move_down(0.5)		# 下降
				elif key == 'c':
					drone.rotate_ccw(20)		# 左旋回
				elif key == 'w':
					drone.rotate_cw(20)			# 右旋回
				elif key == 'f':
					drone.move_forward(0.5)		# 前進
				elif key == 'b':
					drone.move_backward(0.5)	# 後進
				elif key == 'l':
					drone.move_left(0.5)		# 左移動
				elif key == 'r':
					drone.move_right(0.5)		# 右移動
				elif key == 'W':
					time.sleep(5)		# ウェイト

				command_index += 1
				pre_time = time.time()


			# (X)ウィンドウに表示
			cv2.imshow('OpenCV Window', gray_image)	# ウィンドウに表示するイメージを変えれば色々表示できる

			# (Y)OpenCVウィンドウでキー入力を1ms待つ
			key = cv2.waitKey(1)
			if key == 27:					# k が27(ESC)だったらwhileループを脱出，プログラム終了
				break
			elif key == ord('t'):
				drone.takeoff()				# 離陸
			elif key == ord('l'):
				flag = 0
				drone.land()				# 着陸

			# (Z)14秒おきに'command'を送って、死活チェックを通す
			current_time = time.time()	# 現在時刻を取得
			if current_time - pre_time > 14.0 :	# 前回時刻から14秒以上経過しているか？
				drone.send_command('command')	# 'command'送信
				pre_time = current_time			# 前回時刻を更新

	except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
		print( "SIGINTを検知" )

	# telloクラスを削除
	del drone


# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":		# importされると"__main__"は入らないので，実行かimportかを判断できる．
	main()    # メイン関数を実行
