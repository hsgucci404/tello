#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello		# tello.pyをインポート
import time			# time.sleepを使いたいので
import pygame		# pygameでジョイスティックを読む

def main():
	# pygameの初期化とジョイスティックの初期化
	pygame.init()
	joy = pygame.joystick.Joystick(0)	# ジョイスティック番号はjstest-gtkで確認しておく
	joy.init()

	# Telloクラスを使って，droneというインスタンス(実体)を作る
	#   コマンドの応答タイムアウトを0.01秒(10ms)にして，rcコマンドの連送に耐えられるようにする
	drone = tello.Tello('', 8889, command_timeout=.01 )

	time.sleep(0.5)		# 通信が安定するまでちょっと待つ

	#Ctrl+cが押されるまでループ
	try:
		while True:
			# Joystickの読み込み
			#   get_axisは　-1.0〜0.0〜+1.0 で変化するので100倍して±100にする
			#   プラスマイナスの方向が逆の場合は-100倍して反転させる
			a = int( joy.get_axis(2)*100 )		# aは左右移動
			b = int( joy.get_axis(1)*-100 )		# bは前後移動
			c = int( joy.get_axis(3)*-100 )		# cは上下移動
			d = int( joy.get_axis(0)*100 )		# dは旋回
			btn0 = joy.get_button(0)
			btn1 = joy.get_button(1)
			btn2 = joy.get_button(2)
			btn3 = joy.get_button(3)
			pygame.event.pump()		# イベントの更新

			# プラスマイナスの方向や離陸/着陸に使うボタンを確認するためのprint文
			#print("l/r=%d  f/b=%d  u/d=%d  cw/ccw=%d  btn0=%d  btn1=%d  btn2=%d  btn3=%d"%(a, b, c, d, btn0, btn1, btn2, btn3))

			# rcコマンドを送信
			drone.send_command( 'rc %s %s %s %s'%(a, b, c, d) )

			if btn1 == 1:		# 離陸
				drone.takeoff()
			elif btn2 == 1:		# 着陸
				drone.land()

			time.sleep(0.03)	# 適度にウェイトを入れてCPU負荷を下げる

	except( KeyboardInterrupt, SystemExit):    # Ctrl+cが押されたら離脱
		print( "SIGINTを検知" )

	# telloクラスを削除
	del drone


# "python main.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":		# importされると"__main__"は入らないので，実行かimportかを判断できる．
	main()    # メイン関数を実行
