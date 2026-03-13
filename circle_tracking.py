import cv2
import numpy as np
import serial
import time

#  STM'e bağlan (Windows: "COMx", Linux: "/dev/ttyUSBx")
ser = serial.Serial('COM11', 9600, timeout=1)

#  Kamerayı başlat
cap = cv2.VideoCapture(0)

#  Lazer kameradan 3 cm aşağıda
y_offset_cm = 3  

#  PID Parametreleri (Oransal kontrol)
Kp = 2.0  # Hata büyüdükçe hızı artıran katsayı
min_speed = 0  # Minimum hız
max_speed = 200  # Maksimum hız

#  Haritalama fonksiyonu (map_range)
def map_range(value, in_min, in_max, out_min, out_max):
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)

#  Step motor komutlarını STM'e gönder
def ters_orantix(speed_x, x_min=0, x_max=200, xo_min=400, xo_max=800):
    return xo_max - ((speed_x - x_min) / (x_max - x_min)) * (xo_max - xo_min)

def ters_orantiy(speed_y, y_min=0, y_max=200, yo_min=400, yo_max=800):
    return yo_max - ((speed_y - y_min) / (y_max - y_min)) * (yo_max - yo_min)

def send_coordinates(x_dir, speed_x, y_dir, speed_y):
    
    # Eğer mavi eksene göre hata çok küçükse enable=1 olsun
    orjin_tolerans_x = 10  # X ekseni için tolerans
    orjin_tolerans_y = 10  # Y ekseni için tolerans

    if abs(relative_x) < orjin_tolerans_x:
        enablex = 1
    else:
        enablex = 0

    if abs(relative_y) < orjin_tolerans_y:
        enabley = 1
    else:
        enabley = 0

   
    xo = ters_orantix(speed_x)
    yo = ters_orantiy(speed_y)
    message = f"({x_dir},{int(xo)},{enablex},{y_dir},{int(yo)},{enabley})\n"
    ser.write(message.encode())  
    print(message)
    
def empty(a):
    pass

# Trackbar Penceresi
cv2.namedWindow("Parameters")
cv2.createTrackbar("Threshold1", "Parameters", 100, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 200, 255, empty)
cv2.createTrackbar("Min Radius", "Parameters", 10, 100, empty)
cv2.createTrackbar("Max Radius", "Parameters", 50, 200, empty)

while cap.isOpened():
    ret, frame = cap.read()
    
    #  Gerçek zamanlı çözünürlüğü al (her karede güncellenir)
    frameHeight, frameWidth = frame.shape[:2]
    
    if not ret:
        print("Kamera görüntüsü alınamadı!")
        break

    #  Ekran merkezi (Yeşil eksen = lazerin merkezi)
    center_x, center_y = frameWidth // 2, frameHeight // 2  

    #  Mavi ekseni hesapla (kamera 3 cm yukarıda)
    pixel_per_cm = frameHeight / 24  
    y_offset_pixels = int(y_offset_cm * pixel_per_cm)
    camera_center_y = center_y - y_offset_pixels  

    #  Görüntüyü işleme
    imgBlur = cv2.GaussianBlur(frame, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    # Trackbar'dan değerleri oku
    t1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    t2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    minRadius = cv2.getTrackbarPos("Min Radius", "Parameters")
    maxRadius = cv2.getTrackbarPos("Max Radius", "Parameters")

    #  Kenar Algılama
    imgCanny = cv2.Canny(imgGray, t1, t2)

    #  Daireleri tespit et
    circles = cv2.HoughCircles(imgGray, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=100, param2=30,
                               minRadius=minRadius, maxRadius=maxRadius)

    detected_circles = []

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            cx, cy, radius = map(int, circle)  
            detected_circles.append((cx, cy, radius))

    #  Eğer birden fazla daire varsa, en büyük olanı seç
    if len(detected_circles) > 0:
        detected_circles.sort(key=lambda x: (-x[2], x[0]))  
        best_circle = detected_circles[0]  
        cx, cy, radius = best_circle

        # print(f"Daire Merkezi (cx, cy): ({cx}, {cy})")
        # print(f"Ekran Merkezi (center_x, center_y): ({center_x}, {center_y})")

        #  Dairenin dışına mor çember çiz
        cv2.circle(frame, (cx, cy), radius, (255, 0, 255), 2)

        #  Dairenin merkezine kırmızı nokta koy
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        #  Mavi nokta = Dairenin üst kenarı
        mavi_x = cx  
        mavi_y = cy - radius  

        #  Mavi noktayı çiz
        cv2.circle(frame, (mavi_x, mavi_y), 5, (255, 0, 0), -1)  

        #  Mavi eksene (kamera merkezi) göre koordinatlar
        relative_x = int(mavi_x - center_x)  
        relative_y = int(camera_center_y - mavi_y)  # Kamera eksenine göre hesapla

        #  X ve Y ekseninde yön belirleme
        x_dir = 1 if mavi_x > center_x else 0  # Sağdaysa 1, soldaysa 0
        y_dir = 1 if mavi_y < camera_center_y else 0  # Yukarıdaysa 1, aşağıdaysa 0


        #  Orjin bölgesi büyütme (Hassasiyet Aralığı)
        orjin_tolerans_x = 500  # X ekseni toleransı
        orjin_tolerans_y = 800  # Y ekseni toleransı (Daha hassas yapabiliriz!)
        # Orjin alanını büyütmek için

        #  Hata hesaplaması (Orjinden uzaklık)
        error_x = abs(relative_x)
        error_y = abs(relative_y)

        #  Eğer hata çok küçükse motoru durdur
        if error_x < orjin_tolerans_x:
            speed_x = 0
        else:
            speed_x = Kp * error_x

        if error_y < orjin_tolerans_y:
            speed_y = 0
        else:
            speed_y = Kp * error_y

        #  Hız sınırlarını uygula
        speed_x = max(min(speed_x, max_speed), min_speed)
        speed_y = max(min(speed_y, max_speed), min_speed)


        #  PID ile hız hesaplama (Sadece Kp kullanılıyor)
        speed_x = Kp * error_x
        speed_y = Kp * error_y

        #  Hız sınırlarını uygula
        speed_x = max(min(speed_x, max_speed), min_speed)
        speed_y = max(min(speed_y, max_speed), min_speed)

        # print(f"Step Motor X Hızı: {speed_x} (Yön: {x_dir})")
        # print(f"Step Motor Y Hızı: {speed_y} (Yön: {y_dir})")

        #  Step motor hızlarını ve yönlerini STM'e gönder
        send_coordinates(x_dir, speed_x, y_dir, speed_y)

        #  Mavi noktaya göre koordinatlar
        cv2.putText(frame, f"Mavi Nokta: ({relative_x}, {relative_y})", (mavi_x + 10, mavi_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    #  Yeşil ekseni çiz (Lazerin merkezi)
    cv2.line(frame, (center_x, 0), (center_x, frameHeight), (0, 255, 0), 2)  
    cv2.line(frame, (0, center_y), (frameWidth, center_y), (0, 255, 0), 2)  

    #  Mavi ekseni çiz (Kamera merkezi)
    cv2.line(frame, (0, camera_center_y), (frameWidth, camera_center_y), (255, 0, 0), 2)  

    #  Görüntüyü göster
    cv2.imshow("Original Image", frame)
    cv2.imshow("Canny Edges", imgCanny)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
