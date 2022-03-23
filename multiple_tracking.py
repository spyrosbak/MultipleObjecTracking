from __future__ import print_function
import sys
import cv2
from random import randint
import time

trackerTypes = ['KCF', 'MOSSE', 'CSRT']

f = open("Results.txt", "a+")

def createTrackerByName(trackerType):
    # Create a tracker based on tracker name
    if trackerType == trackerTypes[1]:
        tracker = cv2.TrackerKCF_create()
    elif trackerType == trackerTypes[2]:
        tracker = cv2.TrackerMOSSE_create()
    elif trackerType == trackerTypes[3]:
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in trackerTypes:
            print(t)
    return tracker

# Set video to load
videoPath = "Law-Abiding Family of Swans Cross Road at Pedestrian Crossing.mp4"

# Create a video capture object to read videos
cap = cv2.VideoCapture(videoPath)

success, frame = cap.read()
if not success:
  print('Failed to read video')
  sys.exit(1)

# Locate Objects in the First Frame
bboxes = []
colors = []

while True:
  cv2.namedWindow('MultiTracker', cv2.WINDOW_NORMAL)
  bbox = cv2.selectROI('MultiTracker', frame)
  bboxes.append(bbox)
  colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
  print("Press q to quit selecting boxes and start tracking")
  print("Press any other key to select next object")
  k = cv2.waitKey(0) & 0xFF
  if (k == 113):  # q is pressed
    break

print('Selected bounding boxes {}'.format(bboxes))

# Specify the tracker type
trackerType = "CSRT"
#trackerType ='KCF'
#trackerType = 'MOSSE'

# Create MultiTracker object
multiTracker = cv2.MultiTracker_create()

# Initialize MultiTracker
for bbox in bboxes:
  multiTracker.add(createTrackerByName(trackerType), frame, bbox)

# Process video and track objects
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    success, boxes = multiTracker.update(frame)
    for i, newbox in enumerate(boxes):
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

    # show frame
    cv2.imshow('MultiTracker', frame)

    # quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
        break
    t = time.time()
    tmpRunTime = time.time() - t
    Centroid = (int(newbox[0]) + (int(newbox[0]) + int(newbox[2])) / 2, (int(newbox[1]) + (int(newbox[1]) + int(newbox[3])) / 2))
    f.write("Technic Name: CSRT | Frame Number: 1 | Processing Time: {:.8f}".format(tmpRunTime) + "| Centroid: {}\n".format(Centroid) )

cap.release()
cv2.destroyAllWindows()