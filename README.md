# Projeto: Detecção de Gestos, Objetos e Cabeça com YOLO, MediaPipe e OpenCV

Este projeto implementa um sistema interativo que utiliza visão computacional para detecção de gestos, objetos e posição da cabeça. A funcionalidade é complementada por interações em tempo real, incluindo sons e manipulação de modelos 3D, com suporte a um servidor de comunicação via JSON.

Funcionalidades:

1. Detecção de Gestos com as Mãos:
   - Identifica o número de dedos levantados
   - Controla o comportamento de um "cão virtual" com base nos gestos detectados

2. Detecção de Objetos com YOLO:
   - Detecta objetos de interesse, como peluche, copos, garrafas e telemoveis.
   - Gera dados JSON para os objetos detectados e carrega modelos 3D associados.

3. Detecção de Cabeça com MediaPipe:
   - Identifica a posição do nariz para determinar ações como rotação ou backflip.

4. Servidor de Comunicação JSON:
   - Permite que clientes solicitem dados atualizados do estado do sistema

5. Interação em Tempo Real:
   - Exibe as detecções em vídeo ao vivo
   - Emite sons relacionados às interações