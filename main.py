import cv2
import numpy as np

net = cv2.dnn.readNet("dnn_model-220107-114215/dnn_model/yolov4-tiny.weights","dnn_model-220107-114215/dnn_model/yolov4-tiny.cfg")
model =cv2.dnn_DetectionModel(net)
model.setInputParams(size=(320,320),scale=1/255)
#load classes list

classes=[]
with open ("dnn_model-220107-114215/dnn_model/classes.txt","r") as file_object:
    for class_name in file_object.readlines():
        class_name = class_name.strip()
        classes.append(class_name)

print(classes)

cap =cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

button_person= False

def click_button(event,x,y,flags,params):
    global button_person
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        polygon = np.array([[(20, 20), (220, 20), (220, 70), (20, 70)]])
        is_inside = cv2.pointPolygonTest(polygon,(x,y),False)
        if is_inside > 0:
            print("we rae clicking button",x,y)

            if button_person is False:
                button_person = True
            else:
                button_person = False
            print("now button person is : ",button_person)

#create window
cv2.namedWindow('frame')
cv2.setMouseCallback("frame",click_button)


while True:
    ret,frame =cap.read()
    #object detcetion
    (class_ids,score,bboxes) = model.detect(frame)
    for class_id,score,bbox in zip(class_ids,score,bboxes):
        (x,y,w,h)=bbox
        class_name= classes[class_id]
        #print(x,y,w,h)
        if class_name == "person" and button_person is True:
            cv2.putText(frame,class_name,(x,y-5),cv2.FONT_HERSHEY_PLAIN,1,(200,0,50),2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,50),2)

    #cv2.rectangle(frame,(20,20),(80,80),(0,0,150),-1)
    polygon = np.array([[(20,20),(220,20),(220,70),(20,70)]])
    cv2.fillPoly(frame,polygon,(0,0,200))
    cv2.putText(frame,"Person",(30,60),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)




    cv2.imshow("frame",frame)
    key = cv2.waitKey(1)
    if key ==27:
        break
cap.release()
cv2.destroyAllWindows()