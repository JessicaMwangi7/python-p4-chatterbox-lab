#!/usr/bin/env python3

from random import choice as rc
from faker import Faker

from app import app
from models import db, Message

fake = Faker()

usernames = [fake.first_name() for i in range(4)]
if "Duane" not in usernames:
    usernames.append("Duane")

def make_messages():
    with app.app_context():  # Ensure we are in the app context
        Message.query.delete()  # Clear old messages
        db.session.commit()  # Apply delete

        messages = []

        for i in range(20):
            message = Message(
                body=fake.sentence(),
                username=rc(usernames),
            )
            messages.append(message)

        db.session.add_all(messages)
        db.session.commit()

        # ✅ Print messages count
        print(f"✅ Seeded {len(messages)} messages!")

if __name__ == '__main__':
    make_messages()