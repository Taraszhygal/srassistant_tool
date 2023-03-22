import argparse

def install():
    print("Installing...")

def start():
    print("Starting...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Install and start application")
    parser.add_argument('--install', action='store_true', help='Install required dependensies')
    parser.add_argument('--start', default=None, help='Command recognition assistant started')

    args = parser.parse_args()

    if args.install:
        install()
    elif args.start:
        start()
    else:
        parser.print_help()
