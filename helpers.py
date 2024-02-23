from flask_socketio import namespace
import os
from gtts import gTTS
from pydub import AudioSegment
import string
import random
from mysql.connector.cursor_cext import CMySQLCursor
import mysql.connector

connection = mysql.connector.connect(
    user = 'root',
    host = 'localhost',
    password = 'password',
    database = 'makethepix'
)

db = connection.cursor()


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


def generate_id(cursor: CMySQLCursor):
    
    new_id = random_string(24)

    cursor.execute("SELECT alert_id FROM users WHERE alert_id = %s", (new_id,))

    while(cursor.fetchall() != []):
        new_id = random_string(24)
        cursor.execute("SELECT alert_id FROM users WHERE alert_id = %s", (new_id,))

    return new_id


def create_message(cursor: CMySQLCursor, message_id: int, receiver_alert_id: str):
    print(message_id)

    cursor.execute("SELECT * FROM messages WHERE id = %s", (message_id, ))
    message_data = cursor.fetchall()[0]

    text = message_data[1]
    sender = message_data[2]
    status = message_data[3]
    value = message_data[4]
    message_alert_id = message_data[5]
    
    if status != 'approved': return False
    if message_alert_id != receiver_alert_id: return False

    value = str(value)
    value = value.split('.')
    
    if len(value[1]) == 1: value[1] = f'{value[1]}0'

    reais = value[0]
    centavos = value[1]
    value = f'R${reais},{centavos}'

    cursor.execute("SELECT * FROM users WHERE alert_id = %s", (receiver_alert_id,))
    receiver_data = db.fetchall()[0]

    final_message = f'{sender} mandou {reais} reais e {centavos} centavos: {text}'
    sound_message_path = TextToSpeech(final_message, message_id, 1.35, tld=receiver_data[5]).generate()

    response = {
        'sender_name': sender,
        'value': value,
        'text': text,
        'sound_message_path': sound_message_path
    }

    return response