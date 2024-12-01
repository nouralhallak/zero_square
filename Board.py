import copy
import keyboard
from collections import deque
from queue import PriorityQueue

class Board :

    n = None
    m = None
    board= None
    def __init__(self, m , n, blocks, boxs, points):
        self.m = m
        self.n = n
        self.blocks = blocks  
        self.boxs = boxs      
        self.points = points  
        self.board = [['-' for _ in range(n)] for _ in range(m)]
    def print (self):
        self.board = [['-' for _ in range(self.n)] for _ in range(self.m)]
        for block in self.blocks:
            i= block[0]
            j= block[1]
            self.board[i][j] = '@'
        for index , box in enumerate(self.boxs):
            i= box[0]
            j= box[1]
            self.board[i][j] = '#' + str(index)
        for index, point in enumerate(self.points):
            i= point[0]
            j= point[1]
            self.board[i][j] = '*' + str(index)
        for row in self.board:
                print(" ".join(map(str, row)))    

    def get_possible_states(self):
        possible_states = []

        for direction in ['up', 'down', 'left', 'right']:
            if self.can_move(direction):
                new_state = self.move(direction)
                possible_states.append(new_state)

        return possible_states
            
    def can_move(self,box,direction):
        if direction == 'right':
            i= box[0]
            j= box[1]
            j += 1
            new_position = (i,j)
            if new_position in self.blocks:
                return False
            if new_position in self.boxs:
                return False
            if j >= self.n:
                return False
            return True
    
        elif direction == 'left':
            i= box[0]
            j= box[1]
            j -= 1
            new_position = (i,j)
            if new_position in self.blocks:
                return False
            if new_position in self.boxs:
                return False
            if j < 0:
                return False
            return True
    
        elif direction == 'up':
            i= box[0]
            j= box[1]
            i -= 1
            new_position = (i,j)
            if new_position in self.blocks:
                return False
            if new_position in self.boxs:
                return False
            if i < 0:
                return False
            return True
    
        elif direction == 'down':
            i= box[0]
            j= box[1]
            i += 1
            new_position = (i,j)
            if new_position in self.blocks:
                return False
            if new_position in self.boxs:
                return False
            if i >= self.m:
                return False
            return True


    def move(self,direction):
        if direction == 'right':
            for index , box in enumerate(self.boxs):
                i= box[0]
                j= box[1]
                can_move = self.can_move(box,direction)
                while can_move:
                    j +=1
                    box = (i,j)
                    print(box)
                    if box == self.points[index]:
                        self.boxs.pop(index)
                        self.points.pop(index)
                        break
                    can_move = self.can_move(box,direction)
                    self.boxs[index] = box
        
        elif direction == 'left':
            for index , box in enumerate(self.boxs):
                i= box[0]
                j= box[1]
                can_move = self.can_move(box,direction)
                while can_move:
                    j -=1
                    box = (i,j)
                    print(box)
                    if box == self.points[index]:
                        self.boxs.pop(index)
                        self.points.pop(index)
                        break
                    can_move = self.can_move(box,direction)
                    self.boxs[index] = box

        elif direction == 'up':
            for index , box in enumerate(self.boxs):
                i= box[0]
                j= box[1]
                can_move = self.can_move(box,direction)
                while can_move:
                    i -=1
                    box = (i,j)
                    print(box)
                    if box == self.points[index]:
                        self.boxs.pop(index)
                        self.points.pop(index)
                        break
                    can_move = self.can_move(box,direction)
                    self.boxs[index] = box       

        elif direction == 'down':
            for index , box in enumerate(self.boxs):
                i= box[0]
                j= box[1]
                can_move = self.can_move(box,direction)
                while can_move:
                    i +=1
                    box = (i,j)
                    print(box)
                    if box == self.points[index]:
                        self.boxs.pop(index)
                        self.points.pop(index)
                        break
                    can_move = self.can_move(box,direction)
                    self.boxs[index] = box           
    def check_winning(self):
      if len(self.boxs) == 0 and  len(self.points) == 0:
            return True
      return False
    
