# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # predecessor,successor,action
    s = util.Stack()    
    visited = [] # list of visited nodes
    path = []
    starttuples = problem.getSuccessors(problem.getStartState())
    visited.append(problem.getStartState())
    for state,action,cost in starttuples:
        s.push([problem.getStartState(),state,action])
    while not s.isEmpty():
        predecessor,p,action = s.pop()
        if p not in visited:
            visited.append(p)
            path.append([p,(predecessor,action)])
            if not problem.isGoalState(p):
                successors = problem.getSuccessors(p)
                if not problem.isGoalState(p):
                    for state,action,cost in successors:
                        s.push([p,state,action])
        else:
            continue
        if problem.isGoalState(p):
            a = p
            path = dict(path)
            reversePath = []
            while not a == problem.getStartState():
                predecessor,action = path[a]
                reversePath.append(action)
                a = predecessor
            reversePath.reverse()
            return reversePath
        
                
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # predecessor,successor,action
    visited = []
    path = []
    q = util.Queue()
    starttuples = problem.getSuccessors(problem.getStartState())
    visited.append(problem.getStartState())
    for state,action,cost in starttuples:
        q.push([problem.getStartState(),state,action])
    while not q.isEmpty():
        predecessor,p,action = q.pop()
        if p not in visited:
            visited.append(p)
            path.append([p,(predecessor,action)])
        else:
            continue
        if problem.isGoalState(p):
            a = p
            path = dict(path)
            reversePath = []
            while not a == problem.getStartState():
                predecessor,action = path[a]
                reversePath.append(action)
                a = predecessor            
            reversePath.reverse()
            return reversePath
        successors = problem.getSuccessors(p)
        for state,action,cost in successors:
            q.push([p,state,action])
                         
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # predecessor, state, action, cost
    pq = util.PriorityQueue()
    totalCost = 0
    predecessors = []
    visited = []
    starttuples = problem.getSuccessors(problem.getStartState())
    visited.append(problem.getStartState())
    for state,action,cost in starttuples:
        pq.push([problem.getStartState(),state,totalCost + cost,action],totalCost + cost)
    while not pq.isEmpty():
        predecessor,state,totalCost,action = pq.pop()
        if state not in visited:
            visited.append(state)
            predecessors.append([state,(predecessor,action)])
        else:
            continue
        if problem.isGoalState(state):
            move = []
            a = state
            predecessors = dict(predecessors)
            while not a == problem.getStartState():
                predecessor,action = predecessors[a]
                move.append(action)
                a = predecessor
            move.reverse()
            return move
        for successorState,successorAction,successorCost in problem.getSuccessors(state):
            pq.push([state,successorState,totalCost + successorCost,successorAction],totalCost + successorCost)
            
                
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # predecessor, state, action, cost
    pq = util.PriorityQueue()
    totalCost = 0
    predecessors = []
    visited = []
    starttuples = problem.getSuccessors(problem.getStartState())
    visited.append(problem.getStartState())
    for state,action,cost in starttuples:
        pq.push([problem.getStartState(),state,totalCost + cost,action],totalCost + cost + util.manhattanDistance(state,(1,1)))
    while not pq.isEmpty():
        predecessor,state,totalCost,action = pq.pop()
        if state not in visited:
            visited.append(state)
            predecessors.append([state,(predecessor,action)])
        else:
            continue
        if problem.isGoalState(state):
            move = []
            a = state
            predecessors = dict(predecessors)
            while not a == problem.getStartState():
                predecessor,action = predecessors[a]
                move.append(action)
                a = predecessor
            move.reverse()
            return move
        for successorState,successorAction,successorCost in problem.getSuccessors(state):
            pq.push([state,successorState,totalCost + successorCost,successorAction],totalCost + successorCost + util.manhattanDistance(successorState,(1,1)))
    
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
