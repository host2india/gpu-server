import torch
import cv2
import numpy as np

class FaceDetector:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def detect(self, frame):
        h, w, _ = frame.shape
        return [0, 0, w, h]
