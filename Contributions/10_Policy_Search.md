**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Lessons: 30/11/2023, 04/12/2023, 05/12/2023, 11/12/2023, 12/12/2023, 14/12/2023, 18/12/2023
- Stuart Russel, Peter Norvig, *Artificial Intelligence: A Modern Approach* [3th edition]
- Richard S. Sutton, Andrew G. Barto, *Reinforcement Learning: An Introduction* [2nd Edition]
- Useful site to better understand Monte Carlo method [analyticsvidhya.com](https://www.analyticsvidhya.com/blog/2018/11/reinforcement-learning-introduction-monte-carlo-learning-openai-gym/)

.

.

# Policy Search

## Table of Contents
- [Introduction](#introduction)
- [Learning Classifier Systems](#learning-classifier-systems)
  - [Implementation](#implementation)
  - [Rule Evaluation](#rule-evaluation)
- [Reinforcement Learning](#reinforcement-learning)
  - [Key concepts](#key-concepts)
    - [Agent-Environment Interaction](#agent-environment-interaction)
    - [Task types](#task-types)
    - [Policy and Expected Return](#policy-and-expected-return)
  - [Caveats](#caveats)
  - [Model-based vs Model-free](#model-based-vs-model-free)
  - [Markov Decision Process](#markov-decision-process)
  - [Q-Learning](#q-learning)
    - [Considerations](#considerations)
  - [Monte Carlo Methods](#monte-carlo-methods)
  - [Q-L vs MC](#q-l-vs-mc)
  - [Final Considerations](#final-considerations)
  
## Introduction
> 🎯 The objective is to directly learn an optimal `black box policy function` that maps **each state** to the **best action** to perform in that state.
- In some simple cases, similar to a **dictionary**: for each word (state) there is a definition (action). $\pi(s) = a$
- For games like chess, where the number of states is huge, it is impossible to store all the states and their corresponding actions. In these cases, we can use a `function approximator` to estimate the policy function.

## Learning Classifier Systems
Learning Classifier Systems (LCS) are a family of `rule-based` trigger-action machine learning algorithms that combine:
- a `learning component` (performing either supervised learning, **reinforcement learning**, or unsupervised learning), that interacts with the environment and gets a reward.
- a `discovery component` (e.g. a **genetic algorithm**), that is used to evolve the rules guided by the reward.

$IF \; condition \; THEN \; action \; =>[reward] => \; fitness$ 

They were first introduced by *John Holland* in 1976. Nowadays, there is *no real use* of LCS in the field of AI, but they are still interesting to study because they are a good example of how to combine different techniques to solve a problem.

### Implementation
👨🏽‍👩🏻‍👧🏻‍👦🏽 **Population of rules**: the current knowledge of the system, incrementally built by the learning component.
- **Online**: no initial population, the rules are created on the fly.
- **Offline**: the population is created before the learning process starts.
- `Collaborative`: the set of rules should be able to collaborate to solve the problem, covering all the important situations.

🎭 **Bit strings**: the condition part  of the rule, that is compared to the state of the environment.

### Rule Evaluation
> Evaluating a rule is not straightforward, because the condition part of the rule can be satisfied by many different states.
- **Credit assignment problem**: how to assign the reward to the rules that contributed to the reward.
  - Only `responsible` rules that are active when the reward is received should be rewarded/penalized.
  - `Inactive` rules should be removed from the population.
- **Coverage problem**: how to ensure that the rules cover all the important situations.
  - `Subsumption`: a rule is removed if it is covered by another rule that is more general and has a higher fitness.

## Reinforcement Learning
Reinforcement Learning (RL) is a type of machine learning that allows an agent to learn how to behave in an 🌳🌲**environment**🌲🌳 by performing actions and receiving feedback in the form of **rewards**🪙. The agent learns to achieve a goal in an uncertain, potentially complex environment.

> 🎯 The objective is to learn a policy that maximizes the (discounted) `expected cumulative reward`, i.e. not the single step reward, but the sum of the rewards that can be obtained in the **long run**!

### Key concepts

#### Agent-Environment Interaction

- An agent performs actions that modify the environment and, in return, receives a reward for each action. The state of the environment and the reward are updated with each step creating the following cycle.

  The agent:
    1. Receive an `observation` $S^A_t$ from the environment
    2. Select an `action` $A_t$ based on the observation
    3. Execute the action $A_t$ and receive a reward $R_t$

  The environment:
    1. Receive an action $A_t$ from the agent
    2. Execute the action $A_t$ and update its `state` to $S^E_{t+1}$
    3. Calculate the `reward` $R_{t}$ and send it to the agent

- **Environment State and Observability**: the state of the environment is a representation of the current situation of the environment. It is a function of the `history` of all the previous actions and observations. 

  $S_{t+1} = f(H_t)$

  The agent does not have direct access to the state of the environment, but only to the observation $S^A_t$.

  An environment is **fully observable** if the agent can directly observe all aspects of the environment ($S^A_t = S^E_t$).
  - Chess ♟️
  - Tic-tac-toe ❌⭕
  - Pacman 🐱

  In contrast, in **partially observable** environments, if the agent receives indirect information about the environment.
  - Poker 🃏
  - Self-driving car 🚗
  - Stock market 📈

- **History**: the history is the sequence of all the observations, actions and rewards received by the agent. It encapsulates the entire `trajectory` of the agent's interactions with the environment, forming a chronological record of its decision-making process.

  $H_t = A_1, O_1, R_1, ..., A_t, O_t, R_t$

#### Task types
- **Episodic tasks**: are tasks with a well-defined starting and ending point, where the agent-environment interaction breaks down into a sequence of episodes. The agent-environment interaction is divided into episodes, each of which ends in a terminal state, and the next episode starts independently of how the previous one ended.

  - Tic-tac-toe ❌⭕ (each game is an episode)
  - Chess ♟️
  - Pacman 🐱

  In many episodic tasks, the reward is significantly tied to the `outcome at the end` of the episode. This encourages the agent to develop strategies that optimize for the best outcome at the episode's conclusion, rather than immediate gains within the episode.

- **Continuing tasks**: are scenarios where the interaction between the agent and the environment doesn't have a predefined endpoint. This means the agent continues to operate indefinitely without a natural conclusion or 'final step.'

  `Infinite Expected Return`: Because there's no end, the sum of the rewards that the agent can accumulate over time could theoretically be infinite. This poses a challenge in calculating and optimizing the rewards, as there's no natural boundary to the sum.

#### Policy and Expected Return

- **Policy**: is a mapping or strategy that defines how an agent selects actions in response to observations, representing the core decision-making mechanism guiding the agent's behavior in an environment.

  $\pi: S \rightarrow A$

  A policy can be either **deterministic** or **stochastic**. A deterministic policy is a mapping from states to actions, while a stochastic policy is a mapping from states to probability distributions over actions.

  $\pi(a|s) = P[A_t = a | S_t = s]$
  
- **Expected Return**: the expected return is the sum of the rewards obtained by the agent from a given state onwards. It is a measure of the long-term value of a state, and it is used to evaluate the quality of a policy.

  $G_t = \sum_{k=t}^{T} R_{k+1}$

  > ⚠️ The expected return can be **discounted** to give more importance to the immediate rewards. Essential for `NOT episodic` tasks.

  $G_t = \sum_{k=t}^{T} \gamma^{k-t} R_{k+1}$

  where $\gamma$ is the discount factor, $0 \leq \gamma \leq 1$. 
  - When $\gamma = 0$, the agent is myopic and only considers the immediate reward (greedy policy).
  - When $\gamma = 1$, the agent is far-sighted and considers all future rewards equally.

  > ⚠️ Reward may **need to be delayed**, e.g. refueling a helicopter might prevent it from crashing later on! 🚁💥

- **Bellman Equation**: the expected return can be expressed recursively in terms of the expected return of the next state.

  $V(s) = \mathbb{E}[R_{t+1} + \gamma V(S_{t+1}) | S_t = s]$

- **Quality function**: the quality function of a policy is the expected return of the policy for each state-action pair.

  $Q^{\pi}(s, a) = \mathbb{E}[G_t | S_t = s, A_t = a, \pi]$

### Caveats
- **Exploration vs Exploitation**: the agent must balance the need to explore the environment to find better policies and the need to exploit the current knowledge to obtain rewards.
- **Dense vs Sparse Rewards**: the agent may receive rewards at every step or only at the end of the episode.
- **Credit Assignment Problem**: the agent must understand precisely which actions led to the reward.
- **Sample Efficiency**: the minimum number of samples required to learn a good policy.

### Model-based vs Model-free
- **Model-based**: the agent `learns a model of the environment` and uses it to plan its actions. We can know the dynamic of the environment.
  - The model is used to predict the next state and the reward given the current state and action.
- **Model-free**: the agent learns a policy without learning a model of the environment. The agent learns to map states to actions directly `exclusively from trial and error`.

### Markov Decision Process
A Markov Decision Process (MDP) is a mathematical framework for modeling decision-making in fully-observable environment where outcomes are:
1. partly random (e.g. dice roll, stock prices, etc.)
2. partly under the control of a decision maker (the agent's actions).

> 💡 **Markov Property**: the `future is independent of the past` given the present => MEMORYLESS
  - The state captures all the relevant information from the history!
  - The state is a sufficient statistic of the future.

$p(s', r | s, a) = P[S_{t+1} = s', R_{t+1} = r | S_t = s, A_t = a]$

### Q-Learning
Q-Learning is a RL algorithm that learns to make decisions by learning the quality of actions in a given state. It is a **temporal difference learning** algorithm, that learns by comparing the current estimate of the quality of an action with the estimate of the quality of the action in the next state.
- Model-free: it does not require a model of the environment.
- Model-based: it learns a model of the environment.

The update of the Q-table is performed after each action, using the following formula:

$Q^*_{t+1}(s, a) = (1-\alpha)Q^*_{t}(s, a) + \alpha [R_{t+1} + \gamma Q^*_{t}(s', a')]$

where:
- $Q^*_{t}(s, a)$ is the quality of the action $a$ in the state $s$ at time $t$
- $\alpha$ is the learning rate
- $\gamma$ is the discount factor
- $R_{t+1}$ is the reward received after performing action $a$ in state $s$
- $s'$ is the next state
- $a'$ is the action that maximizes the quality in the next state

#### Considerations

> 💡 Somewhat **similar to John Holland's LCS**, that now can be seen as a compact way to approximate the Q-table (even if incredibly slow).
- LCS -> understandable list of rules
- Q-Learning -> a table of state-action values

> ❓ Are we actually `LEARNING` anything? **NOT REALLY!**
- We are just memorizing a long list of state-action pairs and their `values in a table`.
- Caveat: With Q-Learning, the "learned" policy is **not directly transferable** to other problems, even very similar ones.

### Monte Carlo Methods
Monte Carlo methods are a class of computational algorithms that rely on `repeated random sampling` to obtain numerical results. In the context of RL, Monte Carlo methods are used to estimate the value of a state-action pair by **averaging the returns** that are observed after visiting that state-action pair.

The update of the Q-table is performed after each episode, using the following formula:

$Q^*_{t}(s, a) = Q^*_{t-1}(s, a) + \alpha [G_t - Q^*_{t-1}(s, a)]$

where:
- $G_t$ is the return obtained after visiting the state-action pair $s, a$
- $\alpha$ is the learning rate

### Q-L vs MC
- **Learning Speed**: Q-Learning learns faster than Monte Carlo methods due to updating estimates based on maximum future reward, while Monte Carlo waits until the episode's end.
- **Bias and Variance**: Q-Learning has bias as it assumes current Q-values are correct, while Monte Carlo methods have no bias but high variance due to diverse returns.
- **Memory Requirement**: Q-Learning needs less memory than Monte Carlo as it stores only current state and action, while Monte Carlo stores all states and actions in an episode.
- **Policy Requirement**: Q-Learning is off-policy, learning optimal policy regardless of agent's current policy; Monte Carlo is on-policy, learning only the current policy.


### Final Considerations
Reinforcement learning is an intresting idea, but it is almost only applied to game settings. It is not very efficient in terms of:
- sample efficiency
- computational resources
- time

> 💡 **Deep Q-Learning**: using a deep neural network to approximate the action-value function.

