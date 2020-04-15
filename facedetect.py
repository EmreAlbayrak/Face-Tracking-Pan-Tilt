import cv2
import serial

screen_width = 1920
screen_height = 1080

ser: object = serial.Serial('COM3', baudrate = 9600, timeout=0)

#BOUNDARY SHAPE DRAWER
def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):

    #converting images to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #importing face detection features for classification
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)

    #creating array for storing shape objects
    coords = []

    #initiating loop for drawing shapes for each image parameter at a time
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x,y), (x+w,y+h), color, 2)
        cv2.putText(img, text, (x, y-4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        coords = [x, y, w, h]

    #returning drawed shapes for each image parameter at a time
    return coords

#SETTING PARAMETERS FOR CLASSIFICATION
def detect(img, faceCascade):

    #creating color object
    color = {"blue": (255,0,0), "white":(255,255,255),"red":(0,0,255), "green":(0,255,0)}

    #drawing boundary for array elements and changing captured images with added shapes
    coords = draw_boundary(img, faceCascade, 1.1, 10, color['white'], "TARGET")

    #runing code below if coords array is succesfully impelented for 4 elements
    if len(coords) == 4:
        img[coords[1]:coords[1]+coords[3], coords[0]:coords[0]+coords[2]]

        circleThickness = 2

        face_center_x = coords[0] + (coords[2]//2)
        face_center_y = coords[1] + (coords[3]//2)
        cv2.circle(img, ((face_center_x), (face_center_y)), 2, color['red'], circleThickness)
        if (width // 2) > face_center_x + 20:
            print('x-')
            ser.write(b'1')
        elif (width // 2) < face_center_x - 20:
            print('x+')
            ser.write(b'2')
        elif face_center_x - 20 <= width // 2 <= face_center_x + 20:
            print('x0')
            if (height // 2) > face_center_y + 20:
                print('y+')
                ser.write(b'3')
            elif (height // 2) < face_center_y - 20:
                print('y-')
                ser.write(b'4')
            elif face_center_y - 20 <= height // 2 <= face_center_y + 20:
                print('y0')
                ser.write(b'5')
    else:
        ser.write(b'5')
    #returning resulting images
    return img

#CREATING SEGMENTATION OBJECTS FOR CLASSIFICATION USING PRECALCULATED MODELS
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#CREATING CAMERA OBJECT AND INITIATING CAMERA
video_capture = cv2.VideoCapture(1) #Change the number inside of VideoCapture() to change the camera
video_capture.set(cv2.CV_CAP_PROP_FPS, 20)

cv2.namedWindow('My Window',cv2.WINDOW_KEEPRATIO)
cv2.setWindowProperty('My Window',cv2.WND_PROP_ASPECT_RATIO,cv2.WINDOW_KEEPRATIO)
cv2.setWindowProperty('My Window',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

#PRINTING ERROR IF CAMERA OBJECT CREATION IS FAILED
if not video_capture.isOpened():
    print("Cannot open camera")
    exit()

video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

#STARTING INFINITE LOOP FOR SYSTEM
while True:

    # reading camera object as an image stream
    ret, img = video_capture.read()

    #if frame is read correctly ret is True (ret is video stream object)
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        #exit from infinite loop if camera stream capture failed
        break

    #segmentation of parts using precalculated models
    img = detect(img, faceCascade)

    height, width, channels = img.shape

    lineThickness = 1
    cv2.line(img, (0, height//2), (width, height//2), (0, 255, 0), lineThickness)
    cv2.line(img, (width//2, 0), (width//2, height), (0, 255, 0), lineThickness)

    #showing segmented image on screen continuously (real-life)
    cv2.imshow("My Window", img)

    #waiting for Q button press, if Q is pressed break the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

ser.write(b'5')

#DESTROYING CAMERA OBJECT FOR CLEARING MEMORY
video_capture.release()

#DESTROYING IMAGE WINDOWS FOR CLEARING MEMORY
cv2.destroyAllWindows()