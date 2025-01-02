import pyautogui
import random
import time
import threading
import os

stop_flag = threading.Event()

def read_config():
    config = {}
    config_path = os.path.join(os.path.dirname(__file__), 'config.txt')
    try:
        with open(config_path, 'r') as file:
            for line in file:
                name, value = line.strip().split('=')
                config[name] = int(value)
    except FileNotFoundError:
        print("Config file not found. Using default values.")
    except ValueError:
        print("Error parsing config file. Using default values.")
    print(f"Config: {config}")
    return config

def keep_mouse_moving():
    """
    Keeps the mouse cursor moving randomly on the screen to prevent screen savers.
    """
    while not stop_flag.is_set():
        try:
            # Get screen dimensions
            screen_width, screen_height = pyautogui.size()

            # Generate random coordinates within the screen
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)

            # Move the mouse cursor to the random coordinates
            pyautogui.moveTo(x, y, duration=random.uniform(1, 2)) 

            # Read the configuration values again
            config = read_config()
            wait_time = config.get('wait_time', 10)  # Default to 10 if not found

            # Pause for a random interval
            time.sleep(random.uniform(1, wait_time)) 

        except OSError as e:
            if e.errno == 13:
                print("Error 13 - Must be run as administrator")
            else:
                print(f"An OS error occurred: {e}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

def listen_for_enter():
    input("Press Enter to stop the script...\n")
    stop_flag.set()

if __name__ == "__main__":
    listener_thread = threading.Thread(target=listen_for_enter)
    listener_thread.start()
    keep_mouse_moving()
    listener_thread.join()
    print("Script stopped.")
