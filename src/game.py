import random
import sys
import time


import data
import deck_functions as df
import hand_functions as hf
import helper_functions as hp
import joker_functions as jf
import states
import text_ui as ui

DEBUG_MODE = 0

FAST_MODE = False
speeds = [0.01, 0.05, 0.075, 0.3, 0.5, 0.75, 1] #seconds

if FAST_MODE:
    speeds = [0, 0, 0, 0]



def mainLoopPlay(rs1, js1, gs1, selectedIndicesSet, hand, deck, discardPile):
    rs1.currentHands -= 1
    playedHand = [card for i, card in enumerate(hand) if i in selectedIndicesSet]
    # SORTS the inputted hand before evaluating
    playedHand = df.orderRank(playedHand)
    print("You played:", playedHand)
    # notHighCard lets us know if it's a multi card hand thats being scored
    notHighCard, partialHandIndices, rs1.hasHand = hf.evalHand(playedHand, rs1.hasHand, js1.fourFingers)

    chip, mult, XMult, scoredCards = scoreHand(playedHand,partialHandIndices,notHighCard,js1.fourFingers,gs1.chipMultTable,rs1)
    time.sleep(speeds[3])
    ui.printEquation(chip, mult)
    time.sleep(speeds[3])
    print("Scored cards:", scoredCards)

    chip, mult, XMult = jf.jokerCalculation([chip,mult,XMult], js1.playerJokers, scoredCards, rs1, gs1)
    XMult = XMult - 1
    XMult = 1 if XMult <= 0 or XMult is None else XMult

    ui.endOfCalcPrint(chip, mult, XMult)

    rs1.score += round(chip * (mult * XMult))
    ui.slowPrint("Total Level Score:", speed = speeds[2])
    time.sleep(speeds[4])

    if rs1.score > gs1.getCurrentScoreRequired():
        ui.rainbowText(rs1.score)
    else:
        ui.slowPrint(rs1.score, speed = speeds[2])
    time.sleep(speeds[4])
    print()
    print()

    # Resets playedHand
    keptCards = [card for card in hand if card not in playedHand]
    hand, deck = hf.drawCards(keptCards, deck, gs1.totalValues[0])
    discardPile = discardPile + playedHand

    return hand, deck, discardPile



def scoreHand(hand, partialHandIndices, notHighCard, fourFingers, chipMultTable, rs1) -> tuple:
    newPartialHand, highestHandName = None, None
    hasHand = rs1.hasHand

    if notHighCard:
        highestHandName = hp.findHighestHandName(hasHand)
        ui.magPrint(highestHandName[3:].upper())
    else:  # high card
        highestHandName = "hasHighHand"
        ui.magPrint("High Card")

    # Check if the hand we're scoring is a partial hand or not
    partialHands = {
        "hasFourOfAKind": 7,
        "hasThreeOfAKind": 3,
        "hasTwoPair": 2,
        "hasPair": 1,
        "hasHighHand": 0,
    }
    if fourFingers == 4:
        partialHands["hasFlush"] = 5
        partialHands["hasStraight"] = 4

    if highestHandName in partialHands:
        # Feed the correct partialHandIndices index and score the respective hand indices
        indices = partialHandIndices[partialHands[highestHandName]]
        newPartialHand = [card for i, card in enumerate(hand) if i in indices]

    filteredHand = hand if newPartialHand is None else newPartialHand

    highestHandIndex = (
        11 if highestHandName == "hasHighHand" else hp.handNameToIndex(highestHandName, hasHand)
    )

    chip, mult = hp.calculateChipMult(hp.countChips(filteredHand), highestHandIndex, chipMultTable)
    return chip, mult, 1, filteredHand



