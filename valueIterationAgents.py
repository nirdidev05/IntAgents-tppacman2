# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0

    if self.iterations == -1:
        self.runValueIterationCv()
        print(f"{self.iterations } iterations to converge")
    else:
        self.runValueIteration(self.iterations)

  def runValueIteration(self,iter):
     """
        Run the indicated number of iterations
     """
     for _ in range(iter):
         new_values = util.Counter()
         for state in self.mdp.getStates():
             if self.mdp.isTerminal(state):
                 new_values[state] = 0
             else:
                 actions = self.mdp.getPossibleActions(state)
                 new_values[state] = max(self.getQValue(state, a) for a in actions)
         self.values = new_values

  def runValueIterationCv(self):
     """
        Run until convergence: max_s |V_k(s) - V_{k-1}(s)| < epsilon
     """
     self.iterations = 0
     epsilon = 1e-6
     while True:
         new_values = util.Counter()
         for state in self.mdp.getStates():
             if self.mdp.isTerminal(state):
                 new_values[state] = 0
             else:
                 actions = self.mdp.getPossibleActions(state)
                 new_values[state] = max(self.getQValue(state, a) for a in actions)
         delta = max(abs(new_values[s] - self.values[s]) for s in self.mdp.getStates())
         self.values = new_values
         self.iterations += 1
         if delta < epsilon:
             break
 
    
  def getValue(self, state):
    """
      Return the value of the state 
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).
    """
    # Q(s,a) = sum_{s'} T(s,a,s') * [R(s,a,s') + gamma * V(s')]
    q = 0.0
    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
        reward = self.mdp.getReward(state, action, nextState)
        q += prob * (reward + self.discount * self.values[nextState])
    return q
      
  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    # pi*(s) = argmax_a Q(s,a), ties broken randomly
    if self.mdp.isTerminal(state):
        return None
    actions = self.mdp.getPossibleActions(state)
    if not actions:
        return None
    q_values = util.Counter()
    for a in actions:
        q_values[a] = self.getQValue(state, a)
    return q_values.argMax()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
