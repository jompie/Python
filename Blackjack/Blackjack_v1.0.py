import random
faces = ("A","2","3","4","5","6","7","8","9", "10","J","Q","K")
values = (1,2,3,4,5,6,7,8,9,10,10,10,10)
suits = ("Hearts", "Diamonds", "Clubs", "Spades")
playing = False
restart_phrase = "Press 'd' to deal the cards again, or press 'q' to quit"

class Player(object):
    hand = []
    bet = 0
    stats = {"Wins": 0, "Losses": 0}

    def __init__(self, name, credit=1000):
        self.name = name
        self.credit = credit  

    def show_hand(self):
        self.hand.show_hand(hidden=False)

    def hand_value(self):
        return self.hand.get_value()

    def set_bet_amount(self, amount):
        self.bet = amount

class Dealer(Player):   
    def __init__(self):
        self.name = "Dealer"

    def show_hand(self):
        self.hand.show_hand(hidden=True)

class Game(object):
    deck = []
    dealer = Dealer()
    
    def __init__(self):
        player = Player("Player 1", 1000)
        self.deck = Deck()
        self.deck.shuffle()

class Deck(object):
    
    def __init__(self):
        self.cards = []
        for suit in suits:
            for face in faces:
                self.cards.append(Card(suit, face))
    def shuffle(self):
        random.shuffle(self.cards)

    def next_card(self):
        return self.cards.pop()

    def return_cards(self, cards):
        return self.cards

class Card(object):
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def __str__(self):
        return (self.suit +" "+ self.face)

    def get_suit(self):
        return self.suit

    def get_face(self):
        return self.face

    def show_card(self):
        print("\t",self.suit+" "+self.face)
    
class Hand(object):
    
    def __init__(self):
        self.hand = []

    def __str__(self):
        result = ""
        for card in self.hand:
            result += " "+card.__str__()

        return result

    def draw_from_deck(self, deck):
        self.hand.append(deck.next_card())

    def return_to_deck(self, deck):
        deck.return_cards(hand)

    def get_value(self):
        value = 0
        ace_in_hand = False
        for card in self.hand:
            face = card.get_face()
            if face == "A":
                value += 1
                ace_in_hand = True
            elif face in ("10", "J", "Q", "K"):
                value += 10
            else:
                value += int(face)
        if value < 11 and ace_in_hand:
            value += 10

        return value

    def show_hand(self, hidden):
        if hidden and playing:
            starting_card = 1
        else:
            starting_card = 0
        for card in range(starting_card, len(self.hand)):
            self.hand[card].show_card()

def make_bet():
    global player
    bet = 0
    while bet == 0: 
        while True:
            try:
                bet = int(input("Enter your bet: "))
                break
            except:
                print("Your bet must be an integer!")
                continue
        if bet >=1 and bet <= player.credit:
            player.set_bet_amount(bet)
        else:
            print("You only have ", player.credit)
            bet=0
            
def deal():
    global game, player, playing, result
    
    if (playing):
        result = "You lost! Dare to play again? D/Q: "
        playing = False
        player_input()
    else:
        # Let's the player set a bet amount
        make_bet()
        
        # Start with a full deck that's shuffled        
        game.deck = Deck()

        # initialize player and dealer hands
        player.hand = Hand()
        game.dealer.hand = Hand()

        # draw player and dealer hands
        player.hand.draw_from_deck(game.deck)
        game.dealer.hand.draw_from_deck(game.deck)
        player.hand.draw_from_deck(game.deck)
        game.dealer.hand.draw_from_deck(game.deck)

        
    playing = True
    game_step()

def hit():
    global playing, player, game, result

    if playing:
        if player.hand_value() <= 21:
            player.hand.draw_from_deck(game.deck)
        print("Player: ")
        player.show_hand()
        if player.hand_value() >= 22:
            result = "Busted" + restart_phrase

    else:
        result = "Sorry, can't hit" + restart_phrase

    game_step()
            

def stand():
    global playing, player, game, result
    
    if not playing:
        if player.hand_value() > 0:
            result = "Sorry you can't stand"
    else:
        # If the value of the dealers hand is less than 17, another card will be drawn
        while game.dealer.hand_value() < 17:
            game.dealer.hand.draw_from_deck(game.deck)

        # Dealer busts if the value of his hand is more than 21   
        if game.dealer.hand_value() > 21:
            result = "Dealer Busts! You win!" + restart_phrase
            player.credit += player.bet
            playing = False

        # Dealer hand value is lower than the players hand value
        elif game.dealer.hand_value() < player.hand_value():
            result = "You beat the dealer! Congratulations, you win." + restart_phrase
            player.credit += player.bet
            playing = False

        #Dealer hand value is the same as players hand value
        elif game.dealer.hand_value() == player.hand_value():
            result = "Tied up, push!" + restart_phrase
            playing = False

        else:
            result = "Dealer wins!" + restart+phrase
            player.credit -= player.bet
            playing = False

        game_step()
                       
def game_step():
    global result, playing, player, game
    
    print("Your balance:", player.credit)
    print("Player: ")
    player.show_hand()
    print("Hand total: ",player.hand_value(),"\n")
    print("Dealer: ")
    game.dealer.show_hand()
    
    if not playing:
        print(" --- for a total of " + str(game.dealer.hand_value()))
        print("Your balance: " + str(player.credit))
    else: 
        print(" with another card hidden upside down")
    
    print(result)
    
    player_input()

def exit_game():
    print ("Goodbye.")

def player_input():
    global playing
    inp = input().lower()

    if inp == "h":
        hit()
    elif inp == "s":
        stand()
    elif inp == "d":
        deal()
    elif inp == "q":
        exit_game()
    else:
        print("Invalid input! Try again: ")
        player_input()

def intro():
    statement = """Welcome to blackjack! You know the rules."""
    print(statement)

# set default result message
result = "Hit or stand? h/s: "       

intro()

game = Game()
name = ""
credit = 0
while len(name)==0:
        name = input("What's your name?: ")
while credit ==0:
        credit = int(input("How much money do want to lose?"))
player = Player(name,credit)
        
deal()        
