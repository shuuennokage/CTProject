import sys

import telegram
import pygraphviz
from flask import Flask, request
from time import sleep
from transitions import State
from transitions.extensions import GraphMachine as Machine
import random

app = Flask(__name__)
botToken = "438457440:AAFiiRCzMGW-vlBC2Jv43W4vdR0uULkzEvo"
bot = telegram.Bot(botToken)

states = [
    'swamp',
    'volcano',
    'maou',
    'dead',
    'win'
]

transitions = [
    ['area1_clear', 'swamp', 'volcano'],
    ['area2_clear', 'volcano', 'maou'],
    ['die1', 'swamp', 'dead'],
    ['die2', 'volcano', 'dead'],
    ['die3', 'maou', 'dead'],
    ['die_maou', 'maou', 'win']
]

class Game(Machine):
    pass

gameBot = Game(states = states, transitions = transitions, initial = 'swamp')
print(gameBot.state)

def main():
    seekP = 0;
    gameActive = 0;
    STR = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    CON = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    POW = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    DEX = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    SIZ = random.randint(0, 6) + random.randint(0, 6) + 6
    INT = random.randint(0, 6) + random.randint(0, 6) + 6
    LUK = POW * 5
    HP = (CON + SIZ) / 2
    HPMax = HP
    lastMessageId = 0;
    updates = bot.getUpdates();

    if (len(updates)>0):
        lastMessageId = updates[-1]["update_id"]
    
    while(True):
        updates = bot.getUpdates(offset=lastMessageId)
        updates = [update for update in updates if update["update_id"]>lastMessageId]
        for update in updates:
            text = update["message"]["text"];
            msg_id = update["update_id"];
            user_id = update["message"]["from_user"]["id"]
            lastMessageId = msg_id;
            bot.sendMessage(user_id, text);
        #game loop
        
        sleep(0.5);

if __name__ == "__main__" :
    main()
