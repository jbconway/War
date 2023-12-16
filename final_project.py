# this program checks off *(9.1,9.2,9.4,9.5)*

import numpy as np
import pandas as pd
import re
import random

# Initialize a DataFrame with player names and scores
def create_scoreboard():
    scoreboard = pd.DataFrame({'Player': ['Player 1', 'Player 2'], 'Score': [0, 0]})
    return scoreboard

def parse_card_input(card_input):
    #Parses the input string to extract the rank and suit of the card.
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    pattern = r'(\w+)\s+of\s+(\w+)'
    match = re.match(pattern, card_input)

    if match:
        rank, suit = match.groups()
        if rank.capitalize() in ranks and suit.capitalize() in suits:
            return rank.capitalize(), suit.capitalize()
        else:
            return None
    else:
        return None

# Update the score of the winner
def update_score(scoreboard, winner):
    if winner == 1:
        scoreboard.at[0, 'Score'] += 1
    elif winner == 2:
        scoreboard.at[1, 'Score'] += 1

# Print the current scoreboard
def print_scoreboard(scoreboard):
    print(scoreboard)

# save the scoreboard to a csv file
def save_scoreboard(scoreboard, fileName):
    scoreboard.to_csv(fileName, index = False) # checs off *(8.4)*

# loads in a csv scoreboard file
def load_scoreboard(fileName):
    # if the user wants to change their player's names from player1 and player2, 
    # then edit the names in the csv file being read in
    # checks off *(3.19)*
    try:
        scoreboard = pd.read_csv(fileName) #reads in csv file checks off *(8.2)*
    except FileNotFoundError:
        print("file not found, creating a new scoreboard")
        scoreboard = create_scoreboard()
    return scoreboard

# credates the deck as tuples and then a list of tuples. Then, shuffles the deck
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(rank, suit) for suit in suits for rank in ranks] #creates a list of tuples
    # checks off *(5.12)*
    random.shuffle(deck)
    return deck

# sets player's hands to an emptry list
# splits the deck into two and assigns it to a player's hand
def deal(deck):
    player1_hand = []
    player2_hand = []
    for i in range(len(deck)):
        if i % 2 == 0: #makes sure there is the same amount in each deck
            player1_hand.append(deck[i])
        else:
            player2_hand.append(deck[i])
    return player1_hand, player2_hand #returning two lists containing tuples *(5.14)*


# compares the ranks of the cards to determine what is higher/ what wins
def compare_cards(card1, card2, wildcard = None):
    if wildcard:
        if card1==wildcard:
            print(f"Player in position 1 wins with Wildcard: Rank: {wildcard[0]}, Suit: {wildcard[1]}")
            return 1
        elif card2==wildcard:
            print(f"Player in position 2 wins with Wildcard: Rank: {wildcard[0]}, Suit: {wildcard[1]}")
            return 2
        
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    if ranks.index(card1[0]) > ranks.index(card2[0]):
        return 1
    elif ranks.index(card1[0]) < ranks.index(card2[0]):
        return 2
    else:
        return 0  # This represents a tie
    
"""
Conducts a 'war' when both players draw cards of the same rank.
Each player places three cards face down and then one card face up.
The player with the higher face-up card wins all the cards.
If a player does not have enough cards for war, they lose.
"""    
def conduct_war(player1_cards, player2_cards, war_cards=None, wildcard = None ):
    if war_cards is None:
        war_cards = [] #sets to an empty list
    
    if len(player1_cards) < 4 or len(player2_cards) < 4:
        # One of the players doesn't have enough cards to conduct a war
        print("A player is out of cards, round is over!")
        return 1 if len(player2_cards) < 4 else 2 #player one wins if player 2 is out of cards and vice versa

    # Placing three cards face down
    war_cards.extend(player1_cards[:3])
    war_cards.extend(player2_cards[:3])
    del player1_cards[:3]
    del player2_cards[:3]

    # One card face up
    face_up_card1 = player1_cards.pop(0) #removes an item from a lit checks off *(5.1)*
    face_up_card2 = player2_cards.pop(0)
    war_cards.append(face_up_card1)
    war_cards.append(face_up_card2)
    print(f"WAR face up cards: Player 1: [{face_up_card1[0]} of {face_up_card1[1]}]   Player 2: [{face_up_card2[0]} of {face_up_card2[1]}]")
    print(f"Number of cards in war_cards: {len(war_cards)}.")

    winner = compare_cards(face_up_card1, face_up_card2, wildcard)
    if winner == 0:
        # It's a tie, conduct another war
        print(f"WAR Tie, Another round of War!") 
        return conduct_war(player1_cards, player2_cards, war_cards, wildcard)
    elif winner == 1:
        player1_cards.extend(war_cards)
    elif winner == 2:
        player2_cards.extend(war_cards)
    
    return winner


