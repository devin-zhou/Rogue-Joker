import time

from colorama import Fore, Back, Style

speeds = [0.01, 0.05, 0.075, 0.3]

def printJokers(jokers, shop=False):
    for j, joker in enumerate(jokers):
        if shop:  # Print Joker Shop items # dont need this after importing pick
            print(f"{j:<3}{joker[0]:<25}{joker[1][0]}")
        else:  # Print the player's jokers
            print(f"{joker[0]:<25}{joker[1][0]}")
        time.sleep(speeds[1])

def printDeck(baseCards, remainingDeck):
    print("Base Cards:", len(baseCards))
    for card in baseCards:
        colorCard(card)
        print(end=" ")
    print("\nRemaining Deck:", len(remainingDeck))
    for card in remainingDeck:
        colorCard(card)
        print(end=" ")
    print()

def printHand(hand):
    for index, value in enumerate(hand):
        print(f"{index}.", end=" ")
        colorCard(value)
        print()
        time.sleep(speeds[2])

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
        case "X":  # wildcard
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
        time.sleep(speeds[2])

    print(Style.RESET_ALL)  # Reset color at the end


def slowPrint(word, colourType = None, speed=speeds[1]):
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


def printInstructions():
    # Disable all the anomalous-backslash-in-string violations in this function
    # pylint: disable=anomalous-backslash-in-string
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
    time.sleep(speeds[3])
    slowPrint(
        """
    Rogue Joker is a poker roguelike where you create poker hands to earn high scores.
    Each round, you are dealt a hand of cards and can choose to play or discard up to 5 cards. 
    The rarer your poker hands are, the more chips and multipliers (mult) you'll earn to increase your score. 
    Acquire Jokers to augment your scoring potential and create unique synergies.
    """, None, speeds[0],
    )
    time.sleep(speeds[3])
    slowPrint(
        """
    Start by selecting a deck, then choosing 3 Jokers. Press enter to start.

    """, None, speeds[0],
    )
    input()
    # pylint: enable=anomalous-backslash-in-string


def endOfCalcPrint(chip, mult, XMult):
    time.sleep(speeds[3])
    print(Fore.BLUE + "\nTotal Chips:" + Style.RESET_ALL)
    slowPrint(chip, "chip")

    time.sleep(speeds[3])
    print(Fore.RED + "\nTotal Mult:" + Style.RESET_ALL)
    slowPrint(mult, "mult")

    time.sleep(speeds[3])
    print(Fore.RED + Back.WHITE + "\nTotal XMult:" + Style.RESET_ALL)
    slowPrint(XMult, "XMult")

    time.sleep(speeds[3])
    print("\nHand score ", end="")
    printEquation(chip, mult, XMult)

def mainLoopPrompt(goal, rs1, printMode=(0,)):
    if 0 in printMode:
        print("\nEnter " + Back.BLUE + Style.BRIGHT + "P" + Style.RESET_ALL + " followed by indices (max of 5) to play the hand. "
              + Back.RED + Style.BRIGHT + "D" + Style.RESET_ALL + " for discard. E.g. p 023")
        print("Enter " + Back.YELLOW + Style.BRIGHT + "?" + Style.RESET_ALL + " for instructions. ")
    if 1 in printMode:
        print("Score to beat:", goal, "Current level score:", rs1.score)
    if 2 in printMode:
        print(
            f"{Fore.BLUE}Hands: {Back.BLUE}{rs1.currentHands}{Style.RESET_ALL}"
            + f"\t{Fore.RED}Discards: {Back.RED}{rs1.currentDiscards}{Style.RESET_ALL}"
        )

def magPrint(handPrint):
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + handPrint + Style.RESET_ALL, end=" ",)
