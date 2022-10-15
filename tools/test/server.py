# Imports
import sys

def open():
    python3 -m http.server

def launch(url):

def close():


########################
# Main
########################
if __name__=="__main__":
    print("""
    Server Commands:
    1. "open"
    2. "launch  [local URL]"
    3. "close"
    """)

    # Run until user exits program
    while True:
        # Get program command
        command, url = input("\nEnter command: ")

        match command:
            case "open":
                open()
            case "launch":
                launch(url)
            case "close":
                close()
            case "exit":
                quit()
            case _: print("Command not supported")