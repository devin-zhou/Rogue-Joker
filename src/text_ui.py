import time

from colorama import Fore, Back, Style

SPEED_0 = 0.01
SPEED_1 = 0.05
SPEED_2 = 0.075
SPEED_3 = 0.3

def printJokers(jokers, shop=False):
    for j in range(len(jokers)):
        if shop:  # Print Joker Shop items # dont need this after importing pick
            print(f"{j:<3}{jokers[j][0]:<25}{jokers[j][1][0]}")
        else:  # Print the player's jokers
            print(f"{jokers[j][0]:<25}{jokers[j][1][0]}")
        time.sleep(speed1)
        
def printHand(hand):
    for index, value in enumerate(hand):
        print(f"{index}.", end=" ")
        colorCard(value)
        print()
        time.sleep(speed2)

def colorCard(card):
    match card[-1]:
        case "H":
            print(Style.BRIGHT + Fore.RED + card, end="")
        case "D":
            print(Style.BRIGHT + Fore.YELLOW + card, end="")
        case "S":
            print(Style.BRIGHT + Fore.BLUE + card, end="")
        case "C":
            print(Style.BRIGHT + Fore.GREEN + card, end="")
        case _:  # wildcard modifier?
            print(Style.BRIGHT + Fore.MAGENTA + card, end="")
    print(Style.RESET_ALL, end="")
    
def printEquation(chip, mult, XMult=None):
    if XMult is None:
        print(
            f"{Fore.BLUE+Style.BRIGHT}{chip}{Style.RESET_ALL} * {Fore.RED+Style.BRIGHT}{mult}{Style.RESET_ALL}"
            + f" = {Style.BRIGHT}{chip * mult}"
        )
    else:
        print(
            f"{Fore.BLUE+Style.BRIGHT}{chip}{Style.RESET_ALL} * {Fore.RED+Style.BRIGHT}{mult}{Style.RESET_ALL}"
            + f" * {Fore.RED+Back.WHITE+Style.BRIGHT}{XMult}{Style.RESET_ALL} = {Style.BRIGHT}{chip * (mult * XMult)}"
        )
    print(Style.RESET_ALL, end="")

def rainbowText(text):
    colours = [
        Fore.RED,
        Fore.LIGHTRED_EX,
        Fore.YELLOW,
        Fore.GREEN,
        Fore.CYAN,
        Fore.BLUE,
        Fore.MAGENTA,
    ]

    for i, char in enumerate(str(text)):
        colour = colours[i % len(colours)]
        print(colour + Style.BRIGHT + char, end="", flush=True)
        time.sleep(speed1)

    print(Style.RESET_ALL)  # Reset color at the end
    
def printInstructions():
    print(
        """
     ____                              _       _             
    |  _ \ ___   __ _ _   _  ___      | | ___ | | _____ _ __ 
    | |_) / _ \ / _` | | | |/ _ \  _  | |/ _ \| |/ / _ \ '__|
    |  _ < (_) | (_| | |_| |  __/ | |_| | (_) |   <  __/ |   
    |_| \_\___/ \__, |\__,_|\___|  \___/ \___/|_|\_\___|_|   
                |___/                                        
                    """
    )
    time.sleep(speed3)
    slowWordPrint(
        """
    Rogue Joker is a poker roguelike where you create poker hands to earn high scores.
    Each round, you are dealt a hand of cards and can choose to play or discard up to 5 cards. 
    The rarer your poker hands are, the more chips and multipliers (mult) you'll earn to increase your score. 
    Acquire Jokers to augment your scoring potential and create unique synergies.
    """, None, SPEED_0,
    )
    time.sleep(speed3)
    slowWordPrint(
        """
    Start by selecting a deck, then choosing 3 Jokers.

    """, None, SPEED_0,
    )
    
def slowWordPrint(word, colourType, speed=speed1):
    for char in str(word):
        time.sleep(speed)
        if colourType == "chip":
            print(Fore.BLUE + Style.BRIGHT + char + Style.RESET_ALL, end="", flush=True)
        elif colourType == "mult":
            print(Fore.RED + Style.BRIGHT + char + Style.RESET_ALL, end="", flush=True)
        elif colourType == "XMult":
            print(
                Fore.RED + Back.WHITE + Style.BRIGHT + char + Style.RESET_ALL,
                end="",
                flush=True,
            )
        else:
            print(char, end="", flush=True)
    print(end=" ")

def endOfCalcPrint(chip, mult, XMult):
    time.sleep(speed2)
    print(Fore.BLUE + "\nTotal Chips:" + Style.RESET_ALL)
    slowWordPrint(chip, "chip")

    time.sleep(speed2)
    print(Fore.RED + "\nTotal Mult:" + Style.RESET_ALL)
    slowWordPrint(mult, "mult")

    time.sleep(speed2)
    print(Fore.RED + Back.WHITE + "\nTotal XMult:" + Style.RESET_ALL)
    slowWordPrint(XMult, "XMult")

    time.sleep(speed1)
    print("\nHand score ", end="")
    printEquation(chip, mult, XMult)


def mainLoopPrompt(goal, currentScore, currentHands, currentDiscards, printMode=0):
    if printMode < 1:
        print("\nEnter " + Back.BLUE + Style.BRIGHT + "P" + Style.RESET_ALL + " followed by indices to play the hand. " + Back.RED + Style.BRIGHT + "D" + Style.RESET_ALL + " for discard. E.g. p 023")
    if printMode < 2:
        print("Score to beat:", goal, "Current level score:", currentScore)
    if printMode < 3:
        print(
            f"{Fore.BLUE}Hands: {Back.BLUE}{currentHands}{Style.RESET_ALL}"
            + f"\t{Fore.RED}Discards: {Back.RED}{currentDiscards}{Style.RESET_ALL}"
        )