import cv2
import requests
import base64
import os
import schedule
import time

#plant API
plant_url = "https://plant-disease-detector-pytorch.herokuapp.com/"
# LINEAPI
url = "https://notify-api.line.me/api/notify"
access_token = 'Your Token'
headers = {'Authorization': 'Bearer ' + access_token}

def plant_dia():
    # APIを使用する画像の前処理
    def encodeToBase64(filename):
        with open(filename, "rb") as f:
            img_base64 = base64.b64encode(f.read())
        return img_base64

    #capture = cv2.VideoCapture(1)
    # capture = cv2.VideoCapture("/dev/video1")
    capture = cv2.VideoCapture(0)
    ret, plant_photo = capture.read()
    cv2.imwrite('plant.jpg', plant_photo)

    imgdata = encodeToBase64('plant.jpg').decode('utf-8')

    res = requests.post(plant_url,json = {"image":imgdata})

    message = res
    image = 'plant.jpg'  # png or jpg
    payload = {'message': message}
    files = {'imageFile': open(image, 'rb')}
    r = requests.post(url, headers=headers, params=payload, files=files,)

#x分毎のjob実行を登録
schedule.every(0.5).minutes.do(plant_dia)

#x時間毎のjob実行を登録
#schedule.every(x).hours.do(plant_dia)

# plant_diaの実行監視、指定時間になったらplant_dia関数を実行
while True:
    schedule.run_pending()
    time.sleep(1)