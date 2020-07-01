# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error
import time

import cv2

http_url = 'https://api-cn.faceplusplus.com/facepp/v3/compare'
key = "cW2DWAvBTk7lsoo8iCgR4TzWrYpVP_qP"
secret = "NYXhr6g0rTDtKNloY6xyGK1fUpyL_t5W"
filepath_origin = r'data/data_faces_from_camera/person_1/img_face_1.jpg'
filepath = r"C:\Users\tq\Desktop\1.jpg"
cap = cv2.VideoCapture(0)
cap.set(3, 480)

while cap.isOpened():
    flag, img_rd = cap.read()
    kk = cv2.waitKey(1)
    # 按下 q 键退出
    if kk == ord('q'):
        break
    else:
        cv2.imwrite(r"C:\Users\tq\Desktop\1.jpg", img_rd)
        boundary = '----------%s' % hex(int(time.time() * 1000))
        data = []
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
        data.append(key)
        data.append('--%s' % boundary)
        data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
        data.append(secret)
        data.append('--%s' % boundary)
        fr = open(filepath, 'rb')
        data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file1')
        data.append('Content-Type: %s\r\n' % 'application/octet-stream')
        data.append(fr.read())
        fr.close()
        data.append('--%s' % boundary)

        fr = open(filepath_origin, 'rb')
        data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file2')
        data.append('Content-Type: %s\r\n' % 'application/octet-stream')
        data.append(fr.read())
        fr.close()
        data.append('--%s--\r\n' % boundary)

        for i, d in enumerate(data):
            if isinstance(d, str):
                data[i] = d.encode('utf-8')

        http_body = b'\r\n'.join(data)

        # build http request
        req = urllib.request.Request(url=http_url, data=http_body)

        # header
        req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

        try:

            # post data to server
            resp = urllib.request.urlopen(req, timeout=5)
            # get response
            qrcont = resp.read()

            # if you want to load as json, you should decode first,
            # for example: json.loads(qrount.decode('utf-8'))
            # try:
            #     print(json.loads(qrcont.decode('utf-8'))['faces'][0]['attributes']['smile'])
            #     print(json.loads(qrcont.decode('utf-8'))['faces'][0]['attributes']['emotion'])
            # except:
            #     pass
            print(json.loads(qrcont.decode('utf-8'))['confidence'])
            # for face in faces:
            #     rec = face['face_rectangle']
            #     cv2.rectangle(img_rd, tuple([rec['left'], rec['top']]),
            #                   tuple([rec['left'] + rec['width'], rec['top'] + rec['height']]),
            #                   (0, 255, 0), 2)
            cv2.imshow("camera", img_rd)
        except urllib.error.HTTPError as e:
            print(e.read().decode('utf-8'))
cap.release()
cv2.destroyAllWindows()
