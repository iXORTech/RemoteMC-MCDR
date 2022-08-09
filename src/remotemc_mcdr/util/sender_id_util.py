import uuid

sender_id: str


def generate_sender_id():
    global sender_id
    sender_id = uuid.uuid4().hex.upper()
    return sender_id


def get_sender_id():
    return sender_id


def is_the_same_sender_id(received_sender_id: str):
    return received_sender_id == sender_id
