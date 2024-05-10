#! python3.7
import io
import os
import speech_recognition as sr
import torch
from fuzzywuzzy import fuzz

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from sys import platform
import sys

sys.path.append("..\\utils")
from whisperUtils import load_model, get_parser
from promptFormating import prompt_formating

class RealTimeSpeechToText():
    def __init__(self,model_size,name,debug):
        self.name = name
        self.debug = debug
        self.parser = get_parser()
        self.args = self.parser.parse_args()
        if 'linux' in platform:
            self.parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
        self.setMainVars()
        self.setMicrophone()
        self.setAudioModel(model_size)
    def setMainVars(self):
        self.now = datetime.utcnow()
        self.phrase_complete = False
        # The last time a recording was retreived from the queue.
        self.phrase_time = None
        # Current raw audio bytes.
        self.last_sample = bytes()
        # Thread safe Queue for passing data from the threaded recording callback.
        self.data_queue = Queue()
        # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = self.args.energy_threshold
        # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
        self.recorder.dynamic_energy_threshold = False
        # temporal file for audio inputs        
        self.temp_file = NamedTemporaryFile().name
    def setMicrophone(self):
        # Important for linux users. 
        # Prevents permanent application hang and crash by using the wrong Microphone
        if 'linux' in platform:
            self.mic_name = self.args.default_microphone
            if not self.mic_name or self.mic_name == 'list':
                print("Available microphone devices are: ")
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    print(f"Microphone with name \"{name}\" found")   
                return
            else:
                for index, name in enumerate(sr.Microphone.list_microphone_names()):
                    if self.mic_name in name:
                        self.source = sr.Microphone(sample_rate=16000, device_index=index)
                        break
        else:
            self.source = sr.Microphone(sample_rate=16000)
    def setAudioModel(self,model_size):
        # Load / Download model
        self.audio_model = load_model(model_size)

        self.record_timeout = self.args.record_timeout
        self.phrase_timeout = self.args.phrase_timeout

        self.transcription = ['']
        
        with self.source:
            self.recorder.adjust_for_ambient_noise(self.source)
        self.recorder.listen_in_background(self.source, self.record_callback, phrase_time_limit=self.record_timeout)

        # Cue the user that we're ready to go.
        print("Model loaded.\n")

    def Audioloop(self):
        # All the audio logic for preparing the temp file for be translated by the audio_model
        self.phrase_complete = False
        # If enough time has passed between recordings, consider the phrase complete.
        # Clear the current working audio buffer to start over with the new data.
        if self.phrase_time and self.now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
            self.last_sample = bytes()
            self.phrase_complete = True
        # This is the last time we received new audio data from the queue.
        self.phrase_time = self.now

        # Concatenate our current audio data with the latest audio data.
        while not self.data_queue.empty():
            self.data = self.data_queue.get()
            self.last_sample += self.data

        # Use AudioData to convert the raw data to wav data.
        audio_data = sr.AudioData(self.last_sample, self.source.SAMPLE_RATE, self.source.SAMPLE_WIDTH)
        wav_data = io.BytesIO(audio_data.get_wav_data())

        # Write wav data to the temporary file as bytes.
        with open(self.temp_file, 'w+b') as f:
            f.write(wav_data.read())


    def main(self,callback=None):
        while True:
            try:
                self.now = datetime.utcnow()
                # Pull raw recorded audio from the queue.
                if not self.data_queue.empty():
                    self.Audioloop()
                    # Read the transcription.
                    segments, info = self.audio_model.transcribe(self.temp_file, beam_size=2)
                    segment = list(segments)  # The transcription will actually run here.
                    try: 
                        text = (segment[0].text)
                    except:
                        text = ""
                    # If we detected a pause between recordings, add a new item to our transcripion.
                    # Otherwise edit the existing one.
                    if self.phrase_complete:
                        self.transcription.append(text)
                    else:
                        self.transcription[-1] = text
                    # Infinite loops are bad for processors, must sleep.
                    sleep(0.25)
            except KeyboardInterrupt:
                break

        self.finalMessage()    

    def finalMessage(self):
        print("\n\nConversation:")
        for line in self.transcription:
            print(line)       

    def record_callback(self,_, audio:sr.AudioData) -> None:
        """
        Threaded callback function to recieve audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        self.data = audio.get_raw_data()
        self.data_queue.put(self.data)

if __name__ == "__main__":
    voice = RealTimeSpeechToText("small","Maria",True)
    voice.main()
