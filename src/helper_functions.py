import random

#from games
#removeSuits()

def getRandomIndices(deck, k) -> list:
    return random.sample(range(len(deck)), k)

def findJoker(jokerName, jokerList) -> bool:
    for joker in jokerList:
        if joker[0] == jokerName:
            return True
    return False

#from deck_functions
#orderSuit
#orderRank


def fixDiscardPile(discardPile) -> list:
    # 
    fixedDiscardPile = []
    for hand in discardPile:
        for card in hand:
            fixedDiscardPile.append(card)
    return fixedDiscardPile