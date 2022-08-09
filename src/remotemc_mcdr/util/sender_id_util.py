import uuid

sender_id: str


def generate_sender_id():
    global sender_id
    sender_id = uuid.uuid4().hex.upper()
    return sender_id


def get_sender_id():
    return sender_id