def main():
    test = True
    while test == True:
        intro = input("are you ready to play war? enter y/n \t")
        if intro.lower() == "n":
            exit()
        elif intro.lower() == "y": 
            try: 
                maximum_rounds = int(input("how many rounds do you want to play?"))
                if maximum_rounds > 0:
                    card_input = input("Enter a wildcard for the the game (e.g., 'Ace of Spades' or '2 of Hearts'): ")
                    wildcard = parse_card_input (card_input)
                    if(wildcard):
                        print(f"Wild Card Entered: Rank: {wildcard[0]}, Suit: {wildcard[1]}")
                    else:
                    # use a 2 of Hearts as the default wild card
                        wildcard = ('2', 'Hearts')
                        print(f"Invalid Wild Card entry. Defaulting to Wild Card Rank: {wildcard[0]}, Suit: {wildcard[1]}")
        #create two demensional array using numpy to keep track of the # of cards each player has after each round
                    card_counts = np.array([], dtype=int).reshape(0,2)
                    scoreboard = load_scoreboard("War_Scoreboard.csv")
                    deck = create_deck()
                    player1_cards, player2_cards = deal(deck)
                    round_counter = 1

    # Placeholder for the game loop
                    while player1_cards and player2_cards and round_counter <=maximum_rounds:
                        card1 = player1_cards.pop(0) # *(checks off 5.11)*
                        card2 = player2_cards.pop(0)
                        card1_value, card1_suit = card1
                        card2_value, card2_suit = card2
                        print(f"\nRound {round_counter} Play cards: Player 1: [{card1_value} of {card1_suit}]   Player 2: [{card2_value} of {card2_suit}]")

                        winner = compare_cards(card1, card2, wildcard)
                        if winner == 1:
                            player1_cards.extend([card1, card2])

                        elif winner == 2:
                            player2_cards.extend([card1, card2])

                        else:
                            print(f"\nRound {round_counter}: Going to War!")
                            # put the 2 cards already on the table into the war_cards list
                            war_cards = [card1, card2]
                            winner = conduct_war(player1_cards, player2_cards, war_cards)

                        update_score(scoreboard,winner)
                        print(f"Round {round_counter}: Player {winner} wins. ")

                        print_scoreboard(scoreboard)
                        #print(f"Current Score: Player 1: {p1_score}, Player 2: {p2_score}")
                        print(f"Player 1 has {len(player1_cards)} cards and Player 2 has {len(player2_cards)} cards.")
                        # add player's card count to the numpy array
                        round = np.array([[len(player1_cards),len(player2_cards)]])
                        card_counts = np.append(card_counts,round, axis = 0)
                        round_counter+=1
                    save_scoreboard(scoreboard,"War_Scoreboard.csv")
        # using vector computation to determine average card count of each player
        # checks of *(8.1)*
                    average_cards = np.mean(card_counts, axis=0)
                    print(f"Average cards: Player 1: {average_cards[0]}, Player 2: {average_cards[1]}")

    # *(checks off 8.3)*
                    df = pd.DataFrame(card_counts)
                    df['Player 1 > Player 2'] = df[0].shift(-1) > df[1]
                    subset = df[df["Player 1 > Player 2"] == True]
                    print("here are the hands where player 1 did better than player 2")
                    print(subset)
                    test = False
                elif maximum_rounds <=0:
                    print("please enter a valid number")
            except ValueError:
                print("please enter a valid number")
        else:
            ("please enter only y or n \t")
  



if __name__ == "__main__":
    main()