import game
import chess
import multiAgents

state = chess.GameState()

for x in range(len(state.board)):
    for y in range(len(state.board)):
        state.board[x][y] = None

state.board[1][5] = 'BK'
state.board[2][2] = 'WR'
state.board[2][4] = 'BR'
state.board[4][5] = 'BP'
state.board[5][5] = 'WK'
state.board[6][5] = 'WP'

print(state.board)
#act = state.getLegalActions(1)

#print(act)

#print(len(act))"""



agent = multiAgents.AlphaBetaAgent()
#state = chess.GameState()
action = agent.getAction(state)


print(action)
