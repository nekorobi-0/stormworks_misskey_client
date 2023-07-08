import main
import threading
import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import math
now_img = []
t = 0
af = 0
def disp():
    global now_img
    cap = cv2.VideoCapture('badapple.mp4')
    while True:
        ret, img = cap.read()
        img = cv2.resize(img,(213,160))
        img = cv2.line(img,(0,0),(0,160),(0,0,0))
        img = cv2.line(img,(213,0),(213,160),(255,255,255))
        now_img = main.cv2stw(img,213,160)
        cv2.imshow('Video', img)
        cv2.waitKey(26)
class S(BaseHTTPRequestHandler):

    def _set_headers(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        global t
        global af
        ot = t
        t = time.time()
        af = (1 /(t - ot))*0.1 +af *0.9
        print(math.floor(af*10)/10)
        self._set_headers()
        self.wfile.write(str(now_img).encode())
    
    def do_POST(self):
        
        self._set_headers()
        self.wfile.write("<html><body><h1>POST message receive!</h1></body></html>".encode())
def run_http_server(server_class=HTTPServer, handler_class=S, port=8889):

	# startup HTTP server
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print('HTTP server started....')
	httpd.serve_forever()
if __name__ == '__main__':
    thread1 = threading.Thread(target=run_http_server)#http鯖
    thread1.start()
    disp()
