import cv2
import os
from HandTracker import HandDetector
from dottedline import drawrect, drawline
import numpy as np

# Variables
width, height = 1280, 720
frames_folder = "Images"
slide_num = 0
hs, ws = int(120 * 1.2), int(213 * 1.2)
ge_thresh_y = 400
ge_thresh_x = 750
gest_done = False
gest_counter = 0
delay = 15
annotations = [[]]
annot_num = 0
annot_start = False
zoom_factor = 1.0
zoom_increment = 0.1
zoom_center = (width // 2, height // 2)
last_pointer_pos = None  # Store the last pointer position

# Get list of presentation images
path_imgs = sorted(os.listdir(frames_folder), key=len)
print(path_imgs)

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# HandDetector
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # Get image frame
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    pathFullImage = os.path.join(frames_folder, path_imgs[slide_num])
    slide_current = cv2.imread(pathFullImage)
    slide_current = cv2.resize(slide_current, (width, height))

    # Find the hand and its landmarks
    hands, frame = detector.findHands(frame)

    # Draw Gesture Threshold line
    drawrect(frame, (width, 0), (ge_thresh_x, ge_thresh_y), (0, 255, 0), 5, 'dotted')

    if hands and not gest_done:  # If hand is detected
        hand = hands[0]
        cx, cy = hand["center"]
        lm_list = hand["lmList"]  # List of 21 Landmark points
        fingers = detector.fingersUp(hand)

        # Map hand landmarks to full screen coordinates
        x_val = int(np.interp(lm_list[8][0], [0, width], [0, width]))  # Full screen width
        y_val = int(np.interp(lm_list[8][1], [0, height], [0, height]))  # Full screen height
        pointer_pos = x_val, y_val
        last_pointer_pos = pointer_pos  # Update the last pointer position

        if cy < ge_thresh_y and cx > ge_thresh_x:
            annot_start = False

            # gest_1 (previous)
            if fingers == [1, 0, 0, 0, 0]:
                annot_start = False
                if slide_num > 0:
                    gest_done = True
                    slide_num -= 1
                    annotations = [[]]
                    annot_num = 0

            # gest_2 (next)
            if fingers == [0, 0, 0, 0, 1]:
                annot_start = False
                if slide_num < len(path_imgs) - 1:
                    gest_done = True
                    slide_num += 1
                    annotations = [[]]
                    annot_num = 0

            # gest_3 (clear screen)
            if fingers == [1, 1, 1, 1, 1]:
                if annotations:
                    annot_start = False
                    if annot_num >= 0:
                        annotations.clear()
                        annot_num = 0
                        gest_done = True
                        annotations = [[]]

        # gest_4 (show pointer)
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(slide_current, pointer_pos, 4, (0, 0, 255), cv2.FILLED)
            annot_start = False

        # gest_5 (draw)
        if fingers == [0, 1, 0, 0, 0]:
            if not annot_start:
                annot_start = True
                annot_num += 1
                annotations.append([])
            annotations[annot_num].append(pointer_pos)
            cv2.circle(slide_current, pointer_pos, 4, (0, 0, 255), cv2.FILLED)

        else:
            annot_start = False

        # gest_6 (erase)
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annot_start = False
                if annot_num >= 0:
                    annotations.pop(-1)
                    annot_num -= 1
                    gest_done = True

        # Zoom-In (4 fingers up)
        if fingers == [0, 1, 1, 1, 1]:
            if last_pointer_pos:  # Use the last pointer position as the zoom center
                zoom_center = last_pointer_pos
                zoom_factor += zoom_increment
                gest_done = True

        # Zoom-Out (5 fingers up)
        if fingers == [1, 1, 1, 1, 1]:
            zoom_factor = 1.0
            gest_done = True

    else:
        annot_start = False

    # Gesture Performed Iterations:
    if gest_done:
        gest_counter += 1
        if gest_counter > delay:
            gest_counter = 0
            gest_done = False

    # Apply zoom
    if zoom_factor != 1.0:
        h, w = slide_current.shape[:2]
        zoom_width = int(w / zoom_factor)
        zoom_height = int(h / zoom_factor)
        x1 = max(0, zoom_center[0] - zoom_width // 2)
        y1 = max(0, zoom_center[1] - zoom_height // 2)
        x2 = min(w, zoom_center[0] + zoom_width // 2)
        y2 = min(h, zoom_center[1] + zoom_height // 2)
        zoomed_slide = slide_current[y1:y2, x1:x2]
        slide_current = cv2.resize(zoomed_slide, (w, h))

    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(slide_current, annotation[j - 1], annotation[j], (0, 0, 255), 6)

    # Adding cam img on slides
    img_small = cv2.resize(frame, (ws, hs))
    h, w, _ = slide_current.shape
    slide_current[h-hs:h, w-ws:w] = img_small

    # Maximize the screen
    cv2.namedWindow("Slides", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Slides", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow("Slides", slide_current)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()