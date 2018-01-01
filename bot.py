# coding=utf-8
import sys

import telegram
#import graphviz
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
    ['die', '*', 'dead'],
    ['die_maou', 'maou', 'win']
]

class Game(Machine):
    pass

gameBot = Game(states = states, transitions = transitions, initial = 'swamp')
#print(gameBot.state)

def main():
    seekP = 0;
    gameActive = 0;
    textChange = 0;
    against = 0;
    limit = 0;
    sword = 0;
    shield = 0;
    STR = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
    CON = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
    POW = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
    DEX = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
    SIZ = random.randint(1, 6) + random.randint(1, 6) + 6
    INT = random.randint(1, 6) + random.randint(1, 6) + 6
    LUK = POW * 5
    HP = int((CON + SIZ) / 2 + 1)
    HPMax = HP
    aid = 5;
    text = 'non';
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
                sleep(0.2);
                text = '人物數值:\nSTR(力量):{0}   CON(體質):{1}\nPOW(意志):{2}   DEX(敏捷):{3}\nHP(生命上限):{4}   紅色藥水:{5}瓶'.format(STR, CON, POW, DEX, HP, aid)
                bot.sendMessage(user_id, text);
                sleep(0.2);
                text = '起始之地: 血霧沼澤\n...眼前是一片血紅，好似沸騰著的沼地，自地底湧出的魔素蠢蠢欲動，鼻腔裡充斥著血腥與惡臭，你甩甩頭，勇敢面對眼前這片未知的區域。'
                bot.sendMessage(user_id, text);
                sleep(0.2);
                text = '接下來要採取的行動是?\n   探索(輸入 seek)\n   查看自身狀態(輸入status)\n   使用藥水(輸入item)'
                bot.sendMessage(user_id, text);
                sleep(0.2);
                while(gameActive):
                    updates = bot.getUpdates(offset=lastMessageId)
                    updates = [update for update in updates if update["update_id"]>lastMessageId]
                    for update in updates:
                        text = update["message"]["text"];
                        msg_id = update["update_id"];
                        user_id = update["message"]["from_user"]["id"]
                        lastMessageId = msg_id;
                        if(text=='seek' and gameBot.state=='swamp'):
                            textChange = random.randint(1, (6-sword))
                            if(textChange==1 or textChange==2):
                                seekP = seekP + textChange
                                if(textChange==2):
                                    aid = aid + 1
                                    text = '你發現了一瓶紅色藥水。(紅色藥水:{0}瓶)'.format(aid)
                                    bot.sendMessage(user_id, text);
                                    sleep(0.2);
                                text = '周圍的景色像是被火燒過一般，枯木，死地，寸草不生。(調查點+{0})'.format(textChange)
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==3):
                                seekP = seekP + textChange
                                text = '沼澤不斷地冒出血色的氣泡，你嘗試往裡面窺視，看到的卻只有無盡的汙濁。(調查點+{0})'.format(textChange)
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==4):
                                seekP = seekP + textChange
                                against = random.randint(0, 99)
                                limit = (STR*6)
                                if(limit>99):
                                    limit = 99
                                if(against<(STR*6)):
                                    text = '旁邊的刺藤纏住了你的腳踝!你嘗試掙脫:\n(STR抵抗6倍: {0}/{1} 成功)\n你成功掙脫了束縛，刺藤依舊在你背後張牙舞爪地扭動著。(調查點+{2})'.format(against, limit, textChange)
                                else:
                                    HP = HP - 1
                                    text = '旁邊的刺藤纏住了你的腳踝!你嘗試掙脫:\n(STR抵抗6倍: {0}/{1} 失敗)\n你失敗了，刺藤割傷了你的皮膚。(HP-1)(調查點+{2})'.format(against, limit, textChange)
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==5):
                                seekP = seekP + (textChange - 1)
                                against = random.randint(0, 99)
                                limit = (POW*4)
                                if(limit>99):
                                    limit = 99
                                if(against<(POW*4)):
                                    text = '沼澤的毒氣模糊著你的心智，你感覺像要被拉到另一個世界。\n(POW抵抗4倍: {0}/{1} 成功)\n你成功回復了神智，拍打著臉加讓自己有幹勁繼續探索。(調查點+{2})'.format(against, limit, (textChange - 1))
                                else:
                                    HP = HP - 2
                                    text = '沼澤的毒氣模糊著你的心智，你感覺像要被拉到另一個世界。\n(POW抵抗4倍: {0}/{1} 失敗)\n你因為毒氣而昏厥，醒來的時候，身上多了不明的啃咬痕跡跟莫名的不適感。(HP-2)(調查點+{2})'.format(against, limit, (textChange - 1))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==6):
                                seekP = seekP + (textChange - 1)
                                sword = 1
                                STR = STR + 4
                                text = '你在血色的泥濘裡瞥見了一處奇怪的隆起，定睛一看，那是一把燃著鮮豔紅色的長劍，劍身鋒利的彷彿能斬斷一切邪惡。\n你得到了斬邪焰劍。(STR + 4)(調查點+{0})'.format((textChange - 1))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                        elif(text=='seek' and gameBot.state=='volcano'):
                            seekP = seekP + 10;
                            text = 'Volcano seek'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(text=='status'):
                            text = '人物數值:\nSTR(力量):{0}   CON(體質):{1}\nPOW(意志):{2}   DEX(敏捷):{3}\nHP(生命上限):{4}   紅色藥水:{5}瓶'.format(STR, CON, POW, DEX, HP, aid)
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(text=='item'):
                            aid = aid - 1
                            if((HP+3)<=HPMax):
                                HP = HP + 3
                                #print("The HP is now: %d" %(HP))
                            else:
                                HP = HPMax
                                #print("The HP is fully recovered to: %d" %(HP))
                            text = '你喝下了一瓶紅色藥水，微微的辛辣綻放在你的舌尖，你感覺到一股溫暖在體內流動。\n(HP+3, 現在HP: {0})(藥水剩餘{1}瓶)'.format(HP, aid)
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        if(gameBot.state=='swamp' and seekP>=20):
                            seekP = 0;
                            gameBot.trigger('area1_clear')
                            text = '你發現了通往下一個地區的路徑。\n中繼點: 炎獄山脈\n...在這個地區蔓延的只有熾熱，還有地上遍布的熔岩跟石頭碎塊，眼前的一切彷彿都在搖晃。你並沒有放棄，繼續在這個地方尋找著通往魔王城的道路。'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        if(gameBot.state=='volcano' and seekP>=25):
                            seekP = 0;
                            gameBot.trigger('area2_clear')
                            text = '你在熔岩的縫隙發現一條道路，前面吹來了不祥的氣息。\n終戰: 魔王城\n...那個既邪惡又強大的身影佇立在你的面前，光是他的視線就快要使你窒息。但你穩住自己顫抖的雙腳，挺身而出，為了家園，也為了自己的榮譽而戰!'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        text = '接下來要採取的行動是?\n   探索(輸入 seek)\n   查看自身狀態(輸入status)\n   使用藥水(輸入item)'
                        bot.sendMessage(user_id, text);
                    sleep(0.2);
            else:
                text = '歡迎來到Izayoi的game bot!\n在這裡，你可以成為闖蕩異世界的勇者，展開屬於自己的冒險!\n輸入 start 指令以開始遊戲!'
                bot.sendMessage(user_id, text);
                #game loop
        
        sleep(0.2);

if __name__ == "__main__" :
    main()
