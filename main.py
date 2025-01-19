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

def contar_dedos(results): # Função para contar o número de dedos levantados com base nos landmarks detectados por MediaPipe.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            dedos_levantados = 0

            # Coordenada Y do punho para referência
            punho_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

            # Verificar se o polegar está levantado
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

            # Determinar se o polegar está levantado (com base na posição X do polegar em relação ao punho)
            if thumb_tip.x < thumb_ip.x if hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x > 0.5 else thumb_tip.x > thumb_ip.x:
                dedos_levantados += 1
            
            # Verificar os outros dedos (indicador, médio, anelar e mínimo) estão levantados
            dedos = [
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP,
            ]
            articulacoes = [
                mp_hands.HandLandmark.INDEX_FINGER_MCP,
                mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                mp_hands.HandLandmark.RING_FINGER_MCP,
                mp_hands.HandLandmark.PINKY_MCP,
            ]
            for i in range(len(dedos)):
                if hand_landmarks.landmark[dedos[i]].y < hand_landmarks.landmark[articulacoes[i]].y:
                    dedos_levantados += 1
            return dedos_levantados
    return 0

def detectar_cabeca(results): # Função para detectar a posição do nariz com base nos pontos faciais usando o MediaPipe FaceMesh.
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks: # Pegar a coordenada Y do nariz (índice 1 é o ponto da ponta do nariz)
            nose_y = face_landmarks.landmark[1].y
            nose_x = face_landmarks.landmark[1].x
            return nose_x, nose_y
    return None,None



















def start_server(): #Inicializa um servidor para gerir conexões de clientes e dados compartilhados via JSON
    global json_data
    host = "127.0.0.1"
    port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Servidor ouvindo em {host}:{port}...")

    def handle_client(conn, addr): #Gere a comunicação com um cliente conectado
        print(f"Conexão estabelecida com {addr}")
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"Conexão encerrada por {addr}")
                    break
                message = json.loads(data.decode("utf-8"))
                if message["action"] == "get":
                    conn.sendall(json.dumps(json_data).encode("utf-8"))
            except Exception as e:
                print(f"Erro com o cliente {addr}: {e}")
                break
        try:
            conn.close()
        except OSError:
            print(f"Erro ao tentar fechar a conexão com {addr}")

    def accept_connections(): #Aceita conexões de clientes de forma contínua
        while True:
            try:
                conn, addr = server_socket.accept()
                threading.Thread(
                    target=handle_client, args=(conn, addr), daemon=True
                ).start()
            except OSError:
                print("Erro ao aceitar novas conexões")
                break
    threading.Thread(target=accept_connections, daemon=True).start()
    main()
    print("Servidor desligado!")

if __name__ == "__main__":
    start_server()