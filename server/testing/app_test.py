from datetime import datetime

from app import app
from models import db, Message

class TestApp:
    '''Flask application in app.py'''

    # Cleanup any old messages before starting tests
    with app.app_context():
        m = Message.query.filter(
            Message.body == "Hello 👋"
        ).filter(Message.username == "Liza")

        for message in m:
            db.session.delete(message)

        db.session.commit()

    def test_has_correct_columns(self):
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            
            db.session.add(hello_from_liza)
            db.session.commit()

            # Test the columns
            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            # Cleanup after test
            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_returns_list_of_json_objects_for_all_messages_in_database(self):
        '''returns a list of JSON objects for all messages in the database.'''
        with app.app_context():
            response = app.test_client().get('/messages')
            records = Message.query.all()

            # Check if the response JSON contains valid message IDs and bodies
            for message in response.json:
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self):
        '''creates a new message in the database.'''
        with app.app_context():
            # Post a new message
            app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )

            # Check if the message is saved in the database
            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            # Cleanup after test
            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self):
        '''returns data for the newly created message as JSON.'''
        with app.app_context():
            # Post a new message
            response = app.test_client().post(
                '/messages',
                json={
                    "body": "Hello 👋",
                    "username": "Liza",
                }
            )

            # Check if the response is in JSON format and correct data
            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")

            # Cleanup after test
            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)
            db.session.delete(h)
            db.session.commit()

    def test_updates_body_of_message_in_database(self):
        '''updates the body of a message in the database.'''
        with app.app_context():
            # Ensure a message exists before running the test
            m = Message.query.first()
            if not m:
                m = Message(body="Initial Message", username="TestUser")
                db.session.add(m)
                db.session.commit()

            # Store the original values
            id = m.id
            body = m.body

            # Update the message body
            app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body": "Goodbye 👋",
                }
            )

            # Ensure the body was updated using the new method
            g = db.session.get(Message, id)  # Use db.session.get to avoid deprecation warning
            assert g.body == "Goodbye 👋"

            # Revert the change back to the original body
            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_updates_message_body(self):
        '''Another test for updating the body of a message in the database.'''
        with app.app_context():
            # Ensure a message exists before running the test
            m = Message.query.first()
            if not m:
                m = Message(body="Test Message", username="TestUser")
                db.session.add(m)
                db.session.commit()

            # Store the original values
            id = m.id
            body = m.body

            # Update the message body
            app.test_client().patch(
                f'/messages/{id}',
                json={
                    "body": "Updated Message Body 👋",
                }
            )

            # Ensure the body was updated using the new method
            g = db.session.get(Message, id)
            assert g.body == "Updated Message Body 👋"

            # Revert the change back to the original body
            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_deletes_message_from_database(self):
        '''deletes the message from the database.'''
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            # Delete the message via the API
            app.test_client().delete(
                f'/messages/{hello_from_liza.id}'
            )

            # Ensure the message was deleted
            h = Message.query.filter_by(body="Hello 👋").first()
            assert(not h)
