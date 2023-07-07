import requests
import cv2
import websockets
import asyncio
import json
from misskey import Misskey
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import threading

showTL = True
conf_dir = "conf.json"
test = False
output = []

class S(BaseHTTPRequestHandler):

	def _set_headers(self):

		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):

		self._set_headers()
		self.wfile.write("<html><body><h1>GET message receive!</h1></body></html>")

	def do_POST(self):

		self._set_headers()
		self.wfile.write("<html><body><h1>POST message receive!</h1></body></html>")



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
        #メニュー
        img = putText_jp(img, "Misskey Client \n   for Stormworks", (5, 5), 6, (0, 0, 0))
        img = putText_jp(img, "Home", (5, 25), 6, (0, 0, 0))
        img = putText_jp(img, "NOTE", (5, 35), 6, (0, 0, 0))
        #TL
        tl_text = ""
        for i in output:
            tl_text += f"   {i[0]}\n{i[1]}\n"
        img = putText_jp(img, tl_text, (75,5), 6, (0, 0, 0))
        cv2.imshow('image', img)
        cv2.waitKey(10)
        await asyncio.sleep(0.01)

async def getTL(token):
    global output
    #TL取得
    print("try to connect")
    uri = f"wss://stormskey.works/streaming?i={token}"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
	        "type": 'connect',
	        "body": {
		        "channel": 'localTimeline',
		        "id": '0',
            }
        }))
        print("connected")
        while True:
            data = json.loads(await ws.recv())
            output.insert(0,[str(data["body"]["body"]["user"]["name"]),str(data["body"]["body"]["text"])])
            print(output)
            if len(output) > 20:
                output = output[:-1]

def cv2stw(disp_array):
    #OpenCVで描画したのをストわにhttpで投げる
    return

def getconf(file_dir):
    with open(file_dir,"r") as json_open:
        json_load = json.load(json_open)
    return json_load
async def run():
    #非同期で描画処理とTL更新を同時にする
    await asyncio.gather(disp(),getTL(TOKEN))

conf = getconf(conf_dir)
TOKEN= conf["token"]
print(TOKEN)
msk = Misskey('stormskey.works', i=TOKEN)
MY_ID = msk.i()['id']
WS_URL='wss://stormskey.works/streaming?i='+TOKEN
if __name__ == "__main__" and (not test):
    #asyncio.run(getTL(conf["token"]))
    print("not Test mode")
    asyncio.run(run())
elif __name__ =="__main__":
    asyncio.run(getTL(TOKEN))