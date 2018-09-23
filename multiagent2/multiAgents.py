# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]           

        "*** YOUR CODE HERE ***"
        """
        print "successorGameState: ",currentGameState.generatePacmanSuccessor(action)
        print "newPos: ",successorGameState.getPacmanPosition()
        print "newFood: ",successorGameState.getFood()
        print "newGhostStates: ",successorGameState.getGhostStates()
        print "newScaredTimes: ",[ghostState.scaredTimer for ghostState in newGhostStates]
        print "successorScore: ",successorGameState.getScore()
        return successorGameState.getScore()
        """
        newGhostPositions = successorGameState.getGhostPositions()
        score = 100
        scared = False
        for i in newScaredTimes:
            if i > 0:
                scared = True
        if not scared:
            for i in newGhostPositions:
                if manhattanDistance(newPos,i) < 2:
                    score = score - 100
                else:
                    score = score - 100*(1/manhattanDistance(newPos,i))
        else:
            for i in newGhostPositions:
                if manhattanDistance(newPos,i) == 0:
                    score = score + 20
                else:
                    score = score + 100*(1/manhattanDistance(newPos,i))
        #the food doesn't seem to affect anything regardless of the incentive I give
        if successorGameState.hasFood(newPos[0],newPos[1]) == True:
            score = score + 10000
        else:
            score - score - 50
        
        return score

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
      to the MinimaxPacmanAgent & AlphaBetaPacmanAgent.

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
        """
        "*** YOUR CODE HERE ***"
        #this does what it's supposed to but the autograder fails it
        def max_value(gameState, action, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = -1000000
            bestScore = -1000000
            successorActions = gameState.getLegalActions()
            bestAction = ''
            for action in successorActions:
                v = max(v,min_value(gameState.generateSuccessor(0,action),action, depth -1))
                if v > bestScore or bestScore == None:
                    bestScore = v
                    bestAction = action
            return bestAction

        def min_value(gameState, action, depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = 1000000
            bestScore = 1000000
            successorActions = gameState.getLegalActions()
            bestAction = ''
            for action in successorActions:
                v = min(v,max_value(gameState.generateSuccessor(0,action),action, depth-1))
                if v > bestScore or bestScore == None:
                    bestScore = v
                    bestAction = action
            return bestAction

        v = 1000000
        for action in gameState.getLegalActions():
            bestAction = min(v,max_value(gameState.generateSuccessor(0,action),action,self.depth))
        return bestAction
    
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -1000000
        beta = 1000000
        def max_value(state,alpha,beta,action,depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = -1000000
            successorActions = gameState.getLegalActions()
            for action in successorActions:
                v = max(v,min_value(gameState.generateSuccessor(0,action),alpha,beta,action,depth-1))
                if v >= beta:
                    return action
                alpha = max(alpha,v)
            return action
            
        def min_value(state,alpha,beta,action,depth):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = 1000000
            successorActions = gameState.getLegalActions()
            for action in successorActions:
                v = min(v,max_value(gameState.generateSuccessor(0,action),alpha,beta,action,depth-1))
                if v <= alpha:
                    return action
                beta = min(beta,v)
            return action

        v = 0
        for action in gameState.getLegalActions():
            #I have no idea why this throws the error that it does
            bestAction = min(v,max_value(gameState.generateSuccessor(0,action),alpha,beta,action,self.depth))
        return bestAction
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

