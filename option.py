import mido

def on_message(msg):
    if msg.type == 'note_on':
        print(f"Note {msg.note} pressed")

with mido.open_input() as port:
    print(f"Listening to {port.name}")
    for msg in port:
        on_message(msg)
