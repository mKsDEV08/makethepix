from flask_socketio import namespace
import os
from gtts import gTTS
from pydub import AudioSegment
import string
import random
from connector import User, Message, session


class Alerts(namespace.Namespace):
    def on_user_connected(self, data):
        username = data["username"]
        print(f"The user {username} is connected")

    def on_alert_completed(self, data):
        sound_path = data["sound_message_path"]
        sound_path = sound_path.replace("..", ".")

        os.remove(sound_path)

    def on_disconnect(self):
        pass


class TextToSpeech():
    def __init__(self, text: str, filename: str, pitch: float, lang: str = 'pt', tld: str = 'com.br'):
        self.text = text
        self.filename = filename
        self.pitch = pitch
        self.lang = lang
        self.tld = tld

    def generate(self):
        tts = gTTS(self.text, lang=self.lang, tld=self.tld)
        temp_filename = f'static/sounds/messages/{self.filename}-temp.mp3'
        final_filename = f'static/sounds/messages/{self.filename}.mp3'
        tts.save(temp_filename)
        speedup = AudioSegment.from_mp3(temp_filename)
        speedup = speedup.speedup(playback_speed=self.pitch)

        speedup.export(final_filename, format='mp3')
        os.remove(f'./{temp_filename}')
        
        return f'../{final_filename}'
    
    
def random_string(lenght):

    letters = string.ascii_lowercase
    numbers = string.digits
    chars = letters + numbers

    rand = ''.join(random.choice(chars) for i in range(lenght))
    return rand


def generate_id():
    
    def check_id():
        new_id = random_string(24)

        results = session.query(User.alert_id).filter(User.alert_id == new_id)
        result = []
        for r in results:
            result.append(r)

        return [result, new_id]
    
    check = check_id()

    while(check[0] != []):
        check = check_id()

    return check[1]


def create_message(message_id: int, receiver_alert_id: str):
    print(message_id)

    message = session.get(Message, message_id)

    text = message.message
    sender = message.sender_name
    status = message.status
    value = message.value
    message_alert_id = message.receiver_alert_id
    
    if status != 'approved': return False
    if message_alert_id != receiver_alert_id: return False

    value = str(value)
    value = value.split('.')
    
    if len(value[1]) == 1: value[1] = f'{value[1]}0'

    reais = value[0]
    centavos = value[1]
    value = f'R${reais},{centavos}'

    user_preferences = session.query(User.pitch_choose, User.lang_choose).filter(User.alert_id == message_alert_id)[0]
    pitch_choose = user_preferences[0]
    lang_choose = user_preferences[1]

    final_message = f'{sender} mandou {reais} reais e {centavos} centavos: {text}'
    sound_message_path = TextToSpeech(final_message, message_id, pitch_choose, tld=lang_choose).generate()

    response = {
        'sender_name': sender,
        'value': value,
        'text': text,
        'sound_message_path': sound_message_path
    }

    return response