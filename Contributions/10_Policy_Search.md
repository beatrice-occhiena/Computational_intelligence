**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Lessons: 30/11/2023, 04/12/2023, 05/12/2023, 11/12/2023
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
  - [Caveats](#caveats)

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
- **Agent and Environment Interaction**: an agent performs actions that modify the environment and, in return, receives a reward for each action. The state of the environment and the reward are updated with each step creating the following cycle.

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

- **Policy**: is a mapping or strategy that defines how an agent selects actions in response to observations, representing the core decision-making mechanism guiding the agent's behavior in an environment.

  $\pi: S \rightarrow A$

  A policy can be either **deterministic** or **stochastic**. A deterministic policy is a mapping from states to actions, while a stochastic policy is a mapping from states to probability distributions over actions.

  $\pi(a|s) = P[A_t = a | S_t = s]$

- **Expected Return**: the expected return is the sum of the rewards obtained by the agent from a given state onwards. It is a measure of the long-term value of a state, and it is used to evaluate the quality of a policy.

  $G_t = \sum_{k=t}^{T} R_{k+1}$

  > ⚠️ The expected return can be **discounted** to give more importance to the immediate rewards.

  $G_t = \sum_{k=t}^{T} \gamma^{k-t} R_{k+1}$

  where $\gamma$ is the discount factor, $0 \leq \gamma \leq 1$. 
  - When $\gamma = 0$, the agent is myopic and only considers the immediate reward (greedy policy).
  - When $\gamma = 1$, the agent is far-sighted and considers all future rewards equally.

  > ⚠️ Reward may **need to be delayed**, e.g. refueling a helicopter might prevent it from crashing later on! 🚁💥

### Caveats
- **Exploration vs Exploitation**: the agent must balance the need to explore the environment to find better policies and the need to exploit the current knowledge to obtain rewards.
- **Dense vs Sparse Rewards**: the agent may receive rewards at every step or only at the end of the episode.
- **Credit Assignment Problem**: the agent must understand precisely which actions led to the reward.
- **Sample Efficiency**: the minimum number of samples required to learn a good policy.

44:17 11/12/2023