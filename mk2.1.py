import mido
import subprocess
import json
import win32api
import win32con

# Define the applications to map to MIDI input
applications = {
    0: {'path': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', 'display': 1, 'x': 0, 'y': 0},
    1: {'path': 'C:\\Users\\Alex\\AppData\\Local\\Discord\\app-1.0.9020\\Discord.exe', 'display': 2, 'x': 100, 'y': 100},
    2: {'path': 'C:\\Users\\Alex\\AppData\\Roaming\\Spotify\\Spotify.exe', 'display': 1, 'x': 0, 'y': 0},
}

# Get a list of available input ports
input_ports = mido.get_input_names()

# Use the first available input port
if input_ports:
    port_name = input_ports[0]
else:
    print('No MIDI input ports found.')
    exit()

# Set up the MIDI input listener
with mido.open_input(port_name) as port:
    print(f'Listening to {port_name}...')

    # Load the saved window information from file
    try:
        with open('windows.json', 'r') as f:
            windows = json.load(f)
    except FileNotFoundError:
        windows = {}

    # Initialize the volume level to 50%
    volume_level = 50

    # Flag to keep track of whether the pause button has been pressed
    pause_pressed = False

    # Initialize current_application
    current_application = 0

    # Define LED note numbers for actions
    LED_VOLUME_UP = 96
    LED_VOLUME_DOWN = 112
    LED_SKIP_SONG = 115
    LED_SKIP_TO_NEXT_SONG = 116
    LED_PAUSE_PLAY = 114
    LED_GO_BACK = 113

    # Get a list of available output ports
    output_ports = mido.get_output_names()

    # Use the first available output port
    if output_ports:
        output_port_name = output_ports[0]
    else:
        print('No MIDI output ports found.')
        exit()

    # Set up the MIDI output port
    output_port = mido.open_output(output_port_name)

    # Create a function to control the LEDs
    def control_led(note, state):
        # Send a MIDI message to control the LED for the specified note
        message = mido.Message('note_on', note=note, velocity=127 if state else 0)
        output_port.send(message)

    for message in port:
        note = message.note
        velocity = message.velocity

        # Handle actions and control LEDs
        if velocity > 0:
            if note == LED_VOLUME_UP:
                # Increase volume
                volume_level = 100
                control_led(note, True)
                if current_application == 0:
                    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif current_application == 2:
                    win32api.keybd_event(win32con.VK_MEDIA_VOLUME_UP, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_MEDIA_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP, 0)
            # Add similar control for other actions (LED_VOLUME_DOWN, LED_SKIP_SONG, etc.)
            
            # Reset LEDs for other buttons
            for led_note in [LED_VOLUME_UP, LED_VOLUME_DOWN, LED_SKIP_SONG, LED_SKIP_TO_NEXT_SONG, LED_PAUSE_PLAY, LED_GO_BACK]:
                if led_note != note:
                    control_led(led_note, False)

        # Save the window information to file
        with open('windows.json', 'w') as f:
            json.dump(windows, f)
