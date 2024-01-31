
# Review Received

## Lab2 Review by Alessandro Chiabodo S309234

### Overall 
The code looks solid and the algorithm is very well done, starting from the definition of the main rules to the training, and the results are almost unbeatable agents.
I can only say that your work is almost perfect!

### General Annotations
- The upper bound $k$ on the number of objects that can be removed in a turn is correctly implemented in all the agents, and it is possible to see that the win rate of certain players changes by changing K
- The evolutionary algorithm is correctly implemented in the form of ($\mu/\rho$ , $\lambda$)-ES. It would have been possible to try using a variable mutation rate and crossover rate to prefer exploration at the beginning of training and exploitation at the end. 
- The code is also very well documented and explained. It is generally easy to read and understand.

## Lab2 - Nim using ES strategy - Giovanni Bordero s313010

 The code is very easy to read and understand, the explanations in the markdown boxes help to understand both the code and the main idea behind the code.
A mandatory mention for the graphics, which provide a better understanding of the simulation. 

### Code Annotation 
- the ($\mu/\rho$ , $\lambda$)-ES is very well implemented, the only small defect that i can find is the static definition of mutation_rate and crossover_rate and the test done only on that parameters without trying to show other setup.
-  All details well implemented and good intuition the use of the ts [condition,position,actions] for the Rules.

## Peer review Lab 2 - Dimitri Masetta, s306130

### Preface
Where to start from, your code is very well documented and really easy to read, allowing anyone to easily understand your intentions. You have made an amazing job in that regards, well done!!
Let's now analyze more in details the two tasks.
### Task 2.1 - Expert System 
There is little to say about this, you nailed its implementation; using the optimal move in every case except for the situation that you have defined of scarcity, in which there is only one row with more than one matchstick.
I also really liked the implementation of other companion agent, which can improve learning in the task 2.2 by comparing the ES to agents with different playstyles.
### Task 2.2 - Evolution Strategy
Starting from the ruleset, I appreciate your idea for the definition of the ruleset using also a condition to enable the activation of the rule, nice work. Given your innovative approach towards the ruleset and the new knowledge about GP, I can imagine an improved version of your agent able to define more intricate rules.
For the Evolution Strategy itself, it is generally correct and well implemented, but there are some points where improvements are possible:

- In the parent selection(5.1) you come with a sorted population from the survival selection(5.3) and then you perform a top slice of the populations, in this way you obtain purely deterministic parent selection in contrast with the standard random parent selection that is usually exploited in ES. This does not affect the functioning of the agent but can lead to premature convergence, as you lose that part of randomness that give at every memeber of the population a chance to be choose.
- The section in which you do the self-adaptation(5.4) must be moved before the mutation, because otherwise you lose the correlation between sigma and the fitness, as the fitness will be calculated on the values based on the old sigma.
- You have described your code as a comma strategy but in the survival selection(5.3) you have implemented a plus strategy.

## Lab9 Peer Review by stefbracio

The code is well organized and explained in detail. I really liked the idea of implementing a dictionary and a cache to minimize the number of fitness calls, unlike most of the solutions that only focused on the evolutionary side of the problem. It makes your solution stand out and it's a really smart idea.
After that, I like that you explored different strategies for mutation and offspring generations. Looking at the shape of your plots (particularly for problem instances 5 and 10) I see that the fitness function returns the same value for long intervals of time. This could suggest that you're not exploring the solutions space in an optimal way. You could try to implement some kind of strategy to enhance exploration, as for example an island-based system or heavier mutations on the genome.
Overall it's a really good project, well done!

## Lab10 Peer Review by lfmvit

Hi, I took a look at your code for lab10 and here are my toughts about it:

The code is well-documented with comments explaining each part of the code and providing a clear understanding of the logic and purpose of each function or method, nothing seems to be left to guesses, i really appreciated the effort since it makes it very easy to review it, this is also true for what concerns the use of graphical plots, that provide plenty of immediate insights on the effectiveness of the learning process.

For the first part I liked the fact that you separated the performance tests at various amount of steps on the training without shooting a large number of epochs in the first place, the results for 50k steps against a random player are very good in both cases of starting positions (as first or second player).

