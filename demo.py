import sys

import telegram
import pygraphviz
from flask import Flask, request
from time import sleep
from transitions import State
from transitions.extensions import GraphMachine as Machine
import random

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

class Game(object):
    pass

gameBot = Game()
machine = Machine(model = gameBot, states = states, transitions = transitions, initial = 'swamp')
print(gameBot.state)

def main():
    seekP = 0;
    gameActive = 1;
    STR = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    CON = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    POW = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    DEX = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    SIZ = random.randint(0, 6) + random.randint(0, 6) + 6
    INT = random.randint(0, 6) + random.randint(0, 6) + 6
    LUK = POW * 5
    HP = (CON + SIZ) / 2
    HPMax = HP
    
    while(gameActive!=0):
        command = input("Command: ")
        if(command=="start"): #game loop
            print("Game started!")
            while(HP>0):
                command = input("Command(seek/item/hurt): ")
                if(command=='seek'):
                    searchCon = "You searched the %s for a while." %(gameBot.state)
                    print(searchCon)
                    seekP = seek + 5
                    if(seekP>=20 and gameBot.state=='swamp'):
                        gameBot.trigger('area1_clear')
                    elif(seekP>=20 and gameBot.state=='volcano'):
                        gameBot.trigger('area2_clear')
                elif(command=='item'):
                    print("Drank the red aid.")
                    if((HP+2)<=HPMax):
                        HP = HP + 2
                    else:
                        HP = HPMax
                    print("The HP now is: %d" %(HP))
                elif(command=='hurt'):
                    print("Hurt!.")
                    HP = HP - 4
                    if(HP<=0):
                        gameActive = 0;                        
                else:
                    print("Wrong command.")
        else:
            print("Game idled.")

    print("Game ended.")

if __name__ == "__main__" :
    main()
