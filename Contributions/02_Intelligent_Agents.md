
**Author:** Beatrice Occhiena s314971. See [`LICENSE`](https://github.com/beatrice-occhiena/Computational_intelligence/blob/main/LICENSE) for details.
- institutional email: `S314971@studenti.polito.it`
- personal email: `beatrice.occhiena@live.it`
- github repository: [https://github.com/beatrice-occhiena/Computational_intelligence.git](https://github.com/beatrice-occhiena/Computational_intelligence.git)

**Resources:** These notes are the result of additional research and analysis of the lecture material presented by Professor Giovanni Squillero for the Computational Intelligence course during the academic year 2023-2024 @ Politecnico di Torino. They are intended to be my attempt to make a personal contribution and to rework the topics covered in the following resources.
- [https://github.com/squillero/computational-intelligence](https://github.com/squillero/computational-intelligence)
- Stuart Russel, Peter Norvig, *Artificial Intelligence: A Modern Approach* [3th edition]

.

.

# Agents and Environments

### Agent
An agent in the context of AI is any entity that can perceive its environment and take actions based on those perceptions. Agents can vary widely in their design, their degree of complexity, and their level of "intelligence". They can be as simple as a reflex machine or as complex as a human being.

> Our goal for this part of the course is to derive a set of design principles for creating successful agents, which can be genuinely considered intelligent.

- The **agent function** is a crucial aspect of an agent's design. It defines the *relationship between the agent's perceptual inputs and the actions it takes in response to those inputs*. In essence, it's a rulebook that guides the agent's behavior. It's important to note that the agent function is just a *mathematical description*. 📖..

- The **agent program** is the actual, *concrete implementation of this function*. It's the software or hardware that carries out the instructions laid out in the agent function. The agent program brings the agent's decision-making process to life, and its design can have a significant impact on the agent's performance. ⚙️..

### Task Environment
The task environment is the environment in which the agent operates. It's the part of the real world that the agent perceives and acts upon. It's important to note that the task environment is not the same as the real world. It's a simplified version of reality, designed to focus on the aspects that are relevant to the agent's decision-making process.

The task environment is defined by the following components:
- 🌍 **external environment**
- 👁️ **sensors** -> perceive the environment 
- 🫳🏻 **actuators** -> act upon the environment 
- 📈 **performance measure** -> evaluates the success of an agent's actions 

### Agent Types
- **Simple reflex agents** are the simplest type of agent. They select actions based on the `current percept`, ignoring the rest of the percept history. They don't have any memory of the past. They're also unable to consider the future consequences of their actions. They're only capable of *responding reflexively* to the current situation. 
  - e.g. a thermostat 🌡️..
- **Model-based reflex agents** are similar to simple reflex agents, but they're equipped with an internal state that depends on the `percept history`. They're able to consider the past when selecting actions. They're also able to consider the future consequences of their actions.
  - e.g. a game-playing agent 🎮..
- **Goal-based agents** These agents aim to achieve a `specific set of desired outcomes`, and they evaluate their performance based on whether they achieve these goals. They make decisions by considering which actions are most likely to lead to goal attainment. They're able to consider the future consequences of their actions. 
  - e.g. a chess-playing agent ♟️..
- **Utility-based agents** These agents, on the other hand, consider not just achieving specific goals but also the `overall desirability` or utility of different outcomes. They assign numeric values (utilities) to various states or situations, indicating how preferable each state is. These agents make decisions to maximize expected utility. They're able to consider the future consequences of their actions, and most importantly to compare and evaluate the desirability of those consequences. 
  - e.g. a self-driving car agent 🚗..
- **Learning agents** All the previous agent types can be further classified as either learning or non-learning agents. Learning agents are able to `improve their performance over time` by considering past experiences. They're able to learn from their mistakes and adapt their behavior accordingly.
  - e.g. a recommendation system 📺..

### Variations in Task Environments
- **Fully observable vs. partially observable** The environment is fully observable if the agent's sensors give it access to the `complete state` of the environment *at each point in time*. The environment is partially observable if the agent's sensors only give it access to a `partial state`. The agent may not be able to observe certain aspects of the environment, or it may not be able to observe the environment at all times.
  - board game 🎲..
  - self-driving car 🚗..
- **Deterministic vs. stochastic** The environment is deterministic if the next state of the environment is `completely predictable`, since it is determined by the current state and the actions selected by the agent. The environment is stochastic if the next state of the environment is `only partially determined` by the current state and the actions selected by the agent. The environment may be stochastic due to the presence of *random events* or because the agent's sensors are *imprecise*.
  - board game 🎲..
  - wheather forecast 🌦️..
- **Episodic vs. sequential** Episodic environments involve isolated interactions where the agent's actions `don't depend on previous interactions`. Sequential environments, on the other hand, have a series of actions that depend on prior ones.
  - factory robot 🤖..
  - recommendation system 📺..
- **Static vs. dynamic** The environment is static if it doesn't `change while the agent is deliberating`, dynamic otherwise.
  - board game 🎲..
  - self-driving car 🚗..
- **Discrete vs. continuous** The environment is discrete if there are a `finite number of distinct states`, continuous if there are infinite possibilities.
  - tic-tac-toe ✖️..
  - stock market 📈..
- **Single-agent vs. multi-agent** The environment is single-agent if there's `only one agent` operating in it. When there are `multiple agents` operating in the same environment, thay coexist possibly competing or collaborating with each other.
  - puzzle solving game 🧩..
  - logistics 🚚..
- **Known vs. unknown**  Some environments are fully understood and can be modeled accurately. Others are unknown or only partially known, introducing a degree of uncertainty.
  - board game 🎲..
  - self-driving car 🚗..

### Designing an Agent Program
There isn't a one-size-fits-all solution for agent-program design. Instead, a range of basic designs exists. These designs differ in terms of how they handle information and make decisions. Factors like *efficiency, compactness, and flexibility* influence the choice of agent-program design.

The selection of an agent-program design relies on the environment in which the agent functions. Unique environments may require specific designs to enhance the agent's performance. 
- An autonomous `vacuum cleaner` agent 🧹.. -> operates in a simple, predictable environment.
- A `self-driving car` agent 🌳..🚶🏻🚦...🚗 -> operates in a complex, ever-changing environment.

 > An exhaustive and accurate task environment specification is crucial for the design of an effective agent. It's important to consider all the relevant aspects of the environment, and to avoid including irrelevant aspects (abstraction).

 ### Environment Representation
 The way the agent represents and interacts with the environment plays a critical role in its decision-making processes.
  - **Atomic** The environment is atomic if the agent can `perceive and act on it as a single entity`. The agent doesn't need to consider its internal structure and can treat it as a black box. Such environments are typically simple and predictable => high level of abstraction. 📦..
  - **Factored** A factored representation goes a step further by breaking down the states into a `vector of attribute values`. More detailed and structured understanding of the environment => more sophisticated decision-making and reasoning. 📊..
  - **Structured** In this representation, states include `objects`, each of which may have `attributes` of their own, as well as `relationships` with other objects. Structured representations are especially valuable in environments with intricate interactions and dependencies. Most expressive and detailed understanding of the environment => most sophisticated yet complex reasoning. 📚..