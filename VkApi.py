import requests
import json
from random import randint
import logging

class VkApi:
    def __init__(self):
        self.group_id = '183733839'
        self.version = '5.95'
        self.access_token = '994e9307aa5f62c571de613ac17c4719675360c42063d203b30f4986772e37c0bb1d6d4a070c3109c702c'

    def getMembers(self):
        logging.debug('getMembers')
        return requests.get('https://api.vk.com/method/groups.getMembers', {'v': self.version, 'access_token': self.access_token, 'group_id': self.group_id})

    def sendMessageToMembers(self, users, message):
        for user_id in users:
            logging.debug('send message to user {}'.format(user_id))
            requests.post('https://api.vk.com/method/messages.send', {'v': self.version, 'access_token': self.access_token, 'message': message, 'user_id': user_id, 'random_id': randint(0, 1000000)})
