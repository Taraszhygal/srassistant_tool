import argparse
import sys
import subprocess 
from   subprocess import check_call, CalledProcessError, STDOUT
import os
import importlib
from tarfile import RECORDSIZE

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass

def install():
    print("Installing...")
    # implement pip as a subprocess:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'vosk'])
        # process output with an API in the subprocess module:
        reqs = subprocess.check_output([sys.executable, '-m', 'pip','freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]
        print(installed_packages)
        runcmd('apt install -y python3-pyaudio unzip') 
        #print("pyaudio installed")
        #download ukr model audio semple
        runcmd('wget https://alphacephei.com/vosk/models/vosk-model-small-uk-v3-nano.zip')
        runcmd('unzip vosk-model-small-uk-v3-nano.zip && rm vosk-model-small-uk-v3-nano.zip')
    except CalledProcessError as e:
        print(e.output)

def start():
    vosk = importlib.import_module('vosk')
    model = getattr(vosk, 'Model')
    kr = getattr(vosk, 'KaldiRecognizer')
    pyaudio = importlib.import_module('pyaudio')
    print("Starting...")
        
    #read the model
    ukrm = model('./vosk-model-small-uk-v3-nano')
    recognizer = kr (ukrm, 16000)
    
    #recognize micro
    cap = pyaudio.PyAudio()
    stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            res = recognizer.Result()
            json = json.loads(res)
            print(json["text"])
        
        

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
