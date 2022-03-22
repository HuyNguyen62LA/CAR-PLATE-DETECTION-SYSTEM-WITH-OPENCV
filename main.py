import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

frameWidth = 640
frameHeight = 480
nPlateCascade = cv2.CascadeClassifier("Resources\haarcascade_russian_plate_number.xml")
minArea = 100
color = (255, 0, 255)
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)
count = 0
while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 10) #xac dinh bang so tu file xml
    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img)
            imgRoi = cv2.resize(imgRoi, dim, interpolation=cv2.INTER_AREA) #resize lai anh

            cv2.imshow("ROI", imgRoi)

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('r'):
        cv2.imwrite("Resources/Scanned/NoPlate_" + str(count) + ".jpg", imgRoi)
        # Xu ly anh bang so giup de , (x, y), (x + w, y + h), (0, 0, 255), 5) #ve hinh chu nhat
        #             cv2.putText(img, "BIEN SO", (x, y - 5),
        #                         cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
        #             imgRoi = img[y + 15:y + h - 10, x + 15:x + w - 20] #cat hinh bang so, bo hinh chu nhat cho khop voi bang so
        #             width = int(imgRoi.shape[1] * 150 / 100)
        #             height = int(imgRoi.shape[0] * 150 / 100)
        #             dim = (width, heightchuyen sang text hon
        carplate_extract_img_gray = cv2.cvtColor(imgRoi, cv2.COLOR_RGB2GRAY) #chuyen hinh sang mau gray
        carplate_extract_img_gray_blur = cv2.medianBlur(carplate_extract_img_gray, 3)  # lam blur anh
        text = pytesseract.image_to_string(carplate_extract_img_gray_blur,
            config=f'--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.')
        print("So xe:", text)
        cv2.imshow("Result", img)
        cv2.waitKey()
        count += 1

