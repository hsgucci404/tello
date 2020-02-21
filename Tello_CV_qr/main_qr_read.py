#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello		# tello.pyをインポート
import time			# time.sleepを使いたいので
import cv2			# OpenCVを使うため
import zbar			# QRコードの認識
import numpy as np	# 四角形ポリゴンの描画のために必要

# メイン関数
def main():
	# Telloクラスを使って，droneというインスタンス(実体)を作る
	drone = tello.Tello('', 8889, command_timeout=1.0)  

	time.sleep(0.5)		# 通信が安定するまでちょっと待つ

	# zbarによるQRコード認識の準備
	scanner = zbar.ImageScanner()
	scanner.parse_config('enable')

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
			
			# QRコード認識のための処理
			gray_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2GRAY)		# zbarで認識させるために，グレイスケール画像にする 
			rows, cols = gray_image.shape[:2]		# 画像データから画像のサイズを取得(480x360)
			image = zbar.Image(cols, rows, 'Y800', gray_image.tostring())	# zbarのイメージへ変換

			scanner.scan(image)		# zbarイメージをスキャンしてQRコードを探す
			
			# スキャン結果はimageに複数個入っているので，for文でsymbolという名で取り出して繰り返す
			for symbol in image:
				qr_type = symbol.type	# 認識したコードの種別
				qr_msg = symbol.data	# QRコードに書かれたテキスト
				qr_positions = symbol.location	# QRコードを囲む矩形の座標成分
				print('QR code : %s, %s, %s'%(qr_type, qr_msg, str(qr_positions)) )		# 認識結果を表示
				
				# 認識したQRコードを枠線で囲む
				pts = np.array( qr_positions )		# NumPyのarray形式にする
				cv2.polylines(small_image, [pts], True, (0,255,0), thickness=3)		# ポリゴンを元のカラー画像に描画

			del image	# zbarイメージの削除

			# (X)ウィンドウに表示
			cv2.imshow('OpenCV Window', small_image)	# ウィンドウに表示するイメージを変えれば色々表示できる

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
