class Game:

    boardLength = 8
    board = [(x,y) for x in range(8) for y in range(8)]

    white = 1
    black = -1

    whitePawnStart = 1
    blackPawnStart = 7

    # Directions the knight can move in (dx, dy)
    knightDir = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), \
            (2, -1), (2, 1)]

    # Directions the bishop can move in (dx, dy)
    bishopDir = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    # Directions the rook can move in (dx, dy)
    rookDir = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # Directions the queen/king can move in (dx, dy)
    royalDir = bishopDir + rookDir


class Pieces(dict):

    def Pawn(self, x, y, state, turn):
        moves = []

        newY = y + turn

        # Check forward move
        if (x, newY) in Game.board and state.board[newY][x] == None:
            moves.append(((x, y), (x, newY)))

        # Check capture
        for newX in [x - 1, x + 1]:
            if (newX, newY) in Game.board and state.board[newY][newX] != None \
                and pieces[state.board[newY][newX]]['color'] != turn:
                moves.append(((x, y), (newX, newY)))

        # Check first move
        if turn == Game.white and y == Game.whitePawnStart or \
            turn == Game.black and y == Game.blackPawnStart:
            moves.append(((x, y), (x, y + 2 * turn)))

        return moves

    def Knight(self, x, y, state, turn):

        moves = []

        # Check each position
        for dX, dY in Game.knightDir:
            newX = x + dX
            newY = y + dY

            # Check open spot or cature
            if (newX, newY) in Game.board and (state.board[newY][newX] == None \
                or pieces[state.board[newY][newX]]['color'] != turn):
                moves.append( ((x, y), (newX, newY)) )

        return moves

    def Bishop(self, x, y, state, turn):

        moves = []

        for dX, dY in Game.bishopDir:

            n = 1
            while True:
                newX = x + n * dX
                newY = y + n * dY

                if (newX, newY) not in Game.board:
                    break
                elif state.board[newY][newX] == None:
                    moves.append( ((x, y), (newX, newY)) )
                    n += 1
                elif pieces[state.board[newY][newX]]['color'] != turn:
                    moves.append( ((x, y), (newX, newY)) )
                    break
                else:
                    break

        return moves

    def Rook(self, x, y, state, turn):
        moves = []

        for dX, dY in Game.rookDir:

            n = 1
            while True:
                newX = x + n * dX
                newY = y + n * dY

                if (newX, newY) not in Game.board:
                    break
                elif state.board[newY][newX] == None:
                    moves.append( ((x, y), (newX, newY)) )
                    n += 1
                elif pieces[state.board[newY][newX]]['color'] != turn:
                    moves.append( ((x, y), (newX, newY)) )
                    break
                else:
                    break

        return moves
    def Queen(self, x, y, state, turn):
        moves = []

        for dX, dY in Game.royalDir:

            n = 1
            while True:
                newX = x + n * dX
                newY = y + n * dY

                if (newX, newY) not in Game.board:
                    break
                elif state.board[newY][newX] == None:
                    moves.append( ((x, y), (newX, newY)) )
                    n += 1
                elif pieces[state.board[newY][newX]]['color'] != turn:
                    moves.append( ((x, y), (newX, newY)) )
                    break
                else:
                    break

        return moves

    def King(self, x, y, state, turn):
        moves = []

        for dX, dY in Game.royalDir:

            newX = x + dX
            newY = y + dY

            if (newX, newY) in Game.board and (state.board[newY][newX] == None \
                or pieces[state.board[newY][newX]]['color'] != turn):
                moves.append( ((x, y), (newX, newY)) )

        return moves

    def move(self, state, oldPos, newPos):

        # Copy board
        newState = copy.deepcopy(state)

        # Take piece off board
        newState[oldPos[0]][oldPos[1]] = None

        # Place piece down
        newState[newPos[0]][newPos[1]] = state[oldPos[0]][oldPos[1]]

        return newState

pieces = {

            'WR': {'color': 1, 'type': Pieces.Rook, 'points': 5},
            'WN': {'color': 1, 'type': Pieces.Knight, 'points': 2},
            'WB': {'color': 1, 'type': Pieces.Bishop, 'points': 2},
            'WQ': {'color': 1, 'type': Pieces.Queen, 'points': 10},
            'WK': {'color': 1, 'type': Pieces.King, 'points': 0},
            'WP': {'color': 1, 'type': Pieces.Pawn, 'points': 1},
            'BR': {'color': -1, 'type': Pieces.Rook, 'points': 5},
            'BN': {'color': -1, 'type': Pieces.Knight, 'points': 2},
            'BB': {'color': -1, 'type': Pieces.Bishop, 'points': 2},
            'BQ': {'color': -1, 'type': Pieces.Queen, 'points': 10},
            'BK': {'color': -1, 'type': Pieces.King, 'points': 0},
            'BP': {'color': -1, 'type': Pieces.Pawn, 'points': 1}
            }

class Board(list):
    def __init__(self, clone=None):

        # Copy ctor
        if clone != None:
            for y in range(len(clone)):
                self.append([])
                for x in range(len(clone[y])):
                    self[y].append(clone[y][x])

        # Set up board
        else:

            index = 0

            # Set up white pieces
            self.append([])
            self[index].append('WR')
            self[index].append('WN')
            self[index].append('WB')
            self[index].append('WQ')
            self[index].append('WK')
            self[index].append('WB')
            self[index].append('WN')
            self[index].append('WR')

            index += 1

            # Set up white pawns
            self.append([])
            for i in range(Game.boardLength):
                self[index].append('WP')

            index += 1

            # Blank spaces
            for i in range(index, Game.boardLength - index):
                self.append([])
                for j in range(Game.boardLength):
                    self[i].append(None)

                index += 1

            # Set up black pawns
            self.append([])
            for i in range(Game.boardLength):
                self[index].append('BP')

            index += 1

            # Set up black pieces
            self.append([])
            self[index].append('BR')
            self[index].append('BN')
            self[index].append('BB')
            self[index].append('BQ')
            self[index].append('BK')
            self[index].append('BB')
            self[index].append('BN')
            self[index].append('BR')