class NextState:
    def __init__(self, initial_board):
        self.initial_board = initial_board
        self.visited_states = set()

    def generate_next_states(self):
        possible_states = []
        
        for direction in ['up', 'down', 'left', 'right']:
            new_board = copy.deepcopy(self.initial_board)
            new_board.move(direction)  
            state_hash = self.board_state_hash(new_board)  
            if state_hash not in self.visited_states:
                self.visited_states.add(state_hash)
                possible_states.append(new_board)
        
        return possible_states
    def board_state_hash(self, Board):
        state_representation = (tuple(sorted(Board.boxs)), tuple(sorted(Board.points)))
        return hash(state_representation)

class Algorithm:
    def __init__(self, initial_board):
        self.initial_board = initial_board

    def bfs(self):
        print("Running BFS algorithm...")
        queue = deque([(self.initial_board, [])]) 
        visited = set()
        initial_hash = self.board_state_hash(self.initial_board)
        visited.add(initial_hash)

        while queue:
            current_board, path = queue.popleft()
            if current_board.check_winning():
                print("Solution found using BFS!")
                print('Steps Number : ' , len(path))
                for step in path:
                    print('\n*****************************************************\n')
                    step.print()
                return path
            next_state_generator = NextState(current_board)
            next_states = next_state_generator.generate_next_states()

            for next_board in next_states:
                state_hash = self.board_state_hash(next_board)
                if state_hash not in visited:
                    visited.add(state_hash)
                    queue.append((next_board, path + [next_board]))
                    next_board.print()

        print("No solution found using BFS.")
        return None

    def dfs(self):
        print("Running DFS algorithm...")
        stack = [(self.initial_board, [])] 
        visited = set()
        initial_hash = self.board_state_hash(self.initial_board)
        visited.add(initial_hash)

        while stack:
            current_board, path = stack.pop()
            if current_board.check_winning():
                print("Solution found using DFS!")
                print('Steps Number : ' , len(path))
                for step  in path:
                    print('\n*****************************************************\n')
                    step.print()
                return path
            next_state_generator = NextState(current_board)
            next_states = next_state_generator.generate_next_states()

            for next_board in next_states:
                state_hash = self.board_state_hash(next_board)
                if state_hash not in visited:
                    visited.add(state_hash)
                    stack.append((next_board, path + [next_board]))
                    next_board.print()
                    
        print("No solution found using DFS.")
        return None
    
    def ucs(self):
        print("Running UCS algorithm...")
        priority_queue = PriorityQueue()
        cost = 0 
        priority_queue.put((cost, id(self.initial_board) , self.initial_board, []))
        visited = set()
        initial_hash = self.board_state_hash(self.initial_board)
        visited.add(initial_hash)

        while not priority_queue.empty():
            cost , _ , current_board , path = priority_queue.get()
            if current_board.check_winning():
                print("Solution found using UCS!")
                print('Steps Number : ' , len(path))
                for step in path:
                    print('\n*****************************************************\n')
                    step.print()
                return path
            next_state_generator = NextState(current_board)
            next_states = next_state_generator.generate_next_states()

            for next_board in next_states:
                state_hash = self.board_state_hash(next_board)
                if state_hash not in visited:
                    visited.add(state_hash)
                    priority_queue.put((cost + 1, id(next_board), next_board, path + [next_board]))
                    next_board.print()

        print("No solution found using UCS.")
        return None
    
    def A_Star(self,heuristic):
        print("Running A_Star algorithm...")
        priority_queue = PriorityQueue()
        cost = 0 
        priority_queue.put((cost, id(self.initial_board) , self.initial_board, []))
        visited = set()
        initial_hash = self.board_state_hash(self.initial_board)
        visited.add(initial_hash)

        while not priority_queue.empty():
            cost , _ , current_board , path = priority_queue.get()
            if current_board.check_winning():
                print("Solution found using A_Star!")
                print('Steps Number : ' , len(path))
                for step in path:
                    print('\n*****************************************************\n')
                    step.print()
                return path
            next_state_generator = NextState(current_board)
            next_states = next_state_generator.generate_next_states()

            for next_board in next_states:
                state_hash = self.board_state_hash(next_board)
                if state_hash not in visited:
                    visited.add(state_hash)
                    priority_queue.put((cost + heuristic, id(next_board), next_board, path + [next_board]))
                    next_board.print()

        print("No solution found using A_Star.")
        return None
    
    def calculate_heuristic(self, point):
        for block in self.blocks:
            distance = abs(point[0] - block[0]) + abs(point[1]-blocks[1])
            heuristic = heuristic + distance

    def board_state_hash(self, board):
        state_representation = (tuple(board.boxs), tuple(board.points))
        return hash(state_representation)