The part on symmetry exploit strategy is very interesting even though you stated that it is not completely operative it is indeed an aspect that is worth to be investigated for the final project of the course (or at least it seems to me 🧐​).

Overall a great job, good luck for future works!

## Lab10 Review - Claudio Savelli (S317680)

Hi Beatrice!!! Seeing several lab 10 works, I found yours and, having found it very interesting, I decided to make it a review.

First of all, I wanted to congratulate you on the neatness of the notebook, which allows, also thanks to its descriptive comments, to understand the code easily without a README. The methods are written clearly and are easy to comprehend. I also found the emojis to print the board very pretty, and I thank you because I did not know about this feature of Jupyter that I will use in the future!

In addition, I wanted to emphasize how the theoretical explanations you carry out along the notebook are not only useful for an immediate and easy understanding of the code but also turn your work into a tool that can teach the application of the Monte-Carlo method in Reinforcement Learning even to those who are novices in the field! In fact, not only are the explanations extremely clear and concise, but you perfectly point out all the positive and negative aspects of applying this method to any reinforcement learning approach. Excellent work!

I also found very useful the two graphs you proposed, which show how the win rate varies as the number of training games played varies. This shows easily the difference in when our agent does or does not start the game first.

To conclude, the most interesting part of the code, in my opinion, is the one related to 'Symmetry Recognition'. I have also carried it out with a different approach. In my proposed method, I transformed each training match played the trajectory of the match into four equivalent trajectories, rotating the board 90 degrees each time. In such a way, the four trajectories generated for each match are used for training. This method was possible because of the simplicity of the problem, but in this way, the space occupied by the dictionary is not reduced, which is the case in your solution.

As for your request, I could not find an immediate solution to your problem, which seems to make sense the way you try to return to the canonical state. I am sorry ☹

I think you did a great job, and I enjoyed reading it and being able to review it. Congratulations!

## Lab10 peer review Ruben Tetamo s317569

Hi, I made a look at your code and I want to congratulate with you for the clearness and the results that you've reached.

Your implementation of Montecarlo learning works very well and the comments that you inserted make the code easy the comprehend. Emoticons and plots contribute to a very pretty output look. I've noticed also a very good use of class programming in python.

