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

class Game(Machine):
    def getInV(self):
        print('get into the volcano...')
    def getInM(self):
        print('bumped into maou...')
    def getInD(self):
        print('You died...')
    def getInW(self):
        print('You win!')
states = [
    'swamp',
#    'volcano',
    {'name' : 'volcano', 'on_enter' : ['getInV']},
#    'maou',
    {'name' : 'maou', 'on_enter' : ['getInM']},
#    'dead',
    {'name' : 'dead', 'on_enter' : ['getInD']},
#    'win'
    {'name' : 'win', 'on_enter' : ['getInW']}
]

transitions = [
    ['area1_clear', 'swamp', 'volcano'],
    ['area2_clear', 'volcano', 'maou'],
    ['die', '*', 'dead'],
    ['die_maou', 'maou', 'win']
]

gameBot = Game(states = states, transitions = transitions, initial = 'swamp', title = 'Adventure State')
#print(gameBot.state)
gameBot.get_graph().draw('state_diagram.png', prog = 'dot')

def main():
    seekP = 0;
    gameActive = 0;
    gameEnd = 0;
    textChange = 0;
    against = 0;
    against2 = 0;
    limit = 0;
    sword = 0;
    shield = 0;
    plus = 0;
    resist = 0;
    maouHP = 120;
    maouHPMax = 120;
    maouAtk = 6
    maouDef = 3
    maouStart = 0;
