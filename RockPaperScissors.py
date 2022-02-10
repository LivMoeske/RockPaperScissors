# Add your Python code here. E.g.

from microbit import *
import random
import radio
 

radio.on()
#skrur på radio

ROCK_IMAGE = Image("00000:06760:64246:98489:28981")
PAPER_IMAGE = Image("00260:05791:78998:29860:06100")
SCISSORS_IMAGE = Image("57509:70790:07900:70790:57509")
#de forskjellige bildene som blir brukt i RPS

ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

RPS_DICTIONARY = {
    ROCK : ROCK_IMAGE,
    PAPER : PAPER_IMAGE,
    SCISSORS : SCISSORS_IMAGE
    }
#en dictionary gjør det enklere å forbinde f.eks. bilder med variabler
    
RPS_LIST = [ROCK, PAPER, SCISSORS]
sentRPS = ""
#hva denne spilleren har sendt
receivedRPS = ""
#hva den andre spilleren har sendt
wins = 0
losses = 0

def CreateAndSendRandomChoice():
    randomRPS = random.choice(RPS_LIST)
    radio.send(randomRPS)
    return randomRPS
    #en funksjon som velger og sender et tilfeldig utvalg av rock paper scissors
    
def Arbitrate(sent, received):
    global wins
    global losses
    if sent == received:
        display.show(Image.CONFUSED)
        return
    if (sent == ROCK and received == SCISSORS) or (sent == SCISSORS and received == PAPER) or (sent == PAPER and received == ROCK):
        wins += 1
        display.show(Image.HAPPY)
        return
    losses += 1
    display.show(Image.SAD)
    #en funksjon som regner ut om spilleren har vunnet eller tapt
    
def DisplayScore():
    display.scroll(str(wins) + "-" + str(losses))
    #en funksjon som viser de nåtidige poengsummene

    
while True:
    if button_a.was_pressed():
        sentRPS = CreateAndSendRandomChoice() #gjør det tilfeldige valget om til sentRPS
    receivedRPS = radio.receive()
    if receivedRPS: #hvis den får et signal fra den andre
        if sentRPS == "": #og sentRPS er tom
            sentRPS = CreateAndSendRandomChoice() #lager det et tilfeldig utvalg
        display.show(RPS_DICTIONARY[sentRPS]) 
        #velger sentRPS fra RPS_DICTIONARY, dvs. det tar bildet som hører til valget til spilleren
        sleep(1500)
        #viser hva den selv sendte
        display.show(RPS_DICTIONARY[receivedRPS]) 
        #velger receivedRPS fra RPS_DICTIONARY, dvs. det tar bildet som hører til valget til motstanderen
        sleep(1500)
        #viser hva motstanderen sendte
        Arbitrate(sentRPS, receivedRPS)
        sleep(1000)
        #regner ut hvem som vant
        DisplayScore()
        sentRPS = "" #sentRPS blir tom igjen
    if button_b.was_pressed():
        wins = 0
        losses = 0
        DisplayScore()
        #dette tilbakestiller poengsummen (for denne spilleren)