About the simmetry part, I would suggest you to not create from scratch a new subclass, adding again new methods to get actions and to update q values. Personally I would only focus on modifying just the self.q_values inside the MonteCarloPlayer in order to accept only one state for all the ones that are simmetrical to it. You should end up having a only a total of 765 unique game-state according to this paper (http://www.egr.msu.edu/~kdeb/papers/k2007002.pdf) that I reccomend you to read, (the second paragraph, in particular).

## Work on my part
> I've always tried to adapt the strategies proposed by my classmates in the following labs. I especially liked the idea about the symmetry recognition, so I implemented the suggested strategies in the final project.

# Review Given

## Lab2 to Alessandro Chiabodo S309234

### Overall Feedback
The code is well-structured, and the evolutionary algorithm for Nim players appears solid. Well done!

### Annotations
#### K Parameter Consideration
Ensure K is considered consistently. Check:
- Winning move when only 1 column remains.
- Handle cases when no optimal moves are found.

#### SimulativePlayer Optimization
Your `number_wins` method involves creating deep copies of the game state and repeatedly playing random moves until the game ends. The repeated simulation of matches can be very computationally expensive, particularly when it's used in the evolutionary process for fitness evaluation.

## Lab2 to Hosseinkakavand1376

Hello everyone 👋🏻 First of all, well done with your lab! These are my personal comments on some issues I found here and there. I hope they will be helpful in possibly improving your solution ✨.

### Not optimal ruled-based agent
When the game is near the end, we must pay attention to the case in which there is only one row with more than one object. 

| Row | Objects | Binary |
| --- | --- | --- |
| 0 | 🪙 | 001 |
| 1 | 🪙 | 001 |
| 2 | 🪙 🪙 | 010 |

> ⚠️ In this case, choosing to set the next `nim-sum` to 0 would be a losing move! 

I suggest you to change our optimal strategy, exploiting the fact that a player can remove objects from only one row at a time.
1. The number of remaining rows is even $\implies$ we want to remove entirely the abundant row
2. The number of remaining rows is odd $\implies$ we want to leave only one object in the abundant row

### Ineffective Bias Calculation
The `bias` calculation in the `evolved_strategy` function doesn't seem to have any practical impact on the strategy's behavior. 
- The value resulting from `bias = (param + 1) / 2`  is not used in any meaningful way within the function.

### Considerations on the Evolutionary Process
The evolutionary process aims to find the best value for the evolving parameter to optimize strategy performance. However, if the strategy's behavior is not influenced by the evolving parameter, the evolutionary process might not be effectively exploring the space of possible strategies.

In the end, it seems to me that your strategy is primarily driven by the nim-sum condition, so I suggest you to consider exploring alternative strategies for future EA-agents.

## Lab9 to Claudio Savelli 
Hi Claudio,
First and foremost, congratulations on your exceptional efforts in tackling this lab. Your work stands out as one of the most comprehensive and organized solutions I've come across. Here are the aspects that impressed me the most:

### Comparison of Different Strategies
Your approach to the black-box optimization problem with multiple instances is nothing short of perfect. I appreciate that you not only experimented with various strategies but also took the extra step to create summary tables for a clear overview of each result. Fantastic job!

### Memoization Option
It's great that your algorithm incorportes an option for memoization. This feature is invaluable in significantly reducing the number of fitness evaluations, especially in scenarios with a high number of repeated evaluations.

### Segregation Islands Strategy
The addition of a segregation islands strategy to the standard island model is a thoughtful touch. It introduces both **diversity** and **adaptability** by segregating islands that have become too similar, effectively preventing premature convergence.

While your work is truly commendable, I have a couple of suggestions for further enhancement:

### Comments on Strategies and Predictions
Consider adding comments throughout your code to clarify the plan behind the chosen strategies and any anticipated outcomes. This could really serve as valuable guidance for other students looking to replicate or adapt your approach in future labs.

### Experiment Results Presentation
While your work is truly commendable, providing a brief summary or discussion of the experiment results would be the cherry on top. Explaining any observed trends or patterns during the algorithm's performance on different problem instances could offer valuable insights.

Overall, your work is truly remarkable! Keep up the excellent work, and I look forward to seeing more of your contributions.

## Lab9 to Gabriele Lucca

Hi Gabriele,
Great job on tackling Lab 9! Your script implementing the island model for genetic algorithms is well-structured and insightful. Here's what stood out to me:

### Clarity in Explanation
Your introductory section provides a clear and concise overview of the island model and its purposes, both in exploration and exploitation. It's an excellent reference for other stundents that want to understend your strategy.

### Parameter Control
I appreciate the clarity in defining and explaining the parameters such as migration frequency, the number of migrants, and others. Especially in dealing with a black-box optimization task, it is very convenient to potentially customize the script and try different options.

### Functionality and Implementation
The implementation of the island model is well-done, and your use of data classes for `Individuals` adds clarity to the structure of the code. The functions for crossover and mutation are appropriately defined, contributing to the overall readability.

Here are a couple of suggestions for improvement:

### Introducing Memoization
In the current implementation, the code lacks a memoization mechanism for fitness values of the same genome, implying that fitness is recalculated for individuals in each generation. Introducing a memoization strategy could greatly enhance performance by reducing redundant fitness evaluations and promote diversity.

- For example, in my code, to avoid testing more than once the same individual, I used a `dictionary` to keep track of the *genomes* already evaluated. This way, I can check if a potential individual with an equal genome has already been evaluated, and if so, discard it. 

### Experimenting with Diverse Strategies
Take into account the potential for boosting the algorithm's effectiveness by exploring a variety of mutation and selection strategies. This exploration becomes particularly valuable in the context of black-box optimization problems where the underlying fitness function is unknown. You could also insist on different ways for self-adaptation.

### Results Presentation
Consider providing a summary or discussion of the results for each optimization problem. Adding a brief interpretation of the outcomes, or even a graph of some sort, could further enhance the completeness of your work. It would provide at a glance the efficiency and goodness of the strategy adopted, particularly useful for an optimisation task.

Overall, well done!


## Lab10 to Antonio Ferrigno

Hi Antonio 😊,

Great job on completing the lab! I've thoroughly reviewed your code and strategy, and here are my thoughts:

### General
I commend you for using different classes and keeping your code well-organized and concise. The structure is clear and easy to follow.

### Training
#### Rewards Focused on Positive Reinforcement
Your code primarily uses rewards of 1 for wins, 0.5 for draws, and -10 for invalid moves. I interpreted the lack of a specific penalty for losses as a design choice, since the algorithm relies on the cumulative reward signal to guide the learning process.

#### Invalid Moves Handling
As for invalid moves, I don't really understand why you added that possibility, since you already filtered out invalid actions in the valid_actions method. This could be seen as an extra layer of caution to handle unexpected cases, but if you're confident that the valid_actions method is properly filtering out valid moves, you could potentially simplify the step method.

Personally, I think it's definitely better to avoid them directly with a preliminary check like you did. Of course, this is a more deterministic and rule-based approach, but it should lead to more efficient learning, since the agent won't waste time exploring obviously undesirable actions, since the rules of the game are well defined.

### Evaluation
#### Choosing Turns
The random starting player in the evaluation section introduces variability. This is very good, but I think it might be insightful to test the agent's performance separately when starting as player 1 and player 2 to gain a clearer understanding of its capabilities.

#### Final Results
The evaluation results, with 49 wins, 45 losses, and 6 draws out of 100 games, indicate room for improvement. Consider the following factors:
1. Ensure that the agent's exploration during evaluation is controlled appropriately. In the final testing, you may ant to set `epsilon` to 0 during evaluation to have the agent always exploit its learned policy.
2. Penalize all the moves that lead to a loss in an appropriate way.
3. Evaluate the impact of training duration. A sufficient number of episodes is crucial for convergence to an optimal strategy.

### Hyperparameter Tuning
I really appreciated your approach to testing different hyperparameters with cross-validation. It's a valuable strategy for finding the most effective configuration. Very good!

### Visualization
- The visualization of bars with different hyperparameters is a strong point in your implementation. It provides a clear overview of the impact of different settings on the agent's performance.
- However, I'm doubtful about the efficacy of a direct display of all_game_moves and the TicTacToe grid as tuples without episode divisions. Consider organizing this information by episodes for better clarity and interpretation.

Overall, your implementation shows a solid understanding of reinforcement learning concepts. With careful tuning and consideration of the mentioned points, I believe you can further enhance the agent's performance.

Keep up the good work! ✨

## Lab10 to Davide Sferrazza

Hi Davide 😊,

I just finished reviewing your project, and I must say, I am thoroughly impressed! Here are my thoughts:

### Theoretical Introduction
Your introduction to Q-Learning and Monte Carlo strategies is commendable. It provides a solid foundation for understanding the rest of your project.

### Code Organization
I really appreciated the idea of using an abstract class for different player strategies. As I stated in my notebook, I was so inspired by this approach that I've adopted the same organization in my own project!

### Comprehensive Comments
Your comments make it easy to understand the purpose and functionality of each section, which is incredibly helpful not just for reviewers like me, but for anyone who wishes to learn from or build upon your work.

### Statistical Analysis and Visualization
The function you implemented to collect game statistics is very useful. It provides valuable insights into the performance of the strategies over time. 

However, I suggest adding a graph to visually represent the training trend over time, including wins, losses, and draws. This would not only add to the visual appeal but also make the learning process and performance trends more immediately evident.

### Impressive Results
The results you've achieved with both players are fantastic. It's clear that your strategies are effective and well-implemented.

### Comparative Analysis
Your final comparison between the two strategies (Q-Learning and Monte Carlo) is a great way to wrap up your project. It gives a comprehensive view of the strengths and weaknesses of each approach and provides valuable insights into their practical applications.

### A Small Perplexity
The only area where I have some reservations is regarding the negative reward for invalid moves. I understand the reasoning behind it, but I wonder if it might be more efficient to avoid invalid moves altogether with a preliminary check. Of curse, this would be a more deterministic and rule-based approach, but I think it could streamline the learning process by preventing the agent from exploring obviously undesirable actions, given the well-defined rules of the game. However, I acknowledge that I might be missing some aspects of your strategy here.

Overall, your project demonstrates your skills and understanding of the topic. Awesome job! ✨
