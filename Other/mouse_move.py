import pyautogui
import random
import time


def read_config():
    config = {}
    try:
        with open('config.txt', 'r') as file:
            for line in file:
                name, value = line.strip().split('=')
                config[name] = int(value)
    except FileNotFoundError:
        print("Config file not found. Using default values.")
    except ValueError:
        print("Error parsing config file. Using default values.")
    return config

def keep_mouse_moving():
    """
    Keeps the mouse cursor moving randomly on the screen to prevent screen savers.
    """
    while True:
        try:
            # Get screen dimensions
            screen_width, screen_height = pyautogui.size()

            # Generate random coordinates within the screen
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)

            # Move the mouse cursor to the random coordinates
            pyautogui.moveTo(x, y, duration=random.uniform(1, 1)) 

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

if __name__ == "__main__":
    keep_mouse_moving()