# Projeto: Sistema Interativo de Detecção de Gestos, Objetos e Posição da Cabeça  

Este projeto utiliza visão computacional para criar um sistema interativo que combina detecção de gestos, objetos e posição da cabeça. Ele integra bibliotecas como YOLO, MediaPipe e OpenCV para fornecer interações em tempo real com sons, manipulação de modelos 3D e comunicação JSON via servidor.

## Funcionalidades Principais

1. **Detecção de Gestos com as Mãos**  
   - Reconhece o número de dedos levantados.  
   - Controla o comportamento de um "cão virtual" com base nos gestos identificados 

2. **Detecção de Objetos com YOLO**  
   - Detecta objetos como peluches, copos, garrafas e telemóveis.  
   - Gera dados JSON para os objetos detectados e associa modelos 3D a cada um  

3. **Detecção de Posição da Cabeça com MediaPipe**  
   - Acompanha a posição do nariz para acionar animações, como backflips ou rotações  

4. **Servidor de Comunicação JSON**  
   - Disponibiliza dados atualizados do sistema para clientes conectados  

5. **Interação em Tempo Real**  
   - Exibe vídeo ao vivo com as detecções em destaque 
   - Emite sons relacionados às ações realizadas pelo sistema 

## Requisitos  

- **Python 3.8** ou superior  
- **Bibliotecas Python:**  
  - `opencv-python`  
  - `mediapipe`  
  - `ultralytics`  
  - `pygame`  
  - `numpy`  

## Como Configurar e Executar  

### 1. **Preparação dos Arquivos**  

- Faça o download e extraia a pasta do projeto (`TF_a79299_a71433`) no seu computador.  
- Copie a pasta extraída para uma nova pasta chamada **"Computação Visual"** no **Desktop** do seu computador.  

### 2. **Configuração no Blender**  

1. **Abrir Arquivo Blender**  
   - Inicie o Blender.  
   - Acesse **File > Open** e selecione o arquivo `untitled 1.blend` na subpasta `Blender` do projeto.  

2. **Configurar a Textura da Relva**  
   - No canto inferior direito, acesse a aba **Material**.  
   - Clique em **Cor Base** e selecione **Textura de Imagem**.  
   - Carregue o arquivo `Relva.png` da pasta do projeto.  

3. **Iniciar o Servidor no Blender**  
   - Acesse a aba **Scripting** no topo da interface do Blender.  
   - Clique em **Open** e selecione o arquivo `blender.py`.  

### 3. **Configuração no VSCode**  

1. **Abrir o Projeto**  
   - Abra o VS Code.  
   - Vá em **File > Open Folder** e selecione a pasta do projeto.  

2. **Instalar Dependências**  
   - No terminal do VS Code, execute:  
     ```pip install opencv-python mediapipe ultralytics pygame numpy```  

3. **Executar o Código**  
   - No terminal, execute o script principal:  
     ```python.exe .\main.py```  

### 4. **Executar o Projeto**  

1. **Iniciar o Servidor no Blender**  
   - Na aba **Scripting**, clique no botão **Play**.  
   - Verifique a mensagem `bpy.ops.text.run_script()` indicando que o servidor está ativo.  

2. **Executar o Cliente no VS Code**  
   - Certifique-se de que o script `main.py` está em execução no terminal do VS Code.  

3. **Usar Funcionalidades**  

   - **Inserir Objetos:**  
     - Pressione a tecla **Z** para detectar objetos na tela:  
       - **Peluche** → Cão  
       - **Garrafa** → Brinquedo  
       - **Copo** → Tigela  
       - **Telemóvel** → Árvore  

   - **Controlar o Cão Virtual:**  
     - Pressione a tecla **S** para ativar a detecção de gestos:  
       - **1 dedo levantado** → O cão vai até o brinquedo.  
       - **5 dedos levantados** → O cão volta à posição central.  
       - **3 dedos levantados** → O cão vai até a tigela.  
       - **Cabeça para cima** → O cão realiza um backflip.  
       - **Cabeça para os lados** → O cão gira no mesmo local.  

   - **Encerrar o Programa:**  
     - Pressione a tecla **Q** para sair.  

## Observações  

- Certifique-se de que todas as dependências estão corretamente instaladas.  
- Execute os scripts na ordem especificada para evitar erros de sincronização.  