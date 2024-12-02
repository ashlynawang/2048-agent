# NOT USED, DID NOT SEEM TO IMPROVE PERFORMANCE BY MUCH

def simulate_parallel(states):
    with multiprocessing.Pool() as pool:
        results = pool.map(simulate_game, states)
    return results

def parallel_simulation_phase(node, num_simulations):
    states = [node.state for _ in range(num_simulations)]
    rewards = simulate_parallel(states)
    return rewards


Monte Carlo Tree Search
class Node:
    def __init__(self, state, parent=None, action=None):
        self.reward = 0.0
        self.visits = 0
        self.state = state
        self.children = []
        self.parent = parent
        self.action = action
        # self.untried_actions = [move_left, move_right, move_up, move_down]

    def is_fully_expanded(self):
        """ Check if all possible actions have been expanded (left right up down) """
        return len(self.children) == 4

    def best_child(self):
        """ Returns best child found using UCB1. """
        def ucb1(node):
            return (node.reward / node.visits) + np.sqrt(2 * np.log(self.visits) / node.visits)
        return max(self.children,  key=ucb1)


def select(node):
    while node.is_fully_expanded() and node.children:
        node = node.best_child()
    return node


def expand(node):
    actions = [move_left, move_right, move_up, move_down]
    random.shuffle(actions)
    for action in actions:
        new_state = action(node.state)
        if not np.array_equal(new_state, node.state): # only expand valid moves
            child = Node(new_state, parent=node, action=action)
            node.children.append(child)
            return child
    return node    
    action = node.untried_actions.pop(random.randrange(len(node.untried_actions)))
    new_state = action(node.state)
    if not np.array_equal(new_state, node.state):
        child = Node(new_state, parent=node, action=action)
        node.children.append(child)
        return child
    return node


def simulate(state):
    grid = state.copy()
    while not game_over(grid):
        moves = [move_left, move_right, move_up, move_down]
        move = random.choice(moves)
        new_grid = move(grid)
        if not np.array_equal(new_grid, grid):
            grid = new_grid
            add_new_tile(grid)
    return np.max(grid)


def backpropagate(node, reward):
    while node is not None:
        node.visits += 1
        node.reward += reward 
        node = node.parent


def mcts(root, iterations=100):
    for _ in range(iterations):
        leaf = select(root)
        if not leaf.is_fully_expanded():
            leaf = expand(leaf)
        reward = simulate_game(leaf.state)
        backpropagate(leaf, reward)
    
    return root.best_child() 

def mcts(root, iterations=10):
    for _ in range(iterations):
        node = root
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        if not node.is_fully_expanded():
            action = [move_left, move_right, move_up, move_down][len(node.children)] # change later to be random
            new_state = action(node.state)  
            if not np.array_equal(new_state, node.state):
                new_node = Node(new_state)
                node.children.append(new_node)
                node = new_node 
            
        
class MCTSAgent:
    def __init__(self, iterations=500):
        self.iterations = iterations

    def choose_action(self, state):
        root = Node(state)
        best_child = mcts(root, self.iterations)
        return best_child.action
# Main function to compare all move cycles

# ## in main
#     grid = init_grid()
#     agent = MCTSAgent()
#     while not game_over(grid):
#         action = agent.choose_action(grid)
#         new_grid = action(grid)
#         if not np.array_equal(grid, new_grid):
#             grid = new_grid
#             add_new_tile(grid)
        
#     print("Max Tile Achieved by MCTS:", np.max(grid))