class PlayGame:
    def __init__(self, board):
        self.board = board

    def start(self):
        print("Choose a mode:")
        print("1. User Mode")
        print("2. Algorithm Mode (BFS/DFS/UCS/a_star)")
        mode = input("Enter 1 or 2: ").strip()

        if mode == '1':
            self.user_mode()
        elif mode == '2':
            algo_choice = input("Choose an algorithm (bfs/dfs/ucs/a_star): ").strip().lower()
            if algo_choice in ['bfs', 'dfs', 'ucs','a_star']:
                self.algorithm_mode(algo_choice)
            else:
                print("Invalid choice. Please enter 'bfs' or 'dfs' or 'ucs' or 'a_star'.")
        else:
            print("Invalid mode selected. Please restart the game and choose again.")    

    def user_mode(self):
        self.board.print()
        
        def on_arrow_key_event(event):
            if event.event_type == keyboard.KEY_DOWN:
                if event.name in ['up', 'down', 'left', 'right']:
                    self.board.move(event.name)
                    self.board.print()
                    if self.board.check_winning():
                        print("You won the game!")
                        keyboard.press('q')
                        # keyboard.unhook_all() 
        
        keyboard.hook(on_arrow_key_event)
        print("User Mode: Use arrow keys to move boxes. Press 'q' to quit.")
        keyboard.wait('q')
        # keyboard.wait('esc')

    def algorithm_mode(self, algorithm_type):
        algorithm = Algorithm(self.board)
        if algorithm_type == 'bfs':
            solution_path = algorithm.bfs()
        elif algorithm_type == 'dfs':
            solution_path = algorithm.dfs()
        elif algorithm_type == 'ucs':
            solution_path = algorithm.ucs()
        elif algorithm_type == 'a_star':
            solution_path = algorithm.A_Star()    
        else:
            print("Invalid algorithm type. Choose 'bfs' or 'dfs' or 'ucs' or 'A_Star'.")
            return

# blocks = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),
#             (1,0),(1,6),
#             (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6)]1
# boxs = [(1,1)]
# points = [(1,5)]    
blocks = [(0,0),(0,1),(1,1),(0,2),(0,3),(0,4),(0,5),(1,5),(2,5),(0,6),(1,6),(2,6),(0,7),(1,7),(0,8),(1,8),(0,9),(1,9),(0,10),(1,10),
            (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
            (6,1),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,10),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,10),
            (2,9),(3,9),(2,10),(3,10),(4,10),(5,10),(5,9),
            (4,4),(4,5),(4,6)]
boxs = [(1,2),(6,2)]
points = [(4,9),(2,7)]
# Board = Board(3,7, blocks, boxs, points)
Board = Board(8,11, blocks, boxs, points)
Board.print()

next_state_generator = NextState(Board)
possible_states = next_state_generator.generate_next_states()
print(f"Generated {len(possible_states)} possible next states:")

game = PlayGame(Board)
game.start()

