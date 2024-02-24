from connector import User, session

r = session.get(User, 1)

print(r.alert_id)