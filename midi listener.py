import mido

# Find the first available MIDI input
input_name = None
for name in mido.get_input_names():
    if '' in name:
        input_name = name
        break

if input_name is None:
    print('No MIDI input found')
else:
    print(f'Connecting to {input_name}')
    with mido.open_input(input_name) as port:
        for message in port:
            print(message)
