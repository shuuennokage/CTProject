# coding=utf-8
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
#print(gameBot.state)

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
    HP = (CON + SIZ) / 2 + 1
    HPMax = HP
    text = 'non'
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
            #bot.sendMessage(user_id, text);
            if(text=='start'):
	        gameActive = 1;
		text = '你成為了又一位的異世界勇者\n準備踏上打倒魔王的旅程...'
		bot.sendMessage(user_id, text);
		text = "人物數值:\nSTR(力量):{0}   CON(體質):{1}   POW(意志):{2}\nDEX(敏捷):{3}   SIZ(體型):{4}   INT(智力):{5}\nHP(生命):{6}".format(STR, CON, POW, DEX, SIZ, INT, HP)
		bot.sendMessage(user_id, text);
		text = 
		while(gameActive):
		    updates = bot.getUpdates(offset=lastMessageId)
        	    updates = [update for update in updates if update["update_id"]>lastMessageId]
        	    for update in updates:
            		text = update["message"]["text"];
            		msg_id = update["update_id"];
            		user_id = update["message"]["from_user"]["id"]
            		lastMessageId = msg_id;
            		bot.sendMessage(user_id, text);
		    sleep(0.5);
	    else:
	        text = '歡迎來到Izayoi的game bot!\n在這裡,你可以成為闖蕩異世界的勇者,展開屬於自己的冒險!\n輸入 start 指令以開始遊戲!'
	        bot.sendMessage(user_id, text);
        #game loop
        
        sleep(0.5);

if __name__ == "__main__" :
    main()
