from quart import Quart, websocket

app = Quart(__name__)
clients = []
nicknames = []

async def broadcast(message):
    for client in clients:
        await client.send(message)

@app.route("/")
async def home():
    return "Salut !"

@app.websocket("/ws")
async def message():
    message_new_connection = await websocket.receive_json()
    if message_new_connection["username"] in nicknames:
        await websocket.send("nickname déjà enregistré")
        return
    clients.append(websocket._get_current_object())
    nicknames.append(message_new_connection["username"])
    await broadcast(f"{message_new_connection['username']} a rejoint le salon.")
    try:
        while True:
            message = await websocket.receive()
            if not message == "nickname déjà enregistré":
                await broadcast(message)
    except:
        if websocket._get_current_object() in clients:
            index_client = clients.index(websocket._get_current_object())
            clients.remove(websocket._get_current_object())
            nickname = nicknames[index_client]
            nicknames.remove(nickname)
            await broadcast(f"{message_new_connection['username']} a quitté le salon.")



if __name__ == "__main__":
    app.run()
