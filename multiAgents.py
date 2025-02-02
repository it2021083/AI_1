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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

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
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        def minimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            if agentIndex == 0:  # Pacman's turn (max)
                return max_value(state, depth, agentIndex)
            else:  # Ghosts' turn (min)
                return min_value(state, depth, agentIndex)

        def max_value(state, depth, agentIndex):
            v = float('-inf')
            best_action = None
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                successor_value, _ = minimax(successor, depth, agentIndex + 1)
                if successor_value > v:
                    v = successor_value
                    best_action = action
            return v, best_action

        def min_value(state, depth, agentIndex):
            v = float('inf')
            best_action = None
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            nextDepth = depth + 1 if nextAgentIndex == 0 else depth
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                successor_value, _ = minimax(successor, nextDepth, nextAgentIndex)
                if successor_value < v:
                    v = successor_value
                    best_action = action
            return v, best_action

        _, action = minimax(gameState, 0, 0)
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

        def alphabeta(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            if agentIndex == 0:  # Pacman's turn (max)
                return max_value(state, depth, agentIndex, alpha, beta)
            else:  # Ghosts' turn (min)
                return min_value(state, depth, agentIndex, alpha, beta)

        def max_value(state, depth, agentIndex, alpha, beta):
            v = float('-inf')
            best_action = None
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                successor_value, _ = alphabeta(successor, depth, agentIndex + 1, alpha, beta)
                if successor_value > v:
                    v = successor_value
                    best_action = action
                if v > beta:
                    return v, best_action
                alpha = max(alpha, v)
            return v, best_action

        def min_value(state, depth, agentIndex, alpha, beta):
            v = float('inf')
            best_action = None
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            nextDepth = depth + 1 if nextAgentIndex == 0 else depth
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                successor_value, _ = alphabeta(successor, nextDepth, nextAgentIndex, alpha, beta)
                if successor_value < v:
                    v = successor_value
                    best_action = action
                if v < alpha:
                    return v, best_action
                beta = min(beta, v)
            return v, best_action

        _, action = alphabeta(gameState, 0, 0, float('-inf'), float('inf'))
        return action

        
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
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
       
        
        def expectimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            if agentIndex == 0:  # Pacman's turn (max)
                return max_value(state, depth, agentIndex)
            else:  # Ghosts' turn (expectation)
                return expect_value(state, depth, agentIndex)

        def max_value(state, depth, agentIndex):
            v = float('-inf')
            best_action = None
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                successor_value, _ = expectimax(successor, depth, agentIndex + 1)
                if successor_value > v:
                    v = successor_value
                    best_action = action
            return v, best_action

        def expect_value(state, depth, agentIndex):
            v = 0
            actions = state.getLegalActions(agentIndex)
            probability = 1.0 / len(actions)  # Assuming uniform probability
            nextAgentIndex = (agentIndex + 1) % state.getNumAgents()
            nextDepth = depth + 1 if nextAgentIndex == 0 else depth
            for action in actions:
                successor = state.generateSuccessor(agentIndex, action)
                successor_value, _ = expectimax(successor, nextDepth, nextAgentIndex)
                v += probability * successor_value
            return v, None

        _, action = expectimax(gameState, 0, 0)
        return action
        

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    
    # Useful information about the game state
    pacmanPosition = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsules = currentGameState.getCapsules()

    # Initialize score with the game score
    score = currentGameState.getScore()

    # Calculate the distance to the closest food
    if foodList:
        closestFoodDistance = min([util.manhattanDistance(pacmanPosition, food) for food in foodList])
        score += 10.0 / closestFoodDistance

    # Calculate the distance to the closest ghost
    for ghostState in ghostStates:
        ghostPosition = ghostState.getPosition()
        ghostDistance = util.manhattanDistance(pacmanPosition, ghostPosition)
        if ghostState.scaredTimer > 0:
            score += 200.0 / ghostDistance
        else:
            if ghostDistance > 0:
                score -= 10.0 / ghostDistance

    # Calculate the distance to the closest power pellet
    if capsules:
        closestCapsuleDistance = min([util.manhattanDistance(pacmanPosition, capsule) for capsule in capsules])
        score += 20.0 / closestCapsuleDistance

    # Consider the number of food left
    score -= 4.0 * len(foodList)

    # Consider the number of power pellets left
    score -= 20.0 * len(capsules)

    return score


# Abbreviation
better = betterEvaluationFunction

