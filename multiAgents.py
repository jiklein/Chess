# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).




class Agent:
    """
    An agent must define a getAction method, but may also define the
    following methods which will be called if they exist:

    def registerInitialState(self, state): # inspects the starting state
    """

    def __init__(self, index=0):
        self.index = index

    def getAction(self, state):
        """
        The Agent will receive a GameState (from either {pacman, capture, sonar}.py) and
        must return an action from Directions.{North, South, East, West, Stop}
        """
        raiseNotDefined()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = scoreEvaluationFunction
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """
        return minimax(self, 0, gameState, self.depth)['action']

def minimax(agent, agentIndex, state, depth):
    """
    Returns the value of a given state
    """

    # Loop index and update depth
    if agentIndex == state.getNumAgents():
        agentIndex = 0
        depth -= 1

    # Check maximizer
    if agentIndex == 0:
        return max_mini(agent, agentIndex, state, depth)

    # Assume minimizer
    else:
        return min_mini(agent, agentIndex, state, depth)

def min_mini(agent, agentIndex, state, depth):
    """
    Returns the minimum value of the successors
    """
    val, act = float('inf'), None

    # For each successor
    for newAct in state.getLegalActions(-1):
        newState = state.generateSuccessor(-1, newAct)

        # Base case (leaf node or end of search)
        if newState.isEnd() or (depth == 1 and
                agentIndex == state.getNumAgents() - 1):
            newVal = agent.evaluationFunction(newState)

        # Recursive call on successor
        else:
            newVal = minimax(agent, agentIndex + 1, newState, depth)['value']

        # Update minimum
        if newVal < val:
            val, act = newVal, newAct
    return {'value': val, 'action': act}

def max_mini(agent, agentIndex, state, depth):
    """
    Returns the maximum value of the successors
    """
    val, act = float('-inf'), None

    # For each successor
    for newAct in state.getLegalActions(1):
        newState = state.generateSuccessor(1, newAct)

        # Base case (leaf node or end of search)
        if newState.isEnd() or (depth == 1 and
                agentIndex == state.getNumAgents() - 1):
            newVal = agent.evaluationFunction(newState)

        # Recursive call on successor
        else:
            newVal = minimax(agent, agentIndex + 1, newState, depth)['value']

        # Update maximum
        if newVal > val:
            val, act = newVal, newAct
    return {'value': val, 'action': act}

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """
        return prune(float('-inf'), float('inf'), self, 0, gameState, self.depth)['action']

def prune(alpha, beta, agent, agentIndex, state, depth):
    """
    Returns the value of a given state
    """

    # Loop index and update depth
    if agentIndex == state.getNumAgents():
        agentIndex = 0
        depth -= 1

    # Check maximizer
    if agentIndex == 0:
        return max_prune(alpha, beta, agent, agentIndex, state, depth)

    # Assume minimizer
    else:
        return min_prune(alpha, beta, agent, agentIndex, state, depth)

def min_prune(alpha, beta, agent, agentIndex, state, depth):
    """
    Returns the minimum value of the successors
    """
    val, act = float('inf'), None

    # For each successor
    for newAct in state.getLegalActions(-1):
        newState = state.generateSuccessor(-1, newAct)

        # Base case (leaf node or end of search)
        if newState.isEnd() or (depth == 1 and
                agentIndex == state.getNumAgents() - 1):
            newVal = agent.evaluationFunction(newState)

        # Recursive call on successor
        else:
            newVal = prune(alpha, beta, agent, agentIndex + 1, newState, depth)['value']

        # Update minimum
        if newVal < val:
            val, act = newVal, newAct
        if val < alpha:
    #        print("wasPruned")
            return {'value': val, 'action': act}
        beta = min(beta, val)
    return {'value': val, 'action': act}

def max_prune(alpha, beta, agent, agentIndex, state, depth):
    """
    Returns the maximum value of the successors
    """
    val, act = float('-inf'), None

    # For each successor
    for newAct in state.getLegalActions(1):
        newState = state.generateSuccessor(1, newAct)

        # Base case (leaf node or end of search)
        if newState.isEnd() or (depth == 1 and
                agentIndex == state.getNumAgents() - 1):
            newVal = agent.evaluationFunction(newState)

        # Recursive call on successor
        else:
            newVal = prune(alpha, beta, agent, agentIndex + 1, newState, depth)['value']

        # Update maximum
        if newVal > val:
            val, act = newVal, newAct
        if val > beta:
     #       print("wasPruned")
            return {'value': val, 'action': act}
        alpha = max(alpha, val)
    return {'value': val, 'action': act}

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        return expectimax(self, 0, gameState, self.depth)['action']

def expectimax(agent, agentIndex, state, depth):
    """
    Returns the value of a given state
    """

    # Loop index and update depth
    if agentIndex == state.getNumAgents():
        agentIndex = 0
        depth -= 1

    # Check maximizer
    if agentIndex == 0:
        return max_expect(agent, agentIndex, state, depth)

    # Assume minimizer
    else:
        return ave_expect(agent, agentIndex, state, depth)

def ave_expect(agent, agentIndex, state, depth):
    """
    Returns the minimum value of the successors
    """
    total = length = 0

    # For each successor
    for newAct in state.getLegalActions(agentIndex):
        newState = state.generateSuccessor(agentIndex, newAct)

        # Base case (leaf node or end of search)
        if newState.isEnd() or (depth == 1 and
                agentIndex == state.getNumAgents() - 1):
            newVal = agent.evaluationFunction(newState)

        # Recursive call on successor
        else:
            newVal = expectimax(agent, agentIndex + 1, newState, depth)['value']

        # Update total
        total += newVal
        length += 1
        if newAct == 'Stop':
            print(newVal)
    return {'value': total/length, 'action': None}

def max_expect(agent, agentIndex, state, depth):
    """
    Returns the maximum value of the successors
    """
    val, act = float('-inf'), None

    # For each successor
    actionVals = []
    for newAct in state.getLegalActions(agentIndex):
        newState = state.generateSuccessor(agentIndex, newAct)

        # Base case (leaf node or end of search)
        if newState.isEnd() or (depth == 1 and
                agentIndex == state.getNumAgents() - 1):
            newVal = agent.evaluationFunction(newState)

        # Recursive call on successor
        else:
            newVal = expectimax(agent, agentIndex + 1, newState, depth)['value']

        # Update maximum
        actionVals.append({'value': newVal, 'action': newAct})
        if newVal > val:
            val, act = newVal, newAct
    return {'value': val, 'action': act}


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    # Useful information you can extract from a GameState (pacman.py)
    return None
# Abbreviation
better = betterEvaluationFunction
