#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tello		# tello.pyをインポート
import time			# time.sleepを使いたいので
import pygame		# pygameでジョイスティックを読む

def main():
	# pygameの初期化とジョイスティックの初期化
	pygame.init()
	joy = pygame.joystick.Joystick(0)
	joy.init()

	# Telloクラスを使って，droneというインスタンス(実体)を作る
	drone = tello.Tello('', 8889, command_timeout=.01)  

	time.sleep(0.5)		# 通信が安定するまでちょっと待つ

	current_time = time.time()	# 現在時刻の保存変数
	pre_time = current_time		# 5秒ごとの'command'送信のための時刻変数

	#Ctrl+cが押されるまでループ
	try:
		while True:
			# Joystickの読み込み
			rud = int( joy.get_axis(0)*100 )
			ele = int( joy.get_axis(1)*-100 )
			air = int( joy.get_axis(2)*100 )
			thr = int( joy.get_axis(3)*-100 )
			btn0 = joy.get_button(0)
			btn1 = joy.get_button(1)
			btn2 = joy.get_button(2)
			btn3 = joy.get_button(3)
			pygame.event.pump()		# イベントの更新

			#print("ele=%d  rud=%d  thr=%d  air=%d  btn0=%d  btn1=%d  btn2=%d  btn3=%d"%(ele, rud, thr, air, btn0, btn1, btn2, btn3))

			drone.send_command('rc %s %s %s %s'%(air, ele, thr, rud) )

			if btn1 == 1:		# 離陸
				drone.takeoff()
			elif btn2 == 1:	# 着陸
				drone.land()

			time.sleep(0.03)	# 適度にウェイトを入れてCPU負荷を下げる

			# 5秒おきに'command'を送って、死活チェックを通す
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
