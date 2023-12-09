import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

#suits and ranks in tuples 
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
#assigns decks as a list of tuples 
deck = [(suit, rank) for suit in suits for rank in ranks]
print(deck)