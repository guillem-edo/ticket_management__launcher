# app/user.py
class User:
    def __init__(self, username, password, blocks, is_admin=False):
        self.username = username
        self.password = password
        self.blocks = blocks
        self.is_admin = is_admin