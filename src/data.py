commonJokers = {
    "Classic Joker": ["+4 Mult", 0, 4, 1, "common", 2, 1, 0],
    "Misprint": ["+0-23 Mult", 0, 0, 1, "common", 4, 2, 0],
    "Cavendish": ["X3 Mult 1 in 1000 chance you instantly lose"],
    "Lusty Joker": ["Played cards with Heart suit give +3 Mult when scored"],
    "Greedy Joker": ["Played cards with Diamond suit give +3 Mult when scored"],
    "Wrathful Joker": ["Played cards with Spade suit give +3 Mult when scored"],
    "Gluttonous Joker": ["Played cards with Club suit give +3 Mult when scored"],
    "Jolly Joker": ["+8 Mult if played hand contains a Pair"],
    "Zany Joker": ["+12 Mult if played hand contains a Three of a Kind"],
    "Wily Joker": ["+100 Chips if played hand contains a Three of a Kind"],
    "Droll Joker": ["+10 Mult if played hand contains a Flush"],
    "Mystic Summit": ["+15 Mult when 0 discards remaining"],
    "Trading Card": ["If first discard of round has only 1 card, destroy it"],
    "Smiley Face": ["Played face cards give +5 Mult when scored"],
    "Half Joker": ["+20 Mult if scored hand contains 3 or fewer cards"],
    "Gros Michel": ["+15 Mult, 1 in 10 chance this is destroyed each use"],
    "Even Steven": ["Played cards with even rank give +4 Mult when scored (10, 8, 6, 4, 2)"],
    "Odd Todd": ["Played cards with odd rank give +31 Chips when scored (A, 9, 7, 5, 3)"],
    "Scholar": ["Played Aces give +20 Chips and +4 Mult when scored"],
}
# name, desc, + Chips, + Mult, X Mult, rarity, cost, sell_cost, counter (scaling)

# sell_cost = math.max(1, math.floor(cost/2))

uncommonJokers = {
    "Four Fingers": ["All Flushes and Straights can be made with 4 cards"],
    "Acrobat": ["X3 Mult on final hand of round"],
    "Bloodstone": ["1 in 2 chance for played cards with Heart suit to give X1.5 Mult when scored"],
    "Arrowhead": ["Played cards with Spade suit give +50 Chips when scored"],
    "Onyx Agate": ["Played cards with Club suit give +7 Mult when scored"],
    "Fibonacci": ["Each played Ace, 2, 3, 5, or 8 gives +8 Mult when scored"],
    "Space Joker": ["1 in 2 chance to upgrade level of played poker hand"],
    "Troubadour": ["+2 hand size, -1 hand each round"],
    "Merry Andy": ["+3 discards each round, -1 hand size"],
}

rareJokers = {
    "Stuntman": ["+250 Chips, -2 hand size"],
    "The Trio": ["X3 Mult if played hand contains a Three of a Kind"],
    "The Family": ["X4 Mult if played hand contains a Four of a Kind"],
    "The Order": ["X3 Mult if played hand contains a Straight"],
    "The Tribe": ["X2 Mult if played hand contains a Flush"],
    "Brainstorm": ["Copies the ability of your first Joker"],
    "Burnt Joker": ["Upgrade the level of the first discarded poker hand each round"],
    "Triboulet": ["Played Kings and Queens each give X2 Mult when scored"],
}

'''
# altered with a lot of 1s for testing
baseCards1 = [
        "1C", "1C", "1C", "1C", "1C", "1C", "7C", "8C", "9C", "10C", "11C", "12C", "13C",
        "1C","1C","1C","1C","1C","1C","1C","1C","1C","1C"
    ]

baseCards2 = [
    "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C" # 0 - 13
]
'''
checkeredDeck = [
        "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 0 - 13
        "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S", # 14 - 26
        "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
        "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
    ]

abandonedDeck = [
        "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C",
        "1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D",
        "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H",
        "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S"
    ]

allDecks = {
    "Red Deck": "+1 discard every round",
    "Blue Deck": "+1 hand every round",
    "Abandoned Deck": "No Face Cards in your deck",
    "Checkered Deck": "Only Hearts and Spades",
    "Picky Deck": "Start with the Trading Card Joker",
    "Coal Deck": "Start with the Burnt Joker",
    "Green Deck": "Start with 3 random Common Jokers",
    "Gambler Deck": "Start with 2 random Uncommon Jokers",
    "High Roller Deck": "Start with a random Rare Joker",
    "Cobble Deck": "All Face Cards are replaced with Stone Cards (50 chips each)",
    "Erratic Deck": "All Ranks and Suits in deck are randomized",
    "Jungle Deck": "All Face Cards become Wild Cards (Counts as all Suits)"
}

chipMultTable = [
    [160, 16, 50, 3, 1],  # flush five
    [140, 14, 40, 4, 1],  # flush house
    [120, 12, 35, 3, 1],  # five of a kind
    [100, 8, 40, 4, 1],  # Straight Flush
    [60, 7, 30, 3, 1],  # four of a kind
    [40, 4, 25, 2, 1],  # full house
    [35, 4, 15, 2, 1],  # flush
    [30, 4, 30, 3, 1],  # straight
    [30, 3, 20, 2, 1],  # three of a kind
    [20, 2, 20, 1, 1],  # two pair
    [10, 2, 15, 1, 1],  # pair
    [5, 1, 10, 1, 1],  # high card
]
# chip, mult, x*lvl (chip scale), x*lvl (mult scale), lvl

def getHasHand():
    return {
        "hasFlushFive": False,
        "hasFlushHouse": False,
        "hasFiveOfAKind": False,
        "hasStraightFlush": False,
        "hasFourOfAKind": False,
        "hasFullHouse": False,
        "hasFlush": False,
        "hasStraight": False,
        "hasThreeOfAKind": False,
        "hasTwoPair": False,
        "hasPair": False
    }
