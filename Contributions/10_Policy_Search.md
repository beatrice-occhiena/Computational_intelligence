**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Lessons: 30/11/2023, 4/12/2023
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
18:08