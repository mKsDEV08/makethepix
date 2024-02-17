from helpers import create_message, db, TextToSpeech


db.execute("SELECT * FROM users WHERE alert_id = %s", ("0aqc4iqbv93zbcvkwbs4lmps",))
print(db.fetchall())