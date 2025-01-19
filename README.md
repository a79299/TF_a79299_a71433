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

Requisitos:
    - Python 3.8 ou superior
    - Bibliotecas Python:
    - `opencv-python`
    - `mediapipe`
    - `ultralytics`
    - `pygame`
    - `numpy`


Como executar o projeto:
    1. Descarregue e descompacte a pasta do trabalho "TF_a79299_a71433" para o seu computador
    
    2. Criei uma pasta chamada "Computacao Visual" no desktop do seu computador e insira a pasta "TF_a79299_a71433"

    3. Abra o Blender
    - Carregue no botão "File" no canto superior esquerdo
    - Carregue no botão "Open"
    - Selecione o ficheiro "untitled 1.blend" que esta dentro da pasta "Blender" na pasta que descarregou "TF_a79299_a71433"

    4. Carregar Relva
        - No canto inferior direito carregue em "Material"
        - Carregue em "cor base" e de seguida em "textura de imagem"
        - Carregue no botão de "Abrir" e selecione o ficheiro "Relva.png" que esta dentro da pasta que descarregou

    5. Carregar Servidor no blender
        - Carregue na aba "Scripting" no blender na parte superior
        - Clique em "Abrir" e selecione o ficheiro "blender.py" que esta dentro da pasta que descarregou

    6. Carregar a pasta no vscode
        - Abra o Vscode
        - Clique me "File" no canto superior esquerdo e Clique em "open Folder"
        - Selecione a pasta que descarregou
        - no terminal execute este comando "pip install opencv-python mediapipe ultralytics pygame numpy"

    4. Execução do Projeto
    - No blender na aba "Scripting" carregue no botão de play
    - Irá aparecer a mensagem "bpy.ops.text.run_script()" que indica que esta a correr o sevidor na parte do cliente
    - No vscode vá no ficheiro do main.py e no terminal execute este comando "python.exe .\main.py"
    - Abrirá uma janela que é o programa em execução

    5. Executar Funcionalidades:
        Inserir Objetos:
        - CLique no botão "z" do teclado que ira detectar os objetos no ecra 
        - peluche -> cão, garrafa -> brinquedo, copo -> tigela, Telemovel -> Arvore

        Movimentações do cão:
        - CLique no botão "s" do teclado que ira detectar as mãos
        - 1 dedo levantado -> cão vai ate ao brinquedo
        - 5 dedos levantados -> volta a posição central
        - 3 dedos levantados -> vai ate á tigela
        - levantar a cabeça para cima -> cão da um backflip
        - Virar cabeça para o lado -> cão roda no mesmo sitio 

        Terminar programa:
        - Clique no "Q" para sair
