# Imports
import argparse
import subprocess
import webbrowser

def commandLine():
    parser = argparse.ArgumentParser(description = "Local HTTP server")
    parser.add_argument("-r", "--run", action = "store_true", help = "Start an HTTP server", required = False, default = "")
    parser.add_argument("-o", "--open", nargs = 1, help = "Open webpage on running server", required = False, default = "")
    parser.add_argument("-s", "--stop", action = "store_true", help = "Stop running server", required = False, default = "")
    
    args = parser.parse_args()
    
    if args.run:
        print("Starting server @ port 8000...")
        subprocess.run(["python", "-u", "-m", "http.server", "8000"], check=True)
    
    elif args.open:
        print("Opening webpage...")
        webbrowser.open("http://localhost:8000/" + args.open[0], new=2, autoraise=True) # Open new tab; bring to forefront

    elif args.stop:
        print("Stopping server...")
        # TODO: Finish implementation

    else:
        print("Unsupported command")
                
########################
# Main
########################
if __name__=="__main__":
    commandLine()