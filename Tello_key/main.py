#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello	        # tello.pyをインポート
import time	          # time.sleepを使いたいので
from kbhit import *   # kbhit.pyをインポート

# メイン関数本体
def main():
	# kbhitのためのおまじない
	atexit.register(set_normal_term)
	set_curses_term()

	# Telloクラスを使って，droneというインスタンス(実体)を作る
	drone = tello.Tello('', 8889) 

	current_time = time.time()	# 現在時刻の保存変数
	pre_time = current_time		# 5秒ごとの'command'送信のための時刻変数

	#Ctrl+cが押されるまでループ
	try:
		while True:
			if kbhit():     # 何かキーが押されるのを待つ
				key = getch()   # 1文字取得

				# キーに応じた処理
				if key == 't':		# 離陸
					drone.takeoff()
				elif key == 'l':	# 着陸
					drone.land()
				elif key == 'w':	# 前進
					drone.move_forward(0.3)
				elif key == 's':	# 後進
					drone.move_backward(0.3)
				elif key == 'a':	# 左移動
					drone.move_left(0.3)
				elif key == 'd':	# 右移動
					drone.move_right(0.3)
				elif key == 'q':	# 左旋回
					drone.rotate_ccw(20)
				elif key == 'e':	# 右旋回
					drone.rotate_cw(20)
				elif key == 'r':	# 上昇
					drone.move_up(0.3)
				elif key == 'f':	# 下降
					drone.move_down(0.3)

			time.sleep(0.3)	# 適度にウェイトを入れてCPU負荷を下げる

			# 5秒おきに'command'を送って、Telloが自動終了しないようにする
			current_time = time.time()	# 現在時刻を取得
			if current_time - pre_time > 5.0 :	# 前回時刻から5秒以上経過しているか？
				drone.send_command('command')	# 'command'送信
				pre_time = current_time			# 前回時刻を更新

	except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
		print( "SIGINTを検知" )

	# telloクラスを削除
	del drone


# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":		# importされると"__main__"は入らないので，実行かimportかを判断できる．
	main()    # メイン関数を実行
