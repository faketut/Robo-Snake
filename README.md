# Snake AI Project

## Overview

The Snake AI project involves the implementation of various strategies utilizing the Breadth-First Search (BFS) algorithm to guide the snake in a game scenario to locate food, avoid collisions, and maximize safety.

### BFS Algorithm
- **Functionality:** Searches nodes around the initial state (starting point) until reaching the target node (food).
- **Traversal:** Explores adjacent points around the snake's head, avoiding obstacles (snake body and walls) and minimizing revisits for efficiency.

### Rear End Collision & Virtual Snake Exploration
- **Safety Considerations:** Defines safety based on the ability for the snake head to follow the snake tail during movements.
- **Strategy:** Allows the snake to follow its tail when unable to find a path to food; utilizes virtual snake simulations to determine safety before actual food consumption.

### Prioritizing Avoidance of Food Conflicts
- **Optimization:** Seeks a safe path from snake head to tail without leaving gaps, enhancing the snake's ability to find food.
- **Selection Criteria:** Prioritizes selecting the farthest grid from food while ensuring a clear path back to the snake's tail during movement.

## References

The project draws inspiration from the Snake AI strategy detailed in [Hawstein's Snake AI post from 2013](http://www.hawstein.com/posts/snake-ai.html).

## Details
Firstly, place the coordinates of the food in the queue. As long as the queue is not empty, pop the head off the queue. Then, place the four points around the snake's head in the queue and repeat the operation until it covers the entire board. During the traversal process, it should be noted that: 1. The snake's body and walls cannot be accessed. In order to improve efficiency, if there are overlapping grids that have been accessed, they do not need to be accessed again. After the entire cycle ends, we obtain the shortest path between the snake head and the food.

- **Rear end collision+virtual snake exploration:**
Firstly, we should define "security". What is a security state? We found that when the snake head moves one grid, it corresponds to the position of the snake tail moving out of one grid. Therefore, as long as the snake head can follow the snake tail, it is considered safe. Therefore, when the small snake eats its food, it can check that there is a pathway between the snake head and the snake tail, which is considered safe
Based on the above conclusion, we can let the small snake follow its tail when it cannot find a path to eat. When a small snake can eat food, first create a virtual snake simulation and use the BFS algorithm to eat the food along the shortest path. When the virtual snake can find the path between the snake head and the snake tail after eating the food, it is safe to eat. Then, we send the real small snake to eat the food. On the contrary, when the virtual snake finds that it cannot find the path connecting its tail after eating food, it is unsafe to eat it. We let the real snake follow the snake's tail for a step. Until the virtual snake finds a safe state, let the real little snake move.

- **Prioritize staying away from food conflicts:**
We also can find that it's difficult for the snake to find a safe path to eat food from the snake's head to the snake's tail, without creating many gaps. Therefore, when asking a real snake to find its tail, two things need to be met:
1. Find an empty space around the snake head, and once the snake head reaches this space, it can still find a path connecting to the tail
2. If conditions 1 is met, prioritize selecting the grid farthest from the food (Calculate the Manhattan distance between two points)

