import random
import os
import time

'''a terminal blackjack game where 8 standard decks
are being used'''


class Card: # thank you stackoverflow I now get it 
    def __init__(self, value, suit, name):
        self.value = value
        self.suit = suit
        self.name = name

    def __str__(self): # return full card details
        return (f"{self.value}{self.suit}")

suits = ["Heart", "Diamond", "Spade", "Club"]
faceCards = ["J", "Q", "K", "A"]

deck = 8 * [Card(value, suit, str(value)) for value in range(2, 11) for suit in suits] # name = value for non face cards
deck += 8 * [Card(10, suit, name) for name in faceCards for suit in suits] # 8 standard decks, Ace value later recalculated

def shuffleDeck():
    playingDeck = []
    playingDeck += deck
    random.shuffle(playingDeck)
    return playingDeck


class Player:
    def __init__(self, value):
        self.value = value
        self.cards = []

class Hand: # hand 0 reserved for dealer
    def __init__(self, bet):
        self.cards = []
        self.bet = bet
        self.busted = False

    def storeCards(self, cards):
        self.cards.append(cards)

player = Player(100) # set starting amount
hands = []

def giveCard(playingDeck, hand):
    hand.storeCards(playingDeck[0])
    playingDeck.pop(0)
    return playingDeck



def resetCards():
    hands.clear()


def values(hand):
    value = 0
    aceCount = 0
    for card in hand.cards:
        if card.name == "A":
            aceCount += 1 # for allowing 'soft' numbers
        else:
            value += card.value

    for i in range(aceCount):
        if (value + 11) > 21:    
            value += 1
        else:
            value += 11
    
    return value


def blackJack(handNum):
    if values(hands[handNum]) == 21:
        return True
    return False

def split(handNum):
    copyCard = hands[handNum].cards[0]
    hands[handNum].cards = [hands[handNum].cards[1]]
    splitHand = Hand(hands[handNum].bet)
    player.value -= hands[handNum].bet
    splitHand.cards = [copyCard]
    hands.insert(handNum + 1, splitHand)

def dealerCards(playingDeck):
    global hands
    dealerHand = Hand(0) # the house is balling but not that much
    for i in range(2): # creating dealer starting hand
        playingDeck = giveCard(playingDeck, dealerHand)    

    hands.append(dealerHand)
    return playingDeck

def playerCards(playingDeck, bet):
    global hands
    playerHand = Hand(bet)
    for i in range(2): # creating dealer starting hand
        playingDeck = giveCard(playingDeck, playerHand)    

    hands.append(playerHand)
    return playingDeck

def clear():
    os.system("cls")

def scoreboard(final, handNum):
    clear()
    bet = hands[handNum].bet
    string = ""
    string += f"Oveall Amount {int(player.value)}\n"
    string += f"Current Bet: {int(bet)}\n" # make to the hand later
    if final:
        string += f"Dealer: {[card.name + card.suit[:1] for card in hands[0].cards]} --> {values(hands[0])}\n"
    elif hands[0].cards[0].name == "A":
        string += f"Dealer: ['{hands[0].cards[0].name + hands[0].cards[0].suit[:1]}', '??'] --> 11\n\n" # ace first edge case
    else:
        string += f"Dealer: ['{hands[0].cards[0].name + hands[0].cards[0].suit[:1]}', '??'] --> {hands[0].cards[0].value}\n\n"

    for i in range(1, len(hands)):
        if i == handNum:
            string += f"Player: {[card.name + card.suit[:1] for card in hands[i].cards]} --> {values(hands[i])} <-- Playing This Hand\n"
        elif hands[i].busted:
            string += f"Player: {[card.name + card.suit[:1] for card in hands[i].cards]} --> {values(hands[i])} (BUSTED)\n"
        else:
            string += f"Player: {[card.name + card.suit[:1] for card in hands[i].cards]} --> {values(hands[i])}\n"

    
    print(string)
    
def zzz():
    time.sleep(2) # How long to sleep

