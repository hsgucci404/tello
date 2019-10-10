#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

# ArUcoのライブラリを導入
aruco = cv2.aruco

# 4x4のマーカー，ID番号は50までの辞書を使う
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

def main():
	# 10枚のマーカーを作るために10回繰り返す
	for i in range(10):

		ar_image = aruco.drawMarker(dictionary, i, 150)		# ID番号は i ，150x150ピクセルでマーカー画像を作る．

		fileName = "ar" + str(i).zfill(2) + ".png"	# ファイル名を "ar0x.png" の様に作る

		cv2.imwrite(fileName, ar_image)		# マーカー画像を保存する


# "python MakeMarker_0to9.py"として実行された時だけ動く様にするおまじない処理
if __name__ == "__main__":
	main()	# メイン関数を実行
