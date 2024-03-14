import subprocess
import time


def disconnect() -> bool:
    command = 'rasdial "Mobily Prepaid Plan" /disconnect'

    # Execute the command
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False


def connect() -> bool:
    command = 'rasdial "Mobily Prepaid Plan"'

    # Execute the command
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False
