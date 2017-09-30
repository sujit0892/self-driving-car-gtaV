import numpy as np
from PIL import ImageGrab
import cv2
import time
import pyautogui
from directInput import ReleaseKey, PressKey, W, S, A,D


def draw_lines(img, lines):
     try:
         for line in lines:
             cord = line[0]
             cv2.line(img, (cord[0], cord[1]), (cord[2], cord[3]), [255, 255, 255], 3)
     except:
         pass

         
def roi(img,vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img,mask)
    return masked
    
    
def process_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    process_img = cv2.Canny(gray, threshold1 = 200, threshold2=300)
    process_img = cv2.GaussianBlur(process_img, (5,5), 0)
    vertices = np.array([[0, 320], [0, 160], [160, 0], [480,0], [640, 160], [640, 320]], np.int32)
    process_img = roi(process_img, [vertices])
    lines = cv2.HoughLinesP(process_img, 1, np.pi/180, 180, np.array([]), 130, 2)
    draw_lines(process_img, lines)
    return process_img

def main():
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    last_time = time.time()
    while True:
        screen = np.array(ImageGrab.grab(bbox=(0,40,640,480)))
        image = process_img(screen) 
        print('loop took {} seconds'.format(time.time() - last_time))
        last_time = time.time()
        cv2.imshow('window', image)
        #cv2.imshow('window', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main()
    