#    maouAttk = 0;
    damage = 0;
    attack = 0;
    defend = 0;
    cd = 0;
    big = 0;
    STR = 0;
    CON = 0;
    POW = 0;
    DEX = 0;
    SIZ = 0;
    LUK = 0;
    HP = 0;
    HPMax = 0;
    aid = 0;
    noAtk = 0;
    text = 'non';
    lastMessageId = 0;
    updates = bot.getUpdates();

    if (len(updates)>0):
        lastMessageId = updates[-1]["update_id"]
    
    while(True):
        print('You can start now')
        updates = bot.getUpdates(offset=lastMessageId, timeout=1)
        updates = [update for update in updates if update["update_id"]>lastMessageId]
        for update in updates:
            if(gameEnd==1):
                break
            text = update["message"]["text"];
            msg_id = update["update_id"];
            user_id = update["message"]["from_user"]["id"]
            lastMessageId = msg_id;
            #bot.sendMessage(user_id, text);
            if(text=='start'):
                gameActive = 1;
                gameBot.set_state('swamp')
                text = '你成為了又一位的異世界勇者\n準備踏上打倒魔王的旅程...'
                bot.sendMessage(user_id, text);
                sleep(0.2);
                seekP = 0;
                STR = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
                CON = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
                POW = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
                DEX = random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)
                SIZ = random.randint(1, 6) + random.randint(1, 6) + 6
                LUK = POW * 5
                HP = int((CON + SIZ) / 2 + 1)
                HPMax = HP
                aid = 5;
                plus = 0;
                resist = 0;
                maouStart = 0;
                damage = 0;
                attack = 0;
                defend = 0;
                textChange = 0;
                against = 0;
                against2 = 0;
                limit = 0;
                sword = 0;
                shield = 0;
                cd = 0;
                big = 0;
                noAtk = 0;
                maouHP = maouHPMax
                text = '人物數值:\nSTR(力量):{0}   CON(體質):{1}\nPOW(意志):{2}   DEX(敏捷):{3}\nHP(生命):{4}   HP Max(生命上限):{5}\n紅色藥水:{6}瓶\n傷害加成(damage plus):{7}   傷害減免(damage resistance):{8}'.format(STR, CON, POW, DEX, HP, HPMax, aid, plus, resist)
                bot.sendMessage(user_id, text);
                sleep(0.2);
                text = '起始之地: 血霧沼澤\n...眼前是一片血紅，好似沸騰著的沼地，自地底湧出的魔素蠢蠢欲動，鼻腔裡充斥著血腥與惡臭，你甩甩頭，勇敢面對眼前這片未知的區域。'
                bot.sendMessage(user_id, text);
                sleep(0.2);
                text = '接下來要採取的行動是?\n   探索(輸入 seek)\n   查看自身狀態(輸入status)\n   使用藥水(輸入item)\n   離開(輸入exit)'
                bot.sendMessage(user_id, text);
                sleep(0.2);
                while(gameActive!=0 or gameActive!=2):
                    updates = bot.getUpdates(offset=lastMessageId, timeout=1)
                    updates = [update for update in updates if update["update_id"]>lastMessageId]
                    for update in updates:
                        if(gameActive==0):
                            break
                        text = update["message"]["text"];
                        msg_id = update["update_id"];
                        user_id = update["message"]["from_user"]["id"]
                        lastMessageId = msg_id;
                        if(text=='seek' and gameBot.state=='swamp'):
                            textChange = random.randint(1, (7-sword))
                            if(textChange==1 or textChange==2):
                                seekP = seekP + textChange
                                if(textChange==2):
                                    aid = aid + 1
                                    text = '你發現了一瓶紅色藥水。(紅色藥水:{0}瓶)'.format(aid)
                                    bot.sendMessage(user_id, text);
                                    sleep(0.2);
                                text = '周圍的景色像是被火燒過一般，枯木，死地，寸草不生。(調查進度+{0})'.format(textChange)
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==3 or textChange==4):
                                seekP = seekP + (textChange - 1)
                                text = '沼澤不斷地冒出血色的氣泡，你嘗試往裡面窺視，看到的卻只有無盡的汙濁。(調查進度+{0})'.format((textChange - 1))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==5):
                                seekP = seekP + (textChange - 1)
                                against = random.randint(0, 99)
                                limit = (STR*6)
                                if(limit>99):
                                    limit = 99
                                if(against<(STR*6)):
                                    STR = STR + 1
                                    text = '旁邊的刺藤纏住了你的腳踝!你嘗試掙脫:\n(STR抵抗6倍: {0}/{1} 成功)\n你成功掙脫了束縛，刺藤依舊在你背後張牙舞爪地扭動著。(STR+1)(調查進度+{2})'.format(against, limit, (textChange - 1))
                                else:
                                    HP = HP - 1
                                    text = '旁邊的刺藤纏住了你的腳踝!你嘗試掙脫:\n(STR抵抗6倍: {0}/{1} 失敗)\n你失敗了，刺藤割傷了你的皮膚。(HP-1)(調查進度+{2})'.format(against, limit, textChange)
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==6):
                                seekP = seekP + (textChange - 2)
                                against = random.randint(0, 99)
                                limit = (POW*4)
                                if(limit>99):
                                    limit = 99
                                if(against<(POW*4)):
                                    POW = POW + 1
                                    LUK = POW * 5
                                    text = '沼澤的毒氣模糊著你的心智，你感覺像要被拉到另一個世界:\n(POW抵抗4倍: {0}/{1} 成功)\n你成功回復了神智，拍打著臉加讓自己有幹勁繼續探索。(POW+1)(調查進度+{2})'.format(against, limit, (textChange - 2))
                                else:
                                    HP = HP - 2
                                    text = '沼澤的毒氣模糊著你的心智，你感覺像要被拉到另一個世界:\n(POW抵抗4倍: {0}/{1} 失敗)\n你因為毒氣而昏厥，醒來的時候，身上多了不明的啃咬痕跡跟莫名的不適感。(HP-2)(調查進度+{2})'.format(against, limit, (textChange - 1))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==7):
                                seekP = seekP + (textChange - 2)
                                sword = 1
                                plus = plus + 4
                                text = '你在血色的泥濘裡瞥見了一處奇怪的隆起，定睛一看，那是一把燃著鮮豔紅色的長劍，劍身鋒利的彷彿能斬斷一切邪惡。\n你得到了斬邪焰劍。(傷害加成+4)(調查進度+{0})'.format((textChange - 2))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                        elif(text=='seek' and gameBot.state=='volcano'):
                            textChange = random.randint(1, (7-shield))
                            if(textChange==1 or textChange==2):
                                seekP = seekP + textChange;
                                if(textChange==1):
                                    aid = aid + 1
                                    text = '你發現了一瓶紅色藥水。(紅色藥水:{0}瓶)'.format(aid)
                                    bot.sendMessage(user_id, text);
                                    sleep(0.2);
                                text = '岩壁、地板、空中，四處都是熱氣。\n猛烈的熱度侵蝕著你的精神與體力，每一步都使你汗如雨下。(調查進度+{0})'.format(textChange)
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==3):
                                seekP = seekP + textChange;
                                text = '岩漿肆無忌憚的噴發著，那份狂氣彷彿要燒盡這世界上的一切，卻又帶著些許的美麗。(調查進度+{0})'.format(textChange)
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==4):
                                seekP = seekP + (textChange - 1);
                                against = random.randint(0, 99)
                                limit = (DEX*4)
                                if(limit>99):
                                    limit = 99
                                if(against<(DEX*4)):
                                    DEX = DEX + 1
                                    text = '身旁的岩漿突然竄出了魔物!一隻熔岩獸衝向了你，你嘗試逃跑:\n(DEX抵抗4倍: {0}/{1} 成功)\n你成功逃跑了，方才的追逐讓你嚇出了一身冷汗。(DEX+1)(調查進度+{2})'.format(against, limit, (textChange - 1))
                                else:
                                    against2 = random.randint(0, 99)
                                    if(against2<LUK):
                                        HP = HP - 2
                                        text = '身旁的岩漿突然竄出了魔物!一隻熔岩獸衝向了你，你嘗試逃跑:\n(DEX抵抗4倍: {0}/{1} 失敗)\n(LUK判定: 隱藏 成功)\n你僥倖逃出了熔岩獸的魔爪，背後被抓傷的地方還熱辣辣的發疼。(HP-2)(調查進度+{2})'.format(against, limit, (textChange - 1))
                                    else:
                                        HP = HP - 4
                                        text = '身旁的岩漿突然竄出了魔物!一隻熔岩獸衝向了你，你嘗試逃跑:\n(DEX抵抗4倍: {0}/{1} 失敗)\n(LUK判定: 隱藏 失敗)\n你在慌亂之中絆到了自己的腳，熔岩獸朝你吐出了滾燙的火球，你在岩地上痛苦的打滾，費了好大的勁才把身上的火撲滅。(HP-4)(調查進度+{2})'.format(against, limit, (textChange - 1))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==5):
                                seekP = seekP + (textChange - 1);
                                against = random.randint(0, 99)
                                limit = (CON*4)
                                if(limit>99):
                                    limit = 99
                                if(against<(CON*4)):
                                    CON = CON + 1
                                    text = '一陣恐怖的熱浪襲來，身體猶如被燒灼一般，你試圖抵抗這強烈的不適:\n(CON抵抗4倍: {0}/{1} 成功)\n你從暈眩跟反胃感中穩了住腳，將水灑在身上，讓熱量隨著水分蒸發而去。(CON+1)(調查進度+{2})'.format(against, limit, (textChange - 1))
                                else:
                                    HP = HP - 2
                                    text = '一陣恐怖的熱浪襲來，身體猶如被燒灼一般，你試圖抵抗這強烈的不適:\n(CON抵抗4倍: {0}/{1} 失敗)\n你忍受不住這陣熱浪的侵襲，倒在了地上，回過神來，面前是自己些許的嘔吐物，身上還殘留著些許熱汗。(HP-2)(調查進度+{2})'.format(against, limit, (textChange - 1))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==6):
                                seekP = seekP + (textChange - 2);
                                against = random.randint(0, 99)
                                limit = LUK
                                if(limit>99):
                                    limit = 99
                                if(against<LUK):
                                    HP = HP + 1
                                    HPMax = HPMax + 1
                                    STR = STR + 1
                                    CON = CON + 1
                                    POW = POW + 1
                                    DEX = DEX + 1
                                    LUK = POW * 5
                                    text = '你似乎感覺到背後有什麼動靜，猛然的轉過身:\n(LUK判定: 隱藏 成功)\n你發現了一本掉在地上的魔法書，裡面記載的是失傳的身體強化魔法。(全屬性+1)(調查進度+{0})'.format((textChange - 2))
                                else:
                                    POW = POW - 1
                                    text = '你似乎感覺到背後有什麼動靜，猛然的轉過身:\n(LUK判定: 隱藏 失敗)你發現了岩漿不斷從你的背後湧出!你趕緊逃離這裡，一邊感嘆著自己的不運。(POW-1)(調查進度+{0})'.format((textChange - 2))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            elif(textChange==7):
                                seekP = seekP + (textChange - 2);
                                shield = 1;
                                resist = 3;
                                text = '在火山岩的黑暗縫隙中，你注意到有個物體正在閃爍著，是一面純銀的鳶型盾，那聖潔的光芒彷彿能隔絕一切邪惡之物。\n你得到了輝銀聖盾(傷害減免+3)(調查進度+{0})'.format((textChange - 1))
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                        elif(text=='attack' and gameBot.state=='maou'):
                            #player's turn
                            against = random.randint(0, 99)
                            if(against<LUK):
                                attack = random.randint(1, 3)
                                damage = STR + attack + plus - maouDef
                                text = '你向魔王揮出了劍!劍身確實的砍進的魔王的身軀，黑紫色的血從傷口噴湧而出，濺上了你的盔甲。(對魔王造成{0}點傷害)'.format(damage)
                            else:
                                damage = STR + plus - maouDef
                                text = '你向魔王揮出了劍!然而劍身掠過了魔王的身軀，只在空中劃出一道弧形的血痕。(對魔王造成{0}點傷害)'.format(damage)
                            maouHP = maouHP - damage
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(text=='defend' and gameBot.state=='maou'):
                            #player's turn
                            defend = random.randint(1, 3)
                            text = '你舉起了盾，架起了防禦態勢!(下次遭到魔王攻擊的傷害減少{0}點)'.format(defend)
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(text=='skill' and gameBot.state=='maou'):
                            #player's turn
                            if(cd!=0):
                                noAtk = 1
                                text = '技能冷卻尚未結束，無法使用!'
                            else:
                                damage = (STR + plus - maouDef) * 2
                                text = '你使用了\"全力一擊\"!對魔王造成了兩倍的攻擊傷害!(造成{0}點傷害)'.format(damage)
                                maouHP = maouHP - damage
                                cd = cd + 3
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(text=='status'):
                            if(gameBot.state=='maou'):
                                noAtk = 1
                            text = '人物數值:\nSTR(力量):{0}   CON(體質):{1}\nPOW(意志):{2}   DEX(敏捷):{3}\nHP(生命):{4}   HP Max(生命上限):{5}\n紅色藥水:{6}瓶\n傷害加成(damage plus):{7}   傷害減免(damage resistance):{8}'.format(STR, CON, POW, DEX, HP, HPMax, aid, plus, resist)
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(text=='item'):
                            aid = aid - 1
                            if((HP+3)<=HPMax):
                                HP = HP + 3
                            else:
                                HP = HPMax
                            text = '你喝下了一瓶紅色藥水，微微的辛辣與苦澀綻放在你的舌尖，你感覺到一股溫暖在體內流動，傷口也稍微癒合了。\n(HP+3, 現在HP: {0} 最大值: {1})(藥水剩餘{2}瓶)'.format(HP, HPMax, aid)
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(text=='exit'):
                            if(maouStart==0):
                                gameActive = 0;
                                gameEnd = 1;
                                text = '你選擇離開冒險，踏上歸途。'
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                            else:
                                noAtk = 1
                                text = '...都已經來到這裡了，怎麼能夠輕易退卻!\n你咬緊牙關，抹消逃跑的念頭，繼續奮戰。'
                                bot.sendMessage(user_id, text);
                                sleep(0.2);
                        elif(text=='hurt'):
                            HP = HP - 20
                            text = 'hurt!'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(text=='video'):
                            text = 'https://www.youtube.com/watch?v=epfPe2U_2Xk'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        else:
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                            textChange = random.randint(1, 3)
                            if(gameBot.state=='maou'):
                                noAtk = 1
                                if(textChange==1):
                                    text = '在戰鬥中，有一個這樣的聲音在你的心中響起，讓你稍微忘卻了恐懼，認真面對眼前的強敵!'
                                elif(textChange==2):
                                    text = '你喃喃念著這樣的一句話，彷彿它也是一句咒文，能夠讓你獲得力量。'
                                else:
                                    text = '汗不斷的落在地上，你握著劍的手依然微微顫抖著，不知哪裡傳來的這陣聲音，讓你微微感到心安。'
                            else:
                                if(textChange==1):
                                    text = '你喃喃唸道，坐在原地休息，環顧著四周荒蕪的景色，心中湧起了一陣淒涼，但這也化作驅使你前進的動力。'
                                elif(textChange==2):
                                    text = '你向這片大地吶喊，然而它卻沒給你任何回應，這世界彷彿只有你與這一片死寂。'
                                else:
                                    text = '你的心中響起了這樣一道聲音，你不知道它到底從哪裡來。也許，是這個世界在嘗試與你對話吧。'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        if(maouStart==1 and noAtk==0 and maouHP>0):
                            #maou's turn
                            textChange = random.randint(1, 4)
                            if(big==1):
                                big = 0
                                HP = HP - (maouAtk - resist - defend + 2)
                                defend = 0
                                text = '魔王將手中聚集的魔素全部放出，魔力的奔流將你吞噬!(你受到了{0}點傷害)'.format((maouAtk - resist - defend + 2))
                            elif(textChange==1):
                                HP = HP - (maouAtk - resist - defend)
                                text = '魔王手中的黑光綻裂，射向了你!(你受到了{0}點傷害)'.format((maouAtk - resist - defend))
                                defend = 0
                            elif(textChange==2):
                                if(big==0):
                                    big = 1
                                    text = '魔王露出了戲謔的笑容，開始詠唱咒語，龐大的魔素在他面前濃縮。(下一次魔王的傷害提高1.5倍)'
                            elif(textChange==3):
                                HP = HP - (maouAtk - resist - defend - 1)
                                defend = 0
                                text = '魔王手中的魔素化作箭矢，射向了你!(你受到了{0}點傷害)'.format((maouAtk - resist - defend - 1))
                            elif(textChange==4):
                                against = random.randint(1, 2)
                                if(against==1):
                                    text = '魔王狂笑著，彷彿在恥笑你是個天大的笑話。(沒有動作)'
                                else:
                                    text = '魔王靜靜的睥睨著你，彷彿你在他眼中，只是一顆沙粒不過的存在。(沒有動作)'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        if(gameBot.state=='swamp' and seekP>=17):
                            seekP = 0;
                            gameBot.trigger('area1_clear')
                            text = '你發現了通往下一個地區的路徑。\n中繼點: 炎獄山脈\n...在這個地區蔓延的只有熾熱，還有地上遍布的熔岩跟石頭碎塊，眼前的一切彷彿都在搖晃。你並沒有放棄，繼續在這個地方尋找著通往魔王城的道路。'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(gameBot.state=='volcano' and seekP>=22):
                            seekP = 0;
                            maouStart = 1;
                            gameBot.trigger('area2_clear')
                            text = '你在熔岩的縫隙發現一條道路，前面吹來了不祥的氣息。\n終戰: 魔王城\n...那個既邪惡又強大的身影佇立在你的面前，光是他的視線就快要使你窒息。但你穩住自己顫抖的雙腳，挺身而出，為了家園，也為了自己的榮譽而戰!'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                            text = '\"哼!看看是誰來了?余只看到又一個既無知又可笑，前來送死的螻蟻啊!\"\n魔王以極度輕蔑的眼神與口吻，緩緩的瞥向了你，你不由得感到渾身顫慄。\n魔王緩緩向你踏出了一步，\"...余也正好興致高漲，就陪汝玩玩吧!\"'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                        elif(HP<=0):
                            seekP = 0;
                            gameBot.trigger('die')
                            text = '......你清楚的認識到自己的無力與渺小，但是，已經太遲了，隨之而來的是與地面的碰撞感，你漸漸地失去知覺。\n你的意識開始遠去\n慢慢沉入\n無盡的\n黑暗\n中\n.\n.\n.'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                            gameActive = 0
                            gameEnd = 1
                        elif(maouHP<=0):
                            seekP = 0;
                            gameBot.trigger('die_maou')
                            text = '魔王露出了滿意的微笑，\"真是場不錯的戰鬥啊...冒險者....\"\n他的軀體化作灰燼，在一陣又一陣風的吹拂下，消失無蹤。\n你將劍插在地面上，仰天長嘯，你知道這是只屬於你的勝利!\n\n----但是，冒險者與魔王之間，終究存在著宿命，你明白，在你的冒險結束後，又會有新的魔王誕生......'
                            bot.sendMessage(user_id, text);
                            sleep(0.2);
                            gameActive = 0
                            gameEnd = 1
                        if(gameActive==1):
                            if(gameBot.state=='maou'):
                                if(cd>0):
                                    cd = cd -1
                                noAtk = 0
                                text = '魔王HP: {0}/{1}\n\n接下來要採取的行動是?\n   攻擊(輸入 attack)\n   防禦(輸入 defend)\n   使用技能(輸入 skill)\n   查看自身狀態(輸入status)\n   使用藥水(輸入item)\n\n你的HP: {2}/{3}\n\"全力一擊\" cd:{4}'.format(maouHP, maouHPMax, HP, HPMax, cd)
                                bot.sendMessage(user_id, text);
                            else:
                                text = '接下來要採取的行動是?\n   探索(輸入 seek)\n   查看自身狀態(輸入status)\n   使用藥水(輸入item)\n   離開(輸入exit)'
                                bot.sendMessage(user_id, text);
                    if(gameActive==0):
                        break
                    sleep(0.2);
            else:
                text = '歡迎來到Izayoi的game bot!\n在這裡，你可以成為闖蕩異世界的勇者，展開屬於自己的冒險!\n輸入 start 指令以開始遊戲!'
                bot.sendMessage(user_id, text);
        gameEnd = 0;
        sleep(0.2);

if __name__ == "__main__" :
    main()
