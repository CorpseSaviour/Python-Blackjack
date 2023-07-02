import random

class Card:
  def __init__(self,suit,rank):
    self.suit = suit
    self.rank = rank
    if rank == "A":
      self.value = 11
    elif rank == "J" or rank == "Q" or rank == "K":
      self.value = 10
    else:
      self.value = rank

  def __str__(self):
    return f"{self.rank} of {self.suit}"

class Deck:
	def __init__(self):
		self.cards = []
		suits = ["spades", "clubs", "hearts", "diamonds"]
		ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
		for rank in ranks:
			for suit in suits:
				self.cards.append(Card(suit,rank))

	def shuffle(self):
		if len(self.cards) > 1:
			random.shuffle(self.cards)

	def deal(self,number):
		cards_dealt = []
		for n in range(number):
			cards_dealt.append(self.cards.pop())
		return cards_dealt
	
	def __str__(self):		
		deck = ""
		for card in self.cards:
			deck += card.__str__() + " "
		return deck

class Hand:
  def __init__(self, dealer = False):
    self.cards = []
    self.value = 0
    self.dealer = dealer

  def add_card(self, card_list):
    self.cards.extend(card_list)

  def calculate_value(self):
    self.value = 0
    has_ace = False

    for card in self.cards:
      if card.rank == "A":
        has_ace = True

    for card in self.cards:
      self.value += int(card.value)
    
    if self.value > 21 and has_ace:
      self.value -= 10
  
  def get_value(self):
    self.calculate_value()
    return self.value
  
  def display(self, show_all_dealer_cards = False) -> str:
    hand = ""
    if self.dealer:
      hand += "Dealer's hand: " 
    else:
      hand += "Your hand: "
    for index, card in enumerate(self.cards):
      if index == 0 and self.dealer \
      and not show_all_dealer_cards \
      and not self.is_blackjack():
        hand += "hidden, "
      else:
        hand += card.__str__() + ", "
      
    print(hand[:len(hand)-2])

  def is_blackjack(self):
      return self.get_value() == 21

class Game:
    def check_winner(self,player_hand,dealer_hand,game_over = False):
      if not game_over:
        if player_hand.get_value() > 21:
            print("You busted. Dealer wins!")
            return True
        elif dealer_hand.get_value() > 21:
            print("Dealer busted. You win!")
            return True
        elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
            print("Both players have blackjack! Tie!")
            return True
        elif player_hand.is_blackjack():
            print("You have a blackjack! You win!")
            return True
        elif dealer_hand.is_blackjack():
            print("Dealer has a blackjack! Dealer wins!")
            return True
      else:
          if player_hand.get_value() > dealer_hand.get_value():
              print("You win!")
          elif player_hand.get_value() == dealer_hand.get_value():
              print("It's a tie!")
          else:
              print("Dealer wins!")
      return False

    def play(self):
        game_number = 0
        games_to_play = 0
        tries = 0
        while games_to_play <= 0 and tries < 10:
          try:
            tries += 1
            games_to_play = int(input("How many games do you want to play? "))
          except:
            print("You must enter a number!")
        if tries == 10:
            print('Error, too many wrong attempts')
            return
        def multiple():
          if games_to_play > 1:
            return "s"
          else: 
            return ""
        print(f"We'll play {games_to_play} game{multiple()} then!")

        while game_number < games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for i in range(2):
              player_hand.add_card(deck.deal(1))
              dealer_hand.add_card(deck.deal(1))

            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand,dealer_hand):
                continue
            
            choice = ""
            while player_hand.get_value() < 21 and choice not in ["s","stand"]:
                choice = input("Pleace choose 'Hit' or 'Stand': ").lower()
                print()
                while choice not in ["h","s","hit","stand"]:
                  choice =input("Please enter 'Hit' or 'Stand' (or H/S): ").lower()
                if choice in ["h","hit"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()

            if self.check_winner(player_hand,dealer_hand):
              continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
              dealer_hand.add_card(deck.deal(1))
              dealer_hand_value = dealer_hand.get_value()
            
            dealer_hand.display(show_all_dealer_cards=True)

            print("Final Results")
            print("Your hand:",player_hand_value)
            print("Dealer hand:", dealer_hand_value)

            self.check_winner(player_hand,dealer_hand,True)

        print("\nThanks for playing!")

g = Game()
g.play()