import websocket
import threading
import getpass
import os

def send_message(ws):
    while True:
        message = getpass.getpass("")
        ws.send(f"{username}: {message}")

def on_message(ws, message):
    if message == "nickname déjà enregistré":
        os.system("cls")
        print("Le nom d'utilisateur est déjà enregistré, veuillez en choisir un autre.")
        input()
        os.kill(os.getpid(), 3)
    if not message[:int(len(username))] == username:
        print(" ")
    print(message)

def on_open(ws):
    ws.send('{"event": "connect", "username": ' + f'"{username}"' + '}')
    thread_send = threading.Thread(target=send_message, args=[ws])
    thread_send.start()

if __name__ == "__main__":
    global username
    username = input("Nom d'utilisateur: ")
    os.system("cls") if os.name == "nt" else os.system("clear")
    while True:
        ws = websocket.WebSocketApp("ws://127.0.0.1:5000/ws", on_message=on_message, on_open=on_open)
        ws.run_forever()
