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
      
    def play():
        pass

    def show_hand():
        pass

    def hit_or_stand():
        pass

    def set_bet_amount(self, amount):
        self.bet = amount

class Dealer(Player):   
    def __init__(self):
        self.name = "Dealer"

class Game(object):
    deck = []
    dealer = Dealer()
    
    def __init__(self):
        player = Player("Player 1", 1000)
        self.deck = Deck()
        self.deck.shuffle()

    def play():
        pass

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
        result = "You lost! Dare to play again? "
        playing = False
        player_input()
    else:
        make_bet()
        result = "Hit or stand? h/s: "
        player.hand = Hand()
        game.dealer.hand = Hand()

        player.hand.draw_from_deck(game.deck)
        game.dealer.hand.draw_from_deck(game.deck)
    
        player.hand.draw_from_deck(game.deck)
        game.dealer.hand.draw_from_deck(game.deck)

        
    playing = True
    game_step()

def hit():
    global playing, player, game, result

    if playing:
        if player.hand.get_value() <= 21:
            player.hand.draw_from_deck(game.deck)
        print("Player: ")
        player.hand.show_hand(hidden=False)
        if player.hand.get_value() >= 22:
            result = "Busted" + restart_phrase

    else:
        result = "Sorry, can't hit" + restart_phrase

    game_step()
            

def stand():
    global playing, player, game, result

    if not playing:
        if player.hand.get_value() > 0:
            result = "Sorry you can't stand"
    else:
        while game.dealer.hand.get_value() < 17:
            game.dealer.hand.draw_from_deck(game.deck)
            
        if game.dealer.hand.get_value() > 21:
            result = "Dealer Busts! You win!" + restart_phrase
            player.credit += player.bet
            playing = False
            
        elif game.dealer.hand.get_value() < player.hand.get_value():
            result = "You beat the dealer! Congratulations, you win." + restart_phrase
            player.credit += player.bet
            playing = False

        elif game.dealer.hand.get_value() == player.hand.get_value():
            result = "Tied up, push!" + restart_phrase
            playing = False

        else:
            result = "Dealer wins!" + restart+phrase
            player.credit -= player.bet
            playing = False

        game_step()
                       
def game_step():
    global result
    
    print("Your balance:", player.credit)
    print("Player: ")
    player.hand.show_hand(hidden=False)
    print("Hand total: ",player.hand.get_value(),"\n")
    print("Dealer: ")
    game.dealer.hand.show_hand(hidden=True)

    if not playing:
        print(" --- for a total of " + str(game.dealer.hand.get_value()))
        print("Your balance: " + str(player.credit))
    else: 
        print(" with another card hidden upside down")

    print(result)
    
    player_input()

def exit_game():
    pass

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

result = ""        
game = Game()
player = Player("John",1000)
intro()
deal()        
