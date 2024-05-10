import sys
import codecs

sys.path.append("C:\\Users\\Windows 10\\Pictures\\Nao\\lib")

from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", "192.168.43.96", 9559)

phrase = ""

for text in sys.argv:
    if text == sys.argv[0]:
        pass
    else:
        phrase += text + " "

phrase = phrase.decode('utf-8', 'ignore')
phrase = phrase.encode('utf-8', 'ignore')
print(phrase)
tts.say(phrase)