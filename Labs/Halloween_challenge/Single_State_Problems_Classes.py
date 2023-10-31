"""
**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Stuart Russel, Peter Norvig, *Artificial Intelligence: A Modern Approach* [3th edition]
"""

""" 
  Single State Problems Classes
"""
class SingleState_Problem:
  
    def __init__(self, initial_state, goal_state):
      self.initial_state = initial_state
      self.goal_state = goal_state
  
    def tweak(self, state):
      """
      Returns a list of the states reachable from the given state
      """
      raise NotImplementedError
  
    def fitness(self, state):
      """
      Returns the value of the given state
      """
      raise NotImplementedError
  
    def is_goal(self, state):
      """
      Returns True if the given state is a goal state
      """
      return state == self.goal_state
    
    def neighbors(self, state):
      """
      Returns a list of the states reachable from the given state
      """
      raise NotImplementedError

class SingleState_Strategy:

  def __init__(self, n_samples):
    self.fitness_calls = 0
    self.n_samples = n_samples # Number of tweaks desired to sample the gradient

  def Random_Mutation_Hill_Climbing(self, problem, iterations):

    current_state = problem.initial_state
    current_fitness = problem.fitness(current_state)
    self.fitness_calls = 1

    for i in range(iterations):
      
      # Make a small, local change to the current solution
      new_state = problem.tweak(current_state)
      new_fitness = problem.fitness(new_state)
      self.fitness_calls += 1
      if new_fitness > current_fitness:
        current_state = new_state
        current_fitness = new_fitness

    return current_state
  
  def Steepest_Ascent_Hill_Climbing(self, problem, iterations):

    current_state = problem.initial_state
    current_fitness = problem.fitness(current_state)
    self.fitness_calls = 1

    for i in range(iterations):
      best_state = current_state
      best_fitness = current_fitness
      
      # Evaluate all the neighbors of the current solution
      for sample in range(self.n_samples):
        new_state = problem.tweak(current_state)
        new_fitness = problem.fitness(new_state)
        self.fitness_calls += 1
        if new_fitness > best_fitness:
          best_state = new_state
          best_fitness = new_fitness

      # If the best neighbor is better than the current solution, move to it
      if best_fitness > current_fitness:
        current_state = best_state
        current_fitness = best_fitness

    return current_state
  
  """
   We do Hill-Climbing for
a certain random amount of time. Then when time is up, we start over with a new random location
and do Hill-Climbing again for a different random amount of time.
  """
  def Random_Restart_Hill_Climbing(self, problem, iterations, restarts):

    best_state = problem.initial_state
    best_fitness = problem.fitness(best_state)
    self.fitness_calls = 1

    for i in range(restarts):
      random_time = random.randint(0, iterations)
      current_state = problem.random_state()
      current_fitness = problem.fitness(current_state)
      self.fitness_calls += 1

      for i in range(iterations):
        new_state = problem.tweak(current_state)
        new_fitness = problem.fitness(new_state)
        self.fitness_calls += 1
        if new_fitness > current_fitness:
          current_state = new_state
          current_fitness = new_fitness
      if current_fitness > best_fitness:
        best_state = current_state
        best_fitness = current_fitness

    return best_state