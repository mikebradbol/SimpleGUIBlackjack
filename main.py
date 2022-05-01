from random import choice
import tkinter as tk

cards = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')
scores = {'Ace': 1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10}

class BJPlayer():
    def __init__(self):
        self.hand = []
        self.score = [0, 0]
        self.flag = 1

    def printHand(self):
        print(self.hand)

    def maxValidScore(self):
        if self.score[1] > 21:
            return self.score[0]
        else:
            return self.score[1]

    def restart(self):
        self.hand = []
        self.score = [0, 0]
        self.flag = 1

    def getHandStr(self):
        return ' '.join(self.hand)

    def getScoreStr(self):
        if self.score[0] != self.score[1]:
            return f'{self.score[0]} and {self.score[1]}'
        else:
            return f'{self.score[0]}'

    

# I'm going to try to make a simple blackjack game
def main():
    # 'shuffle' the deck at the beginning of the game
    deck = []
    shuffle(deck)

    dealer = BJPlayer()
    player = BJPlayer()
    winOrLose = 0
    actions = ('stand', 'hit')
    pastActions = []

    # deal the first 4 cards of the game
    for i in range(2):
        dealer.flag = pick(dealer, deck)
        player.flag = pick(player, deck)

    # see if either player has already won
    # if both dealer and player have 21, dealer wins
    if (dealer.score[0] == 21) or (dealer.score[1] == 21):
        winOrLose = 1
    elif (player.score[0] == 21) or (player.score[1] == 21):
        winOrLose = 2

    # enter the main gameplay loop until the player wins or loses
    while not winOrLose:
        # first we let the player know what score they have
        # TODO: make this prettier
        print(player.hand)
        print(player.score)

        # player needs to decide what to do
        action = input("What will you do?\n")
        action = action.lower()
        while action not in actions:
            action = input('Invalid action: available actions are "hit" and "stand"\n')

        pastActions.append(action)

        # perform a hit if requested
        if action == 'hit':
            pick(player, deck)
            # check for bust or win
            val = bustOrWin(player)
            if val == 1:
                winOrLose = 1
                break
            elif val == 2:
                winOrLose = 2
                break
                
        # 'perform' player's hold or draw for dealer
        # dealer doesn't draw if they are at 17 or above in either of their scores
        if (dealer.score[0] < 17) and (dealer.score[1] < 17):
            pick(dealer, deck)
            # check for bust or win
            val = bustOrWin(dealer)
            if val == 1:
                winOrLose = 2
                break
            elif val == 2:
                winOrLose = 1
        else:
            if len(pastActions) >= 2:
                if (pastActions[-1] == 'stand') and (pastActions[-2] == 'stand'):
                    print('The game has come to a stalemate')
                    dealerPoints = dealer.maxValidScore()
                    playerPoints = player.maxValidScore()
                    if dealerPoints >= playerPoints:
                        winOrLose = 1
                    else:
                        winOrLose = 2
                    break
            else:
                print('The dealer has chosen to stand')
        
    print('Final hands')
    print(f'dealer: {dealer.hand}')
    print(f'player: {player.hand}')
    if winOrLose == 1:
        print("Dealer won, better luck next time")
    else:
        print('Congrats! You won!')


# randomly picks a card for the player and adds it to the player's score
def pick(player, deck):
    # pick the player's new card
    card = deck.pop()
    player.hand.append(card)

    # add the player's card to their scores
    if (card == 'Ace') and (player.flag):
        player.score[0] += 1
        player.score[1] += 11
        return 0
    else:
        player.score[0] += scores[card]
        player.score[1] += scores[card]
        return player.flag

def bustOrWin(player):
    score = player.score
    if score[0] > 21:
        return 1
        
    if (score[0] == 21) or (score[1] == 21):
        return 2

    return 0

# "shuffles" the deck at the beginning of the game
def shuffle(deck):
    copyCards = list(cards)
    while len(deck) < 52:
        card = choice(copyCards)
        deck.append(card)
        if deck.count(card) == 4:
            copyCards.remove(card)
    

# remade the game with a tkinter gui
def gui():

    def initWinCheck():
        # see if either player has won the game
        if (dealer.score[0] == 21) or (dealer.score[1] == 21):
            gameOver(0)
        elif (player.score[0] == 21) or (player.score[1] == 21):
            gameOver(1)
    
    # performs the requested action, processes the dealer's next move and determines if either player has won
    def action(n):
        # if the player wanted to hit, hit
        if n:
            player.flag = pick(player, deck)
            if (player.score[0] == 21) or (player.score[1] == 21):
                gameOver(1)
            elif player.score[0] > 21:
                gameOver(0)
        # determine what the dealer is going to do
        # dealer stands on soft 17
        if dealer.score[1] < 17:
            dealer.flag = pick(dealer, deck)
            if (dealer.score[0] == 21) or (dealer.score[1] == 21):
                gameOver(0)
            elif dealer.score[0] > 21:
                gameOver(1)
        # if the dealer stands, determine if a stalemate has occured
        else:
            if not n:
                pScore = player.score[1] if player.score[1] < 22 else player.score[0]
                dScore = dealer.score[1] if dealer.score[1] < 22 else dealer.score[0]
                if pScore > dScore:
                    gameOver(1)
                else:
                    gameOver(0)
                
        gameLoop()
        
    # enter the main gameplay loop until the player wins or loses
    def gameLoop():        
        # clear the frame to build a new one
        for widget in frame.winfo_children():
            widget.destroy()

        playerhand = tk.Label(frame, text='Your hand is: ' + player.getHandStr())
        playerhand.pack()

        playerscore = tk.Label(frame, text='Your score(s) are: ' + player.getScoreStr())
        playerscore.pack()

        hit = tk.Button(frame, text='Hit', command=lambda n=1: action(n))
        hit.pack()
        stand = tk.Button(frame, text='Stand', command=lambda n=0: action(n))
        stand.pack()

        frame.pack()
        tk.mainloop()

    def gameOver(flag):
        for widget in frame.winfo_children():
            widget.destroy()

        top = ('Game Over... You Lost...', 'Congrats! You Won!')

        label = tk.Label(frame, text=top[flag])
        label.pack()

        playerhand = tk.Label(frame, text='Your hand is: ' + player.getHandStr())
        playerhand.pack()

        playerscore = tk.Label(frame, text='Your score(s) are: ' + player.getScoreStr())
        playerscore.pack()

        dealerhand = tk.Label(frame, text="The dealer's hand was: " + dealer.getHandStr())
        dealerhand.pack()

        dealerscore = tk.Label(frame, text="The dealer's score(s) is: " + dealer.getScoreStr())
        dealerscore.pack()

        button = tk.Button(frame, text='Restart', command=lambda n=0:restart())
        button.pack()

        frame.pack()
        tk.mainloop()

    def restart():
        global deck
        deck = []
        shuffle(deck)

        player.restart()
        dealer.restart()
        for i in range(2):
            dealer.flag = pick(dealer, deck)
            player.flag = pick(player, deck)
        initWinCheck()
        gameLoop()


    window = tk.Tk()
    window.title = 'Black Jack'
    frame = tk.Frame(window)

    deck = []
    shuffle(deck)
    
    dealer = BJPlayer()
    player = BJPlayer()

    # deal the first 4 cards of the game
    for i in range(2):
        dealer.flag = pick(dealer, deck)
        player.flag = pick(player, deck)

    initWinCheck()
    gameLoop()
        
        
  
if __name__ == '__main__':
        gui()