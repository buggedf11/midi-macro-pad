import mido

# Define your password sequence as a list of MIDI note numbers
# Replace these with the actual MIDI note numbers of your desired password sequence
password_sequence = [1, 2, 3, 4, 5, 6, 7, 8]

# Create a dictionary to store the LED state for each button (0-127)
led_states = {note: False for note in range(128)}

# Create a list to store the currently entered numbers
entered_numbers = []

# Function to set the LED state for a button
def set_led_state(note, state):
    led_states[note] = state

# Function to update the LEDs on the Launchpad
def update_leds():
    with mido.open_output('Launchpad 0') as port:  # Update to your device's name
        for note, state in led_states.items():
            # Send a MIDI message to control the LED for the specified note
            message = mido.Message('note_on', channel=0, note=note, velocity=127 if state else 0, time=0)
            port.send(message)

# Function to display the entered numbers on the Launchpad
def display_entered_numbers():
    for i, number in enumerate(entered_numbers):
        set_led_state(number, True)
        update_leds()

# Function to listen to MIDI input from the "Launchpad 0" device and check for the password
def listen_for_password():
    received_notes = []
    
    while True:
        with mido.open_input('Launchpad 0') as port:  # Update to your device's name
            for msg in port:
                if msg.type == 'note_on':
                    received_notes.append(msg.note)

                    # Check if the received notes match the password sequence
                    if received_notes == password_sequence:
                        print("Access granted!")
                        # Light up the buttons for the password sequence
                        for note in received_notes:
                            set_led_state(note, True)
                        update_leds()
                        return
                    else:
                        # Incorrect input, display entered numbers and set LEDs accordingly
                        entered_numbers = received_notes[-len(password_sequence):]
                        display_entered_numbers()
                elif msg.type == 'note_off':
                    received_notes = []

if __name__ == "__main__":
    listen_for_password()
