import random

class cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.is_mine = False
        self.is_flagged = False
        self.is_revealed = False
        self.neighbor_mines = 0
        self.status = "\u2588" # "\u2588":filled, " ":empty, "F":flag, "X":mine


    def reveal(self, board, recursive=False):
        self.is_revealed = True
        if self.is_mine and not recursive:          ###
            self.status = "X"
            return False
        elif self.neighbor_mines == 0:
            self.status = " "
            for cell in board.adjacent_cells(self.row, self.col):
                if not cell.is_revealed:
                    cell.reveal(board, recursive=True)          # this should be a problem, issue with numbering.
            return True
        elif self.neighbor_mines > 0:
            self.status = str(self.neighbor_mines)
            return True
        
    def toggle_flag(self):
        self.is_flagged = not self.is_flagged
        if self.is_flagged:
            self.status = "F"
        else:
            self.status = "\u2588" 
        
class board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = self.create_board()
        self.directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

    def create_board(self):
        return [[cell(x, y) for y in range(self.cols)] for x in range(self.rows)]
    
    def valid_index(self, row, col):
        return row >= 0 and col >= 0 and row < self.rows and col < self.cols

    def __getitem__(self, index):
        row, col = index
        if not self.valid_index(row, col):
            return None
        else:
            return self.board[row][col]

    def __setitem__(self, index, value):
        row, col = index
        self.board[row][col] = value

    def cell_gen(self):
        for row in self.board:
            for cell in row:
                yield cell

    def adjacent_cells(self, row, col):
        for dx, dy in self.directions:
            if self.valid_index(row+dx, col+dy):
                yield self.board[row+dx][col+dy]

    def neighboring_mines(self, row, col):
        count = 0
        for cell in self.adjacent_cells(row, col):
            if cell.is_mine:
                count += 1
        return count

    def empty_cells(self):
        for cell in self.cell_gen():
            if cell.neighbor_mines == 0:
                yield cell

    def unrevealed_count(self):
        count = 0
        for cell in self.cell_gen():
            if not cell.is_revealed:
                count += 1
        return count
        
                                    # Need to implement flag system "f 0 0"?

class Minesweeper:
    def __init__(self, rows, cols, **kwarg):
        self.rows = rows
        self.cols = cols
        area = self.rows * self.cols
        self.mine_count = kwarg.get('mines', int(0.0002*(area)**2 +0.0938*(area) + 0.8937) ) # getting this from a reddit thread 
        self.board = board(rows, cols)

        self.game_status = "In Progress"

        self.mines = self.place_mines(self.mine_count)        
        self.count_neighbor_mines()

    def game_loop(self):
        self.display_board()
        while not self.game_status == "Game Over":
            row_col = input("Enter row & Col: ")
            if row_col.lower() in ["q",'quit','exit']: break
            if row_col.lower() == "r": 
                self.reveal_all()
                row_col = "0 0"
            try:
                row, col = row_col.split()                 
                self.check_cell(int(row), int(col))
                self.display_board()
                self.check_status()
            except:
                print("Invalid input. Please try again.")
                continue

        if input("Play again? (y/n) ") == "y":
            self.__init__(self.rows, self.cols, mines = self.mine_count)
            self.game_loop()

        pass

    def reveal_all(self):
        for cell in self.board.cell_gen():
            cell.reveal(self.board)

    def place_mines(self, mine_count):
        locs = []
        while len(locs) < mine_count:
            (x,y) = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if (x,y) not in locs: 
                locs.append((x,y))

        for (x,y) in locs: 
            self.board[x, y].is_mine = True
    

        return locs
    
    def count_neighbor_mines(self):
        for cell in self.board.cell_gen():
            cell.neighbor_mines = self.board.neighboring_mines(cell.row, cell.col)

    def display_board(self):
        output = []
        border = "-"*(self.cols*4+1)

        output.append(border)
        
        for i in range(self.rows):
            row = "| "
            for j in range(self.cols):
                val = self.board[i, j].status
                row += f"{val} | "
            output.append(row)
            output.append(border)

        print("\n".join(output))
        return "Board displayed"

    def check_cell(self, row, col):
        print("Checking cell", row, col)
        if self.board[row, col].reveal(self.board):
            return True
            
        else: 
            print("Game Over")
            self.game_status = "Game Over"
            return False
        
    def check_status(self):
        if self.mine_count == self.board.unrevealed_count():
            print("You win!")
            self.game_status = "Game Over"
        pass
        
            


# Example usage
if __name__ == "__main__":
    game = Minesweeper(9, 9) #, 3)
    game.game_loop()