def main(playerJokers = None, setSeed = None):
    random.seed(setSeed)

    # prevent dangerous-default-value
    if playerJokers is None:
        playerJokers = []

    discardPile = []
    printMode = (0, 1, 2)
    hand, deck = None, None

    gs1 = states.GameState(baseCards = df.getBaseCards())
    gs1.getChipMultTable()
    rs1 = states.RoundState(currentHands = gs1.totalValues[1], currentDiscards = gs1.totalValues[2], hasHand = data.getHasHand())
    js1 = states.JokerState(playerJokers)

    hp.clearConsole()

    # deck selection
    if not FAST_MODE:
        ui.printInstructions()
        gs1.selectedDeck = df.deckSelection(data.allDecks)
    else:
        gs1.selectedDeck = "Checkered Deck"

    # apply new deck
    df.applyDeck(gs1.selectedDeck, js1, gs1)

    # Joker Selection from joker shop
    js1.initJokerPool()
    if not FAST_MODE:
        # insert deck dependency here
        #
        jf.jokerSelection(js1)
    else:
        js1.playerJokers = [["Classic Joker","a"], ["Four Fingers","a"], ["Burnt Joker","a"],
                            ["Lusty Joker","a"],["Bloodstone","a"], ["Trading Card","a"],
                            ["Brainstorm","a"], ["Space Joker","a"]]

    time.sleep(speeds[3])

    # Per game Loop
    while gs1.currentLevel < len(gs1.requiredScores):
        jf.jokerDeckApplication(js1, gs1, rs1)  # Apply jokers that affect deck, hand

        # to do todo put deck and hand into a state object

        if discardPile : # Check if not first loop of game, mix discard pile with remaining deck and hand
            gs1.baseCards = deck + discardPile + hand
        handWithDeck = hf.generateHand(gs1.totalValues[0], gs1.baseCards)
        hand, deck = df.orderRank(handWithDeck[0]), handWithDeck[1]

        # Per level Loop
        currentRequiredScore = gs1.getCurrentScoreRequired()
        print("--- LEVEL", gs1.currentLevel + 1, "---")  # +1 for 0 index
        print("Score Required:", currentRequiredScore)
        while rs1.score < currentRequiredScore:
            # Check for lose condition (out of hands)
            if rs1.currentHands <= 0 and rs1.score < currentRequiredScore:
                print(rs1.score, "is less than", currentRequiredScore, "\nGame Over")
                sys.exit(0)

            # Reset round values
            rs1.resetScoringValues(True)
            # Reset hasHand
            rs1.hasHand = data.getHasHand()

            ui.mainLoopPrompt(currentRequiredScore, rs1, printMode)
            printMode = (2,) # The comma is needed to make it a tuple with one element
            ui.printHand(hand)
            print("Deck Length:", len(deck))

            userInput = input()
            userInputAction = userInput[0].lower()
            userInputCardIndex = userInput[1:].strip()
            selectedIndicesSet = {int(x) for x in userInputCardIndex}

            # Limit hand / discard size
            if len(selectedIndicesSet) > 5:
                print("Error: selected too many cards")
                ui.mainLoopPrompt(currentRequiredScore, rs1, (0,))
                continue

            # DISCARD
            if userInputAction == "d" and rs1.currentDiscards > 0:
                rs1.currentDiscards -= 1 # Used up a discard

                # Removes cards from the hand based on indices
                keptCards, discarded = [], []
                for index, card in enumerate(hand):
                    if index not in selectedIndicesSet:
                        keptCards.append(card)
                    else:
                        discarded.append(card)

                # Trading Card and Burnt Joker
                firstDiscard = gs1.totalValues[2] == rs1.currentDiscards + 1
                foundTradingCard = hp.findJoker("Trading Card", js1.playerJokers)
                foundBurntJoker = hp.findJoker("Burnt Joker", js1.playerJokers)

                if firstDiscard and foundTradingCard and len(discarded) == 1:
                    # Trading Card prevents the discarded card from entering the discardPile, thus removing it from the deck
                    ui.slowPrint("Trading Card: " + str(discarded[0]) + " removed from deck", speed = speeds[1])
                    print()
                else:
                    discardPile = discardPile + discarded

                if foundBurntJoker and firstDiscard:
                    tempHasHand = data.getHasHand()
                    foundMultiCardHand, _, foundHands = hf.evalHand(discarded, tempHasHand, js1.fourFingers)

                    if foundMultiCardHand:
                        upgradeName = hp.findHighestHandName(foundHands)
                        upgradeIndex = hp.handNameToIndex(upgradeName, tempHasHand)
                    else:
                        upgradeName = "hasHighHand"
                        upgradeIndex = 11

                    newLvl = gs1.increaseHandLevel(upgradeIndex)
                    ui.slowPrint("Burnt Joker: " + upgradeName[3::] + " level increased from "
                                 + str(newLvl - 1) + " -> " + str(newLvl), speed = speeds[1])
                    print()

                hand = keptCards
                hand, deck = hf.drawCards(hand, deck, gs1.totalValues[0])

            # PLAY
            elif userInputAction == "p":
                hand, deck, discardPile = mainLoopPlay(rs1, js1, gs1, selectedIndicesSet, hand, deck, discardPile)

            # Out of Discards
            elif userInputAction == "d" and rs1.currentDiscards == 0:
                print("Error: Out of Discards. Try Again")
                time.sleep(speeds[3])
                continue

            # HELP
            elif userInputAction == "?":
                print('"q" to quit\n"c" to clear text\n"j" to view jokers\n"v" to view deck')
                time.sleep(speeds[3])

            # QUIT
            elif userInputAction == "q":
                sys.exit(0)

            # CLEAR
            elif userInputAction == "c":
                hp.clearConsole()

            # SHOW JOKERS
            elif userInputAction == "j":
                ui.printJokers(js1.playerJokers)
                time.sleep(speeds[3])

            # SHOW chip mult table
            elif userInputAction == "t":
                print(gs1.chipMultTable)
                time.sleep(speeds[3])

            # VIEW DECK
            elif userInputAction == "v":
                # Temp variable to prevent changing deck order
                remainingDeckTemp = df.orderSuit(deck)
                ui.printDeck(gs1.baseCards, remainingDeckTemp)
                time.sleep(speeds[3])

            else:
                hp.clearConsole()
                print("Error: Try Again")
                time.sleep(speeds[1])

        # Beat the current level
        if rs1.score > currentRequiredScore:
            print(rs1.score, "is greater than", currentRequiredScore)
            # Reset variables for next level
            gs1.currentLevel += 1
            print("Press enter to continue")
            input()
            time.sleep(speeds[3])
            if gs1.currentLevel != len(gs1.requiredScores):
                jf.jokerSelection(js1)
                foundFourFingers = hp.findJoker("Four Fingers", js1.playerJokers)
                if foundFourFingers:
                    js1.updateFourFingers()

    print("--- You win ---")


if __name__ == "__main__":
    # Can force jokers from command line argument for testing, format should be a list of joker names (e.g. ["Stuntman", "Cavendish"])
    forcedJoker = sys.argv[1] if len(sys.argv) > 1 else None
    forcedSeed = sys.argv[2] if len(sys.argv) > 2 else None
    #main(forcedJoker, "c") # demo seed
