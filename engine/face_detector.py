import cv2

def detect_face(image_path):
    img = cv2.imread(image_path)
    return img is not None