def game():
    playingDeck = shuffleDeck()
    player.value = 100

    while player.value > 0:
        resetCards()

        if len(playingDeck) <= 250: # reshuffles deck at 40% deck used point
            playingDeck = shuffleDeck()

        playingDeck = dealerCards(playingDeck) # gives dealer first two cards


        while True: # handles bets w exceptions
            clear()
            try:
                bet = int(input(f"You currently have ${player.value}\nHow much would you like to bet?\n"))
                if bet <= player.value:
                    player.value -= bet
                    playingDeck = playerCards(playingDeck, bet) # starting hand

                    if player.value > 0:
                        choice = input("Would you like to bet on multiple hands, Yes(Y) or press any other key\n").lower()
                        if choice == "y":
                            continue

                    break
                else:
                    print("Overbet, you can't afford that")
            except Exception:
                print("Please type a valid integer")
                zzz()


        insurancePool = 0
        totalProfit = 0
        handNum = 0
        while handNum + 1 < len(hands):
            handNum += 1
            bet = hands[handNum].bet


            if hands[0].cards[0].name == "A" and handNum == 1: # insurance / push check with BJ
                for i in range(1, len(hands)): # handles insurance per hand
                    scoreboard(False, i)
                    choice = input(f"Dealer shows an Ace, would you like to buy insurance for this hand?\nRate: ${int(hands[i].bet/2)} --> ${int(hands[i].bet + hands[i].bet/2)} if BJ shows\nYes(Y) or No(N)\n").lower()
                    if choice == "y" and not blackJack(i):
                        player.value -= hands[i].bet/2
                        if blackJack(0):
                            insurancePool += int(hands[i].bet + hands[i].bet/2)
                    else:
                        if blackJack(0):
                            totalProfit -=  int(hands[i].bet)
                    
                if blackJack(0):
                    scoreboard(True, 0)
                    print(f"Dealer had a BJ!\nYou get back {int(insurancePool)} from insurance")
                    player.value += int(insurancePool)
                    zzz()
                    break
                else:
                    print("The game continues on...")
                    zzz()                     


            if blackJack(handNum):
                player.value += int(bet * 2.5)
                hands[handNum].bet = 0
                totalProfit += bet * 2.5
                scoreboard(False, handNum)
                print("You hit a blackjack!")
                zzz()
                continue

                
            while values(hands[handNum]) < 21:
                scoreboard(False, handNum)

                if hands[handNum].cards[0].value == hands[handNum].cards[1].value and len(hands[handNum].cards) == 2: # allows splitting 
                    choice = input("Hit(H), Stand(S), Double Down (D) or Split (SP)\n").lower() 
                    if choice == "sp":
                        split(handNum)
                        scoreboard(False, handNum)
                        zzz()
                        playingDeck = giveCard(playingDeck, hands[handNum])
                        scoreboard(False, handNum)
                        zzz()
                        playingDeck = giveCard(playingDeck, hands[handNum + 1])

                        continue
                    
                elif len(hands[handNum].cards) == 2: # allows for DD first turn
                    choice = input("Hit(H), Stand(S) or Double Down (D)\n").lower() 
                else: 
                    choice = input("Hit(H) or Stand(S)\n").lower()


                if choice == "d" and len(hands[handNum].cards) == 2:
                    if player.value >= bet:
                        playingDeck = giveCard(playingDeck, hands[handNum])
                        player.value -= bet
                        hands[handNum].bet *= 2
                        break
                    else:
                        print("Can't afford")
                        zzz()
                        continue

                elif choice == "h":
                    playingDeck = giveCard(playingDeck, hands[handNum])

                else:
                    break

            if values(hands[handNum]) > 21: 
                hands[handNum].busted = True # tells object the hand has busted
                scoreboard(False, handNum)
                totalProfit -= bet
                hands[handNum].bet = 0
                continue

        while values(hands[0]) < 17 and False in [busted.busted for busted in hands[1:]]: # checks if all hands are busted first | dealer's turn
            scoreboard(True, 0)
            zzz()
            playingDeck = giveCard(playingDeck, hands[0])

        for i in range(1, len(hands)):
            handNum = i
            bet = hands[handNum].bet
            if values(hands[0]) > 21:
                scoreboard(True, handNum)
                print(("Dealer busted everywhere? You win!\n"))
                player.value += (bet * 2)  
                totalProfit += bet * 2

            elif values(hands[handNum]) <= 21 and values(hands[handNum]) > values(hands[0]):
                scoreboard(True, handNum)
                print(("You beat the dealer!\n"))
                player.value += bet * 2
                totalProfit += bet * 2
                
            elif values(hands[handNum]) == values(hands[0]):
                scoreboard(True, handNum)
                print(("You tied with the dealer!\n"))
                player.value += bet
                totalProfit += bet
            else:
                scoreboard(True, handNum)
                print("You lost!\n")
                if insurancePool == 0:
                    totalProfit -= bet


            zzz()


        scoreboard(True, 0)
        print(f"Total Profit: {int(totalProfit)}")
        zzz()


game()

while True:
    print("AHAHAHHA you busted shit ass blackjack mf player")
    choice = input("Yes (Y) if you would like to try again").lower()
    if choice == "y":
        game()
    else:
        quit()
