import numpy as np
import pandas as pd
import re
import random


def create_scoreboard():
    # Initialize a DataFrame with player names and scores
    scoreboard = pd.DataFrame({'Player': ['Player 1', 'Player 2'], 'Score': [0, 0]})
    return scoreboard

def update_score(scoreboard, winner):
    # Update the score of the winner
    if winner == 1:
        scoreboard.at[0, 'Score'] += 1
    elif winner == 2:
        scoreboard.at[1, 'Score'] += 1

def print_scoreboard(scoreboard):
    # Print the current scoreboard
    print(scoreboard)

def save_scoreboard(scoreboard, fileName):
    scoreboard.to_csv(fileName, index = False)

def load_scoreboard(fileName):
    # if the user wants to change their player's names from player1 and player2, then edit the names in the csv file being read in
    #
    try:
        scoreboard = pd.read_csv(fileName)
    except FileNotFoundError:
        print("file not found, creating a new scoreboard")
        scoreboard = create_scoreboard()
    return scoreboard

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal(deck):
    player1_hand = []
    player2_hand = []

    for i in range(len(deck)):
        if i % 2 == 0:
            player1_hand.append(deck[i])
        else:
            player2_hand.append(deck[i])

    return player1_hand, player2_hand #returning two lists containing tuples *(5.14)*

# Placeholder for additional functions like compare_cards, conduct_war, play_round
def compare_cards(card1, card2):
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    if ranks.index(card1[0]) > ranks.index(card2[0]):
        return 1
    elif ranks.index(card1[0]) < ranks.index(card2[0]):
        return 2
    else:
        return 0  # This represents a tie
    

def conduct_war(player1_cards, player2_cards, war_cards=None ):
    """
    Conducts a 'war' when both players draw cards of the same rank.
    Each player places three cards face down and then one card face up.
    The player with the higher face-up card wins all the cards.
    If a player does not have enough cards for war, they lose.
    """
    if war_cards is None:
        war_cards = []
    
    if len(player1_cards) < 4 or len(player2_cards) < 4:
        # One of the players doesn't have enough cards to conduct a war
        print("A player is out of cards, round is over!")
        return 1 if len(player2_cards) < 4 else 2

    # Placing three cards face down
    war_cards.extend(player1_cards[:3])
    war_cards.extend(player2_cards[:3])
    del player1_cards[:3]
    del player2_cards[:3]

    # One card face up
    face_up_card1 = player1_cards.pop(0)
    face_up_card2 = player2_cards.pop(0)
    war_cards.append(face_up_card1)
    war_cards.append(face_up_card2)
    print(f"WAR face up cards: Player 1: [{face_up_card1[0]} of {face_up_card1[1]}]   Player 2: [{face_up_card2[0]} of {face_up_card2[1]}]")
    print(f"Number of cards in war_cards: {len(war_cards)}.")

    winner = compare_cards(face_up_card1, face_up_card2)
    if winner == 0:
        # It's a tie, conduct another war
        print(f"WAR Tie, Another round of War!") 
        return conduct_war(player1_cards, player2_cards, war_cards)
    elif winner == 1:
        player1_cards.extend(war_cards)
    elif winner == 2:
        player2_cards.extend(war_cards)
    
    return winner


def main():
    #create two demensional array using numpy to keep track of the # of cards each player has after each round
    card_counts = np.array([], dtype=int).reshape(0,2)
    scoreboard = load_scoreboard("War_Scoreboard.csv")
    deck = create_deck()
    player1_cards, player2_cards = deal(deck)
    round_counter = 1
    maximum_rounds = 10

    # Placeholder for the game loop
    while player1_cards and player2_cards and round_counter <=maximum_rounds:
        card1 = player1_cards.pop(0)
        card2 = player2_cards.pop(0)
        card1_value, card1_suit = card1
        card2_value, card2_suit = card2
        print(f"\nRound {round_counter} Play cards: Player 1: [{card1_value} of {card1_suit}]   Player 2: [{card2_value} of {card2_suit}]")

        winner = compare_cards(card1, card2)
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
    average_cards = np.mean(card_counts, axis=0)
    print(f"Average cards: Player 1: {average_cards[0]}, Player 2: {average_cards[1]}")

    df = pd.DataFrame(card_counts)
    df['Player 1 > Player 2'] = df[0].shift(-1) > df[1]
    subset = df[df["Player 1 > Player 2"] == True]
    print("here are the hands where player 1 did better than player 2")
    print(subset)
  


    # Placeholder for determining and announcing the final winner

if __name__ == "__main__":
    main()