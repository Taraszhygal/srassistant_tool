import argparse
import sys
import subprocess 
from   subprocess import check_call, CalledProcessError, STDOUT
import os
import importlib



def install():
    print("Installing...")
    # implement pip as a subprocess:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'vosk'])
        # process output with an API in the subprocess module:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        print(installed_packages)
        subprocess.check_call(['apt-get', 'install', '-y', 'python3-pyaudio unzip'], stdout=open(os.devnull,'wb'), stderr=STDOUT) 
        print("pyaudio installed")
        #download ukr model audio semple
        subprocess.check_call(['wget', 'https://alphacephei.com/vosk/models/vosk-model-small-uk-v3-nano.zip'], stderr=STDOUT)
        subprocess.check_call(['unzip', 'vosk-model-small-uk-v3-nano.zip'], stderr=STDOUT)
    except CalledProcessError as e:
        print(e.output)

def start():
    vosk = importlib.import_module('vosk')
    model = getattr(vosk, 'Model')
    kr = getattr(vosk, 'KaldiRecognizer')
    while True:
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
