# Imports
import argparse

class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser(description = "Local HTTP server")
        parser.add_argument("-o", "--open", help = "", required = False, default = "")
        parser.add_argument("-r", "--run", help = "", required = False, default = "") # TODO: Add input var for HTML directory
        parser.add_argument("-c", "--close", help = "", required = False, default = "")
        
        argument = parser.parse_args()
        self.parse(argument)

    def parse(self, arg):
        match arg:
            case arg.open:
                print("cmd")

            case arg.run:
                print("cmd")

            case arg.close:
                print("cmd")

            case _:
                print("unsupported")
                
########################
# Main
########################
if __name__=="__main__":
    CommandLine()