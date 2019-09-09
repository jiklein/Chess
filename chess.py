import copy
from game import Game, Board, Pieces
from game import pieces


class GameState:

    def __init__(self, prevState=None):

        # Copy ctor
        if prevState != None:
            self.board = Board(prevState.board)

        # Set up new board
        else:
            self.board = Board()

    def getLegalActions(self, turn=Game.white):

        actions = self.getMoves(turn)

        # Check for illegal actions (player is in check)
        for act in actions.copy():

            # Get successor
            oppTurn = Game.white if turn == Game.black else Game.black
            successor = self.generateSuccessor(oppTurn, act)

            # Find king
            location = None
            for x in range(len(successor.board)):
                for y in range(len(successor.board[x])):
                    piece = successor.board[y][x]
                    if piece != None and pieces[piece]['color'] == turn and \
                        pieces[piece]['type'] == Pieces.King:
                        location = (x, y)

            # Check if opponent can take king
            moves = successor.getMoves(oppTurn)
            for move in moves:
                if location in move and act in actions:

                    # Remove illegal action
                    actions.remove(act)

        return actions

    def getMoves(self, turn):
        moves = []

        # For each board position
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):

                piece = self.board[y][x]

                # Check movable piece
                if piece != None and pieces[piece]['color'] == turn:

                    # Add new moves
                    moves += pieces[piece]['type'](Pieces, x, y, self, turn)

        return moves


    def generateSuccessor(self, agentIndex, action):

        # Copy current state
        newState = GameState(self)

        # Save piece that will move
        piece = newState.board[action[0][1]][action[0][0]]

        # Remove from board
        newState.board[action[0][1]][action[0][0]] = None

        # Add in new position
        newState.board[action[1][1]][action[1][0]] = piece

        return newState

    def getScore(self):
        whiteScore = 0
        blackScore = 0

        for row in self.board:
            for piece in row:
                if piece != None:
                    if pieces[piece]['color'] == Game.white:
                        whiteScore += pieces[piece]['points']
                    else:
                        blackScore += pieces[piece]['points']

        score = whiteScore - blackScore
#        print(score)
        return score

    def getNumAgents(self):
        return 2

    def isEnd(self):
        end = len(self.getLegalActions(Game.white)) == 0 or \
                len(self.getLegalActions(Game.black)) == 0

        if end:
            print(end)

        return end
        #return False
