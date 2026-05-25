import random
import data

def getBaseCards():
    baseCards = []
    for suit in ["C", "D", "H", "S"]:
        for rank in range(1, 14):
            baseCards.append(str(rank) + suit)
    return baseCards

def redDeck(roundState, gameState):
    gameState.totalDiscards += 1
    roundState.currentDiscards = gameState.totalDiscards

def blueDeck(roundState, gameState):
    gameState.totalHands += 1
    roundState.currentHands = gameState.totalHands

def abandonedDeck(gameState):
    gameState.baseCards = data.abandonedDeck

def checkeredDeck(gameState):
    gameState.baseCards = data.checkeredDeck

def pickyDeck(jokerState):
    jokerState.playerJokers.append("Trading Card")
    del jokerState.commonJokers["Trading Card"]

def coalDeck(jokerState):
    jokerState.playerJokers.append("Burnt Joker")
    del jokerState.commonJokers["Burnt Joker"]

def greenDeck(jokerState):
    drawRandomJoker(jokerState.commonJokers, jokerState, 3)

def gamblerDeck(jokerState):
    drawRandomJoker(jokerState.uncommonJokers, jokerState, 2)

def highRollerDeck(jokerState):
    drawRandomJoker(jokerState.rareJokers, jokerState)

def cobbleDeck(gameState):
    for i, _ in enumerate(gameState.baseCards):
        if gameState.baseCards[i][:-1] in {"11", "12", "13"}:
            gameState.baseCards[i] = "50" + gameState.baseCards[i][-1]

def erraticDeck(gameState):
    for i, _ in enumerate(gameState.baseCards):
        rank = random.randint(1, 13)
        suit = random.choice(["S", "H", "D", "C"])
        gameState.baseCards[i] = str(rank) + suit
    gameState.baseCards = orderSuit(gameState.baseCards)

def jungleDeck(gameState):
    for i, _ in enumerate(gameState.baseCards):
        if gameState.baseCards[i][:-1] in {"11", "12", "13"}:
            gameState.baseCards[i] = gameState.baseCards[i][0] + "X"


def drawRandomJoker(pool, jokerState, count=1):
    for _ in range(count):
        key, item = random.choice(list(pool.items()))
        del pool[key]
        jokerState.playerJokers.append([key, item])

def applyDeck(selectedDeck, roundState, jokerState, gameState):
    # The integer represents which variables are required. 0 = gameState, 1 = roundState, gameState, 2 = jokerState
    deckFunctions = {
        "Red Deck": (redDeck, 1),
        "Blue Deck": (blueDeck, 1),
        "Abandoned Deck": (abandonedDeck, 0),
        "Checkered Deck": (checkeredDeck, 0),
        "Picky Deck": (pickyDeck, 2),
        "Coal Deck": (coalDeck, 2),
        "Green Deck": (greenDeck, 2),
        "Gambler Deck": (gamblerDeck, 2),
        "High Roller Deck": (highRollerDeck, 2),
        "Cobble Deck": (cobbleDeck, 0),
        "Erratic Deck": (erraticDeck, 0),
        "Jungle Deck": (jungleDeck, 0),
    }
    modifier = deckFunctions.get(selectedDeck)
    if modifier[1] == 0:
        modifier[0](gameState)
    elif modifier[1] == 1:
        modifier[0](roundState, gameState)
    else:
        modifier[0](jokerState)

# Orders the hand suit. Ordered by rank within each respective suit.
def orderSuit(hand: list) -> list:
    spades, hearts, diamonds, clubs, wildcards  = [], [], [], [], []
    for cardSuit in hand:
        match cardSuit[-1]:
            case "S":
                spades.append(cardSuit)
            case "H":
                hearts.append(cardSuit)
            case "D":
                diamonds.append(cardSuit)
            case "C":
                clubs.append(cardSuit)
            case _:
                wildcards.append(cardSuit)
    return orderRank(spades) + orderRank(hearts) + orderRank(diamonds) + orderRank(clubs) + orderRank(wildcards)

# Orders the hand by rank, keeps the suits
def orderRank(hand: list) -> list:
    # It can be done in one line with the sorted() function and a lambda function / anonymous function
    return sorted(hand, key=lambda card: int(card[:-1]))
