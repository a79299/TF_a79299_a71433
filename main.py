import socket
import json
import threading
import numpy as np
import mediapipe as mp
import cv2
import logging
from ultralytics import YOLO
import pygame

# Inicializar o mixer de som do Pygame
pygame.mixer.init()

json_data = []

# configuração e carregamento do modelo YOLO11 para detecção de objetos
logging.getLogger("ultralytics").setLevel(logging.ERROR)
model = YOLO("models/yolo11s.pt")

# Configurar MediaPipe para detecção de mãos
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Configurar MediaPipe para detecção de cara
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.7, min_tracking_confidence=0.7)