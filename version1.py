import cv2
from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(maxHands=1, detectionCon=0.8)

cap = cv2.VideoCapture(0)
prev_wrist_x = 0  
def is_ok_gesture(lmList):
    try:
        thumb_tip = lmList[4]
        index_tip = lmList[8]
        middle_tip = lmList[12][1]
        ring_tip = lmList[16][1]
        pinky_tip = lmList[20][1]

        middle_pip = lmList[10][1]
        ring_pip = lmList[14][1]
        pinky_pip = lmList[18][1]

        distance = ((thumb_tip[0] - index_tip[0]) ** 2 + (thumb_tip[1] - index_tip[1]) ** 2) ** 0.5

        return (
            distance < 30
            and middle_tip < middle_pip
            and ring_tip < ring_pip
            and pinky_tip < pinky_pip
        )
    except:
        return False

def is_hello_gesture(lmList):
    try:
        wrist = lmList[0][1]
        return all(lmList[tip][1] < wrist for tip in [8, 12, 16, 20])
    except:
        return False

def is_thankyou_gesture(lmList):
    try:
        thumb_tip = lmList[4]
        index_tip = lmList[8]
        wrist = lmList[0]
        return (
            abs(thumb_tip[1] - wrist[1]) < 50 and
            abs(index_tip[1] - wrist[1]) < 50
        )
    except:
        return False

def is_yes_gesture(lmList):
    try:
        thumb_tip = lmList[4]
        index_tip = lmList[8]
        return thumb_tip[1] < index_tip[1]
    except:
        return False

def is_no_gesture(lmList, prev_wrist_x):
    try:
        wrist = lmList[0]
        return abs(wrist[0] - prev_wrist_x) > 50
    except:
        return False
def is_iloveyou_gesture(lmList):
    try:
        thumb_tip = lmList[4]
        index_tip = lmList[8]
        middle_tip = lmList[12]
        ring_tip = lmList[16]
        pinky_tip = lmList[20]

        return (
            thumb_tip[1] < lmList[3][1] and  # Thumb extended
            index_tip[1] < lmList[7][1] and  # Index finger extended
            middle_tip[1] > lmList[10][1] and  # Middle finger folded
            ring_tip[1] > lmList[14][1] and  # Ring finger folded
            pinky_tip[1] < lmList[19][1]  # Pinky finger extended
        )
    except:
        return False
    

def is_please_gesture(lmList):
    try:
        return all([
            lmList[8][1] < lmList[6][1],
            lmList[12][1] < lmList[10][1],
            lmList[16][1] < lmList[14][1],
            lmList[20][1] < lmList[18][1]
        ])
    except:
        return False

def is_stop_gesture(lmList):
    try:
        wrist = lmList[0]
        return all(lmList[tip][1] < wrist[1] for tip in [8, 12, 16, 20])  
    except:
        return False

def is_like_gesture(lmList):
    try:
        thumb_tip = lmList[4]
        thumb_mcp = lmList[2]
        other_fingers = [lmList[8][1], lmList[12][1], lmList[16][1], lmList[20][1]]

        return (
            thumb_tip[1] < thumb_mcp[1]  
            and all(finger > lmList[0][1] for finger in other_fingers)  
        )
    except:
        return False

def is_dislike_gesture(lmList):
    try:
        thumb_tip = lmList[4]
        thumb_mcp = lmList[2]
        other_fingers = [lmList[8][1], lmList[12][1], lmList[16][1], lmList[20][1]]

        return (
            thumb_tip[1] > thumb_mcp[1]  
            and all(finger > lmList[0][1] for finger in other_fingers) 
        )
    except:
        return False

def is_peace_gesture(lmList):
    try:
        index_tip = lmList[8]
        middle_tip = lmList[12]
        ring_tip = lmList[16]
        pinky_tip = lmList[20]

        return (
            index_tip[1] < lmList[6][1] and
            middle_tip[1] < lmList[10][1] and
            ring_tip[1] > lmList[14][1] and
            pinky_tip[1] > lmList[18][1]
        )  
    except:
        return False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    hands, frame = detector.findHands(frame)
    
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        bbox = hand['bbox']
        
        if bbox and isinstance(bbox, (list, tuple)) and len(bbox) == 4:
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        if lmList and isinstance(lmList, list):
            if is_ok_gesture(lmList):
                cv2.putText(frame, "OK", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif is_hello_gesture(lmList):
                cv2.putText(frame, "Hello", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif is_thankyou_gesture(lmList):
                cv2.putText(frame, "Thank You", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            elif is_yes_gesture(lmList):
                cv2.putText(frame, "Yes", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)#
            elif is_no_gesture(lmList, prev_wrist_x):
                cv2.putText(frame, "No", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif is_stop_gesture(lmList):
                cv2.putText(frame, "Stop", (50, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif is_like_gesture(lmList):
                cv2.putText(frame, "Like", (50, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif is_dislike_gesture(lmList):
                cv2.putText(frame, "Dislike", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225), 2)#
            elif is_peace_gesture(lmList):
                cv2.putText(frame, "Peace", (50, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            elif is_iloveyou_gesture(lmList):
                cv2.putText(frame, "I LOVE YOU", (50, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            prev_wrist_x = lmList[0][0]

    cv2.imshow("Sign Language Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()