from utils import set_timeout, fetch

last_seen_id = 0

send_message = document.getElementById("send_message")
sender = document.getElementById("sender")
message_text = document.getElementById("message_text")
chat_window = document.getElementById("chat_window")
zoo_selector = document.getElementById("zoo_selector")

def append_message(message):
    item = document.createElement("li")
    item.className = "list-group-item"
    item.innerHTML = f'[<b>{message["sender"]}</b>]: <span>{message["text"]} </span><span class="badge bg-info text-dark">{message["time"]}</span>'
    chat_window.prepend(item)

async def send_message_click(e):
    full_name = zoo_selector.value + sender.value
    await fetch(f"/send_message?sender={full_name}&text={message_text.value}", method="GET")
    message_text.value = ""

async def load_fresh_messages():
    global last_seen_id
    result = await fetch(f"/get_messages?after={last_seen_id}", method="GET")
    data = await result.json()
    all_messages = data["messages"]
    for msg in all_messages:
        last_seen_id = msg["msg_id"]
        append_message(msg)
    set_timeout(1, load_fresh_messages)


async def message_enter(event):
    console.log(event.code)
    if event.code == "Enter":
        await send_message_click(event)

send_message.onclick = send_message_click

message_text.onkeypress = message_enter

load_fresh_messages()
