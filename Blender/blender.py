import bpy
import socket
import json
import threading
import time
import math
 
class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
 
    def connect(self):
        """Tenta conectar ao servidor via socket."""
        try:
            self.sock.connect((self.host, self.port))
            self.connected = True
            print("Conectado ao servidor com sucesso.")
        except Exception as e:
            self.connected = False
            print(f"Falha ao conectar ao servidor: {e}")
 
    def listen_and_request(self):
        """Escuta o servidor e solicita dados periodicamente."""
        while self.running:
            if not self.connected:
                self.reconnect()
                time.sleep(2)
                continue
 
            try:
                # Envia uma requisição para obter dados
                request = {"action": "get"}
                self.sock.sendall(json.dumps(request).encode("utf-8"))
 
                # Recebe dados do servidor
                data = self.sock.recv(4096)
                if not data:
                    break
 
                message = data.decode("utf-8")
                detected_objects = json.loads(message)
                self.handle_message(detected_objects)
 
                # Pausa para evitar sobrecarga de requisições
                time.sleep(0.1)
 
            except Exception as e:
                print(f"Erro ao escutar o servidor: {e}")
 
    def reconnect(self):
        """Tenta reconectar ao servidor caso a conexão seja perdida."""
        print("Tentando reconectar ao servidor...")
        self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()
 
    def handle_message(self, objects):
        """Processa os dados recebidos do servidor."""
        try:
            for object in objects:
                name = object.get("name")
                model = object.get("model")
                location = object.get("location", [0, 0, 0])
                rotation = object.get("rotation", [0,0,0])
                scale = object.get("scale",[0,0,0])
 
                # Verifica se os dados são válidos antes de continuar
                if name and model and isinstance(location, list) and len(location) == 3:
                    # Adiciona uma tarefa ao timer do Blender para criar ou atualizar o objeto
                    bpy.app.timers.register(
                        lambda name=name, model=model, location=location, rotation=rotation, scale=scale: self.create_object(name, model, location,rotation,scale)
                    )
        except Exception as e:
            print(f"Erro ao processar a mensagem recebida: {e}")
 
    def stop(self):
        """Encerra o cliente socket."""
        self.running = False
        if self.sock:
            self.sock.close()
        print("Cliente socket encerrado.")
 
    def create_object(self, name, model, location, rotation,scale):
        """Cria ou atualiza um objeto no Blender com rotação e escala ajustados."""
        try:
            # Verifica se o nome está sendo recebido corretamente
 
            obj = bpy.data.objects.get(str(name))
            if obj is None:
                # Importa o modelo OBJ
                bpy.ops.wm.obj_import(filepath=model)
                imported_objects = bpy.context.selected_objects
                for imported_obj in imported_objects:
                    imported_obj.name = name
                    imported_obj.location = tuple(location)
                    imported_obj.scale = tuple(scale)
            else:
                # Atualiza a localização do objeto existente
                obj.location = tuple(location)
                obj.rotation_euler = (math.radians(rotation[0]),math.radians(rotation[1]),math.radians(rotation[2]))
        except Exception as e:
            print(f"Erro ao criar/atualizar objeto '{name}': {e}")
 
 
class ModalSocketOperator(bpy.types.Operator):
    """Operador modal para gerenciar o cliente socket."""
    bl_idname = "wm.modal_socket_operator"
    bl_label = "Socket Client Operator"
 
    def __init__(self):
        self.client = None
 
    def modal(self, context, event):
        """Gerencia eventos do modal no Blender."""
        if event.type == "ESC":
            self.client.stop()
            return {"CANCELLED"}
        return {"PASS_THROUGH"}
 
    def execute(self, context):
        """Inicia o cliente socket e a thread de escuta."""
        self.client = SocketClient("127.0.0.1", 65432)
        self.client.connect()
 
        threading.Thread(target=self.client.listen_and_request, daemon=True).start()
 
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}
 
 
def register():
    """Registra a classe do operador no Blender."""
    bpy.utils.register_class(ModalSocketOperator)
 
 
def unregister():
    """Remove a classe do operador do Blender."""
    bpy.utils.unregister_class(ModalSocketOperator)
 
 
if __name__ == "__main__":
    register()
    bpy.ops.wm.modal_socket_operator("INVOKE_DEFAULT")