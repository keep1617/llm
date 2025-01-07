from fer import FER
import cv2
import pprint


img = cv2.imread("seol.jpg")
detector = FER()
result = detector.detect_emotions(img)
pprint.pprint(result)