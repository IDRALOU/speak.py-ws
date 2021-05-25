from quart import Quart, websocket
import json

app = Quart(__name__)
clients = []
nicknames = []

async def broadcast(message, username):
    for client in clients:
        await client.send(json.dumps({"type": "message", "username": username, "message": message}))

async def send_new_connection(username):
    for client in clients:
        await client.send(json.dumps({"type": "connection", "username": username}))

async def send_leave(username):
    for client in clients:
        await client.send(json.dumps({"type": "leave", "username": username}))

@app.route("/")
async def home():
    return "Salut !"

@app.websocket("/")
async def ws():
    message_new_connection = await websocket.receive_json()
    if message_new_connection["username"] in nicknames:
        await websocket.send("nickname déjà enregistré")
        return
    elif message_new_connection["event"] != "connect":
        await websocket.send("close")
        return
    clients.append(websocket._get_current_object())
    nicknames.append(message_new_connection["username"])
    await send_new_connection(message_new_connection["username"])
    try:
        while True:
            message = await websocket.receive_json()
            if message["username"] not in nicknames:
                await websocket.send("close")
                break
            if message["event"] == "post message":
                if message["message"] != "nickname déjà enregistré":
                    await broadcast(message["message"], message["username"])
    except:
        if websocket._get_current_object() in clients:
            index_client = clients.index(websocket._get_current_object())
            clients.remove(websocket._get_current_object())
            nickname = nicknames[index_client]
            nicknames.remove(nickname)
            await send_leave(nickname)



if __name__ == "__main__":
    app.run()
