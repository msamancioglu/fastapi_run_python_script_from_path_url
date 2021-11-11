import sys
def main(arg):
    print(f"Hello from {__file__} file. This is your argument : {arg}")
    
if __name__ == "__main__":
    main(sys.argv[1])