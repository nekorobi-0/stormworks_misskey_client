import requests
import cv2
import websockets
import asyncio
import json
from misskey import Misskey
import threading
showTL = True
conf_dir = "conf.json"
async def disp():
    #描画系
    pass

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
            output = data["body"]["body"]["user"]["name"]+":"+data["body"]["body"]["text"]
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
if __name__ == "__main__":
    #asyncio.run(getTL(conf["token"]))
    asyncio.run(run())