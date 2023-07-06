import requests
import cv2
import websockets
import asyncio
import json
from misskey import Misskey
import numpy as np
from PIL import ImageFont, ImageDraw, Image
showTL = True
conf_dir = "conf.json"
test = True

def putText_jp(img, text, point, size, color):
    #https://monomonotech.jp/kurage/raspberrypi/opencv_japanese.html
    #Notoフォントとする
    font = ImageFont.truetype('K6X8.ttf',size)

    #imgをndarrayからPILに変換
    img_pil = Image.fromarray(img)

    #drawインスタンス生成
    draw = ImageDraw.Draw(img_pil)

    #テキスト描画
    draw.text(point, text, fill=color, font=font)

    #PILからndarrayに変換して返す
    return np.array(img_pil)

async def disp():
    #描画系
    while True:
        img = cv2.imread('background.png')
        cv2.line(img,(70,0),(70,160),(0,0,0))
        img = putText_jp(img, "Misskey Client \n   for Stormworks", (5, 5), 6, (0, 0, 0))
        img = putText_jp(img, "Home", (5, 25), 6, (0, 0, 0))
        img = putText_jp(img, "NOTE", (5, 35), 6, (0, 0, 0))
        cv2.imshow('image', img)
        cv2.waitKey(1)

async def getTL(token):
    #TL取得
    uri = f"wss://stormskey.works/streaming?i={token}"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
	        "type": 'connect',
	        "body": {
		        "channel": 'localTimeline',
		        "id": '0',
            }
        }))
        while True:
            data = json.loads(await ws.recv())
            output = str(data["body"]["body"]["user"]["name"])+":"+str(data["body"]["body"]["text"])
            print(output)

def cv2stw(disp_array):
    #OpenCVで描画したのをストわにhttpで投げる
    return

def getconf(file_dir):
    with open(file_dir,"r") as json_open:
        json_load = json.load(json_open)
    return json_load
async def run():
    #非同期で描画処理とTL更新を同時にする
    await asyncio.gather(disp(),getTL(conf["token"]))

conf = getconf(conf_dir)
TOKEN= conf["token"]
print(TOKEN)
msk = Misskey('stormskey.works', i=TOKEN)
MY_ID = msk.i()['id']
WS_URL='wss://stormskey.works/streaming?i='+TOKEN
if __name__ == "__main__" and not test:
    #asyncio.run(getTL(conf["token"]))
    asyncio.run(run())
elif __name__ =="__main__":
    asyncio.run(disp())