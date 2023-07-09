import cv2
import websockets
import asyncio
import json
from misskey import Misskey
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import romaji
import requests
showTL = True
conf_dir = "conf.json"
domain = "stormskey.works"
test = False
output = []
now_img = []
TL_name = 'localTimeline'
compo_screen = []
touch_pos = []
button_status = {"NOTE":False,"Home":False,"selectTL":False,"selectSV":False}
toggle_status = ""
importing_text = ""
key_old = -10
key_id = {-10:"",-9:"9",-8:"8",-7:"7",-6:"6",-5:"5",-4:"4",-3:"3",-2:"2",-1:"1",0:"0",
          1:"a",2:"b",3:"c",4:"d",5:"e",6:"f",7:"g",8:"h",9:"i",10:"j",11:"k",12:"l",13:"m",
          14:"n",15:"o",16:"p",17:"q",18:"r",19:"s",20:"t",21:"u",22:"v",23:"w",24:"x",25:"y",26:"z",27:" ",28:"\n",29:";"}
class S(BaseHTTPRequestHandler):

    def _set_headers(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global compo_screen
        global touch_pos
        if self.requestline[5:8] == "stw":
            compo_screen = self.requestline[8:-9].split(",")
            compo_screen.pop(0)
            touch_pos = [int(compo_screen[0]),int(compo_screen[1])]
            print(compo_screen)
        self._set_headers()
        self.wfile.write(str(now_img).encode())
    
    def do_POST(self):
        
        self._set_headers()
        self.wfile.write("<html><body><h1>POST message receive!</h1></body></html>".encode())

def run_http_server(server_class=HTTPServer, handler_class=S, port=8888):

	# startup HTTP server
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('HTTP server started....')
	httpd.serve_forever()



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

def disp():
    #描画系とタッチ処理
    global now_img
    while True:
        #タッチ処理
        def intouch(txy,xy,xy2):#(tx,ty),(x,y),(x2,y2)..xyは左上xy2は右下
            if len(txy) != 2:
                return False
            if xy[0]<=txy[0] and txy[0]<=xy2[0] and xy[1]<txy[1] and txy[1]<=xy2[1]:
                return True
            else: 
                return False
        def selectable_text(img,text,xy,fontsize,color):
            id = text
            global toggle_status
            sel = intouch(touch_pos,xy,(xy[0]+60,xy[1]+8))
            if (button_status[str(id)] != sel) and sel:
                print("yes")
                if toggle_status == id:
                    toggle_status = ""
                else:
                    toggle_status = id
            button_status[str(id)] = sel
            sel = toggle_status == id
            if sel:
                of = 7
            else:
                of = 0
            img = putText_jp(img, text, (xy[0]+of,xy[1]), fontsize,color)
            return img
        home = intouch(touch_pos,(5,25),(29,33))

        #描画のためのやつ
        img = cv2.imread('background.png')
        cv2.line(img,(70,0),(70,160),(0,0,0))
        cv2.line(img,(0,0),(0,160),(0,0,0))
        #メニュー
        img = putText_jp(img, "Misskey Client \n   for Stormworks", (5, 5), 6, (0, 0, 0))
        img = selectable_text(img, "Home", (5, 25), 6, (0, 0, 0))
        img = selectable_text(img, "NOTE", (5, 35), 6, (0, 0, 0))
        img = selectable_text(img, "selectTL", (5, 45), 6, (0, 0, 0))
        img = selectable_text(img, "selectSV", (5, 55), 6, (0, 0, 0))
        img = putText_jp(img, f"Connecting to\n{domain}", (5, 140), 6, (0, 0, 0))
        if toggle_status == "Home":
            #TL
            tl_text = ""
            for i in output:
                tl_text += f"   {i[0]}\n{i[1]}\n"
            img = putText_jp(img, tl_text, (75,5), 6, (0, 0, 0))
        elif toggle_status == "NOTE":
            global importing_text
            global key_old
            list_lang = ["jp","en"]
            img = putText_jp(img, list_lang[len(importing_text.split(";"))%2], (95, 10), 6, (0, 0, 0))
            img = putText_jp(img,"送信", (150, 10), 6, (0, 0, 0))
            key = int(compo_screen[2])
            if key != key_old:
                if key == 30:
                    importing_text = importing_text[:-1]
                else:
                    importing_text += key_id[key]
            key_old = key
            show_text = ""
            for i,text in enumerate(importing_text.split(";")):
                if i%2 == 0:
                    show_text +=text
                else:
                    show_text += romaji.romaji2hiragana(text)
            if intouch(touch_pos,(150,10),(180,20))and show_text != "":
                msk.notes_create(text=show_text)
                importing_text = ""
            img = putText_jp(img,show_text, (85, 20), 6, (0, 0, 0))
        show_img = cv2.resize(img, (964, 480))
        cv2.imshow('image', show_img)
        now_img = cv2stw(img,288,160)
        cv2.waitKey(10)

async def getTL(token):
    global output
    #TL取得
    while True:
        print("try to connect")
        uri = f"wss://{domain}/streaming?i={token}"
        async with websockets.connect(uri) as ws:
            await ws.send(json.dumps({
	            "type": 'connect',
	            "body": {
		            "channel": TL_name,
		            "id": TL_name,
                }
            }))
            print("connected")
            while True:
                try:
                    data = json.loads(await ws.recv())
                except websockets.exceptions.ConnectionClosedError:
                    break
                output.insert(0,[str(data["body"]["body"]["user"]["name"]),str(data["body"]["body"]["text"])])
                if len(output) > 20:
                    output = output[:-1]
        await asyncio.sleep(1)
def cv2stw(disp_array,x,y):
    img = cv2.resize(disp_array,(x,y))
    #OpenCVで描画したのをストわにhttpで投げるための処理
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#モノクロ
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    now_img_raw = img.tolist()
    now_img = []
    for i in now_img_raw:
        now_img += i
    f = 255
    c = 0
    now_img2 = []
    for i in now_img:
        c += 1
        if f != i:
            now_img2.append(c)
            c = 0
        f = i
    now_img2.pop(0)
    now_img = re.sub(r'[^(0-9|,)]',"", str(now_img2))
    return now_img

def getconf(file_dir):
    with open(file_dir,"r") as json_open:
        json_load = json.load(json_open)
    return json_load


conf = getconf(conf_dir)
TOKEN= conf[domain]["token"]
print(TOKEN)
msk = Misskey(domain, i=TOKEN)
MY_ID = msk.i()['id']
WS_URL=f'wss://{domain}/streaming?i={TOKEN}'
if __name__ == "__main__" and (not test):
    #asyncio.run(getTL(conf["token"]))
    print("not Test mode")
    #非同期で描画処理とTL更新とhttp鯖ホストを同時にする
    thread1 = threading.Thread(target=run_http_server)#http鯖
    thread2 = threading.Thread(target=disp)#描画系
    thread1.start()
    thread2.start()
    asyncio.run(getTL(TOKEN))
elif __name__ =="__main__":
    asyncio.run(getTL(TOKEN))