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

def main(): #Função principal que gere o loop de lógica do programa
    global json_data
    
    # Inicializar a captura de vídeo
    cap = cv2.VideoCapture(0)
    
    # Variáveis de controle
    walking_to_toy = False
    back_from_toy = False
    backflip = False
    can_walk = False
    walking_to_food = False
    detect_object = False
    detect_head = False
    rotate = False
    side = None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Erro ao acessar a câmera.")
            break

        # Inverter e processar frame para MediaPipe
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Deteção de mãos com MediaPipe
        hand_results = hands.process(rgb_frame)

        # Desenhar landmarks das mãos
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
        dedos = contar_dedos(hand_results) # Contar dedos levantados
        if dedos is not None:
            cv2.putText(frame, f"Dedos levantados: {dedos}", (10, 30),  # Ajuste na posição vertical
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)  # Redução de escala e espessura
        cv2.putText(frame, f"Pode andar: {can_walk}", (10, 60),  # Proximidade ajustada
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)  # Redução de escala e espessura
           
        if can_walk: # Lógica baseada nos dedos levantados e detecção de cabeça
            if dedos == 1 and not back_from_toy and not backflip and not walking_to_food:
                walking_to_toy = True
            elif dedos == 3 and not walking_to_toy and not backflip and not back_from_toy:
                walking_to_food = True
            elif dedos == 5 and not walking_to_toy and not backflip and not walking_to_food:
                back_from_toy = True
            elif detect_head:
                face_results = face_mesh.process(rgb_frame)
                nose_x,nose_y = detectar_cabeca(face_results)
                if nose_x and nose_x >= 0.7:
                    rotate = True
                elif nose_y and nose_y <= 0.47:
                    backflip = True
                    
            for i in range(len(json_data)): # Atualizar estado do "json_data" com base nas interações
                if json_data[i]["name"] == "Dog":
                    if walking_to_toy:
                        if json_data[i]["rotation"] == [0, 0, -135]:
                            if json_data[i]["location"][1] < 85:
                                json_data[i]["location"][0] -= 1
                                json_data[i]["location"][1] += 1
                            else:
                                pygame.mixer.music.load('C:/Users/admin/Desktop/Computacao Visual/TF_a79299_a71433/Sounds/dog-toy-sound.mp3')
                                pygame.mixer.music.play()
                                walking_to_toy = False
                                back_from_toy = False
                                walking_to_food = False
                                backflip = False
                                rotate = False
                        else:
                            json_data[i]["rotation"] = [0, 0, -135]
                    elif walking_to_food:
                        if json_data[i]["rotation"] == [0, 0, -230]:
                            if json_data[i]["location"][1] < 57:
                                json_data[i]["location"][0] += 1
                                json_data[i]["location"][1] += 1
                            else:
                                pygame.mixer.music.load('C:/Users/admin/Desktop/Computacao Visual/TF_a79299_a71433/Sounds/dog-eating-sound.mp3')
                                pygame.mixer.music.play()
                                walking_to_toy = False
                                back_from_toy = False
                                walking_to_food = False
                                backflip = False
                        else:
                            json_data[i]["rotation"] = [0, 0, -230]
                    elif backflip:
                        if json_data[i]["rotation"][0] - 5 >= -360:
                            json_data[i]["rotation"][0] = (json_data[i]["rotation"][0] - 5)
                            if json_data[i]["rotation"][0] >= -180:
                                pygame.mixer.music.load('C:/Users/admin/Desktop/Computacao Visual/TF_a79299_a71433/Sounds/dog-backflip-sound.mp3')
                                pygame.mixer.music.play()
                                json_data[i]["location"][2] = (json_data[i]["location"][2] + 1.5)
                            else:
                                json_data[i]["location"][2] = (json_data[i]["location"][2] - 1.5)
                        elif json_data[i]["rotation"][0] == -360:
                            json_data[i]["rotation"][0] = 0
                            walking_to_toy = False
                            back_from_toy = False
                            walking_to_food = False
                            backflip = False
                            rotate = False
                    elif rotate:
                        if json_data[i]["rotation"][2] - 5 >= -360:
                            json_data[i]["rotation"][2] = (json_data[i]["rotation"][2] - 5)
                        elif json_data[i]["rotation"][2] == -360:
                            json_data[i]["rotation"][2] = 0
                            pygame.mixer.music.load('C:/Users/admin/Desktop/Computacao Visual/TF_a79299_a71433/Sounds/dog-happy-sound.mp3')
                            pygame.mixer.music.play()
                            walking_to_toy = False
                            back_from_toy = False
                            walking_to_food = False
                            backflip = False
                            rotate = False
                    elif back_from_toy:
                        if json_data[i]["location"] == [-85,85,0]:
                            side = "Toy"
                        elif json_data[i]["location"] == [57,57,0]:
                            side = "bowl"
                        if side == "Toy":
                            if json_data[i]["rotation"] == [0, 0, 45]:
                                if json_data[i]["location"][1] > 0:
                                    json_data[i]["location"][0] += 1
                                    json_data[i]["location"][1] -= 1
                                else:
                                    walking_to_toy = False
                                    back_from_toy = False
                                    walking_to_food = False
                                    backflip = False
                                    rotate = False
                                    json_data[i]["rotation"] = [0, 0, 0]
                                    side = None
                            else:
                                json_data[i]["rotation"] = [0, 0, 45]
                        elif side == "bowl":
                            if json_data[i]["rotation"] == [0, 0, -45]:
                                if json_data[i]["location"][1] > 0:
                                    json_data[i]["location"][0] -= 1
                                    json_data[i]["location"][1] -= 1
                                else:
                                    walking_to_toy = False
                                    back_from_toy = False
                                    walking_to_food = False
                                    backflip = False
                                    rotate = False
                                    json_data[i]["rotation"] = [0, 0, 0]
                                    side = None
                            else:
                                json_data[i]["rotation"] = [0, 0, -45]

        # Deteção de objetos com YOLO
        if detect_object:
            results = model(frame, stream=False)
            for result in results:
                boxes = result.boxes  # Obter as bounding boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = model.names[cls]

                    # Verificar objetos de interesse
                    if label in ["teddy bear", "cup", "bottle", "cell phone"]:
                        # Desenhar bounding box ao redor do objeto
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"{label} ({conf:.2f})", (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                        # Atualizar json_data com base no objeto detectado
                        detected_objects = []

                        for obj in json_data:
                            detected_objects.append(obj['name'])
                        if "Dog" not in detected_objects and label == "teddy bear":
                            json_data.append({'name': 'Dog', 'model': "C:/Users/admin/Desktop/Computacao Visual/TF_a79299_a71433/Objects/dog/Dog.obj", "location": [0, 0, 0], "rotation": [0,0,0], "scale": [1,1,1]})
                        elif "Bowl" not in detected_objects and label == "cup":
                            json_data.append({'name': 'Bowl', 'model': "C:/Users/admin/Desktop/Computacao Visual/TF_a79299_a71433/Objects/bowl.obj", "location": [70, 70, 2], "rotation": [90,0,0],"scale": [0.023,0.023,0.023]})
                        elif "Toy" not in detected_objects and label == "bottle":
                            json_data.append({'name': 'Toy', 'model': "C:/Users/admin/Desktop/Computacao Visual/TF_a79299_a71433/Objects/toy.obj", "location": [-104, 99, 2.5], "rotation": [0,0,45],"scale": [0.5,0.5,0.5]})
                        elif "CellPhone" not in detected_objects and  label == "cell phone":
                            json_data.append({'name': 'Tree', 'model': "C:/Users/admin/Desktop/Computacao Visual/TF_a79299_a71433/Objects/tree/Tree.obj", "location": [-105, -114, 0], "rotation": [90,0,0], "scale" : [14,14,14]})

        # Exibir frame
        cv2.imshow("Detecção de Objetos, Gestos e Cabeça", frame)

        # Sair com 'q'
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == ord('s'):
            can_walk = not can_walk
        if key == ord('z'):
            detect_object = not detect_object
        if key == ord('x'):
            detect_head = not detect_head
    cap.release()
    cv2.destroyAllWindows()


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