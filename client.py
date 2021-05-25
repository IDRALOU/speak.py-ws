import websocket
import json
import threading
import base64
import getpass
import os

def send_message(ws):
    while True:
        message = getpass.getpass("")
        try:
            ws.send('{"event": "post message", "username": ' + f'"{username}", ' + '"message": ' f'"{message}"' + '}')
        except:
            pass

def on_message(ws, message):
    if message == "nickname déjà enregistré":
        os.system("cls")
        print("Le nom d'utilisateur est déjà enregistré, veuillez en choisir un autre.")
        input("Appuyez sur une touche pour continuer...")
        os.kill(os.getpid(), 3)
    elif message == "close":
        os.kill(os.getpid(), 3)
    message_json = json.loads(message)
    if not message_json["username"] == username:
        print(" ")
    if message_json["type"] == "message":
        print(f"{message_json['username']}: {message_json['message']}")
    elif message_json["type"] == "connection":
        print(f"{message_json['username']} s'est connecté")
    elif message_json["type"] == "leave":
        print(f"{message_json['username']} a quitté le salon")

def on_open(ws):
    ws.send('{"event": "connect", "username": ' + f'"{username}"' + '}')
    thread_send = threading.Thread(target=send_message, args=[ws])
    thread_send.start()

if __name__ == "__main__":
    global username
    username = input("Nom d'utilisateur: ")
    os.system("cls") if os.name == "nt" else os.system("clear")
    url_chat = input("URL du chat (Exemple: jesaispasquoi.com): ")
    os.system("cls") if os.name == "nt" else os.system("clear")
    while True:
        try:
            ws = websocket.WebSocketApp(f"wss://{url_chat}", on_message=on_message, on_open=on_open)
            ws_check = ws.run_forever()
            if ws_check == True:
                print("L'URL du chat est incorrecte.")
                input("Appuyez sur une touche pour continuer...")
                os.kill(os.getpid(), 3)
        except Exception as e:
            print(e)
