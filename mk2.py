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

    for message in port:
        note = message.note
        velocity = message.velocity
        if velocity > 0:
            if note == 96:
                # Increase volume
                volume_level = 100
                if current_application == 0:
                    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif current_application == 2:
                    win32api.keybd_event(win32con.VK_MEDIA_VOLUME_UP, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_MEDIA_VOLUME_UP, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif note == 112:
                # Decrease volume
                volume_level = 10
                if current_application == 0:
                    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif current_application == 2:
                    win32api.keybd_event(win32con.VK_MEDIA_VOLUME_DOWN, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_MEDIA_VOLUME_DOWN, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif note == 115:
                # Skip song
                if current_application == 0:
                    win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif current_application == 2:
                    win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)
            elif note == 116:
                # Skip to next song
                if not skip_pressed:
                    skip_pressed = True
                    if current_application == 0:
                        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, 0, 0)
                    elif current_application == 2:
                        win32api.keybd_event(win32con.VK_MEDIA_NEXT_TRACK, 0, 0, 0)
            elif note == 114:
                # Pause/Play
                if not pause_pressed:
                    pause_pressed = True
                    if current_application == 0:
                        win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
                    elif current_application == 2:
                        win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
                else:
                    pause_pressed = False
                if current_application == 0:
                    win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif current_application == 2:
                    win32api.keybd_event(win32con.VK_MEDIA_PLAY_PAUSE, 0, 0, 0)
            elif note == 113:
                # Go back a song
                if current_application == 0:
                    win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)
                elif current_application == 2:
                    win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, 0, 0)
                    win32api.keybd_event(win32con.VK_MEDIA_PREV_TRACK, 0, win32con.KEYEVENTF_KEYUP, 0)

            # Trigger the specified application
            if note in applications:
                application_path = applications[note]['path']
                display_num = applications[note]['display']
                x_pos = applications[note]['x']
                y_pos = applications[note]['y']
                try:
                    # Check if the window is already open
                    if application_path in windows:
                        # If it is, move it to the correct position
                        subprocess.call(['powershell', '-Command', f'$w = Get-Process "{{application_path.split("\\\\")[-1].split(".")[0]}}"; $w.MainWindowHandle | ForEach-Object {{Set-Window -ProcessId $w.Id -WindowHandle $_ -X {x_pos} -Y {y_pos}}};'])
                    else:
                        # If it's not, open it and save the window information
                        startupinfo = subprocess.STARTUPINFO()
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        startupinfo.wShowWindow = 3
                        startupinfo.lpReserved = None
                        startupinfo.lpDesktop = None
                        startupinfo.lpTitle = None
                        startupinfo.cbReserved2 = 0
                        startupinfo.lpReserved2 = None
                        startupinfo.dwX = x_pos
                        startupinfo.dwY = y_pos
                        startupinfo.dwXSize = 0
                        startupinfo.dwYSize = 0
                        startupinfo.dwXCountChars = 0
                        startupinfo.dwYCountChars = 0
                        startupinfo.dwFillAttribute = 0
                        startupinfo.dwFlags |= 4  # Use position
                        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                        startupinfo.dwFlags |= subprocess.STARTF_USESTDHANDLES

                        subprocess.Popen(application_path, startupinfo=startupinfo, creationflags=subprocess.DETACHED_PROCESS)
                        windows[application_path] = {'x': x_pos, 'y': y_pos}

                except OSError as e:
                    print(f'Error: {e}')

        # Save the window information to file
        with open('windows.json', 'w') as f:
            json.dump(windows, f)

            