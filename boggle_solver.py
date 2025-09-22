""" Name: Lauren Oliver, SID: 003100456 """

class Boggle:
    def __init__(self, grid, dictionary):
        """
        Constructor for Boggle class.
        
        Parameters:
        grid (list[list[str]]): 2D array representing the Boggle board.
        dictionary (list[str]): List of valid words.
        
        Initializes:
        self.solutions (set): Stores unique words found during search.
        """
        self.grid = grid
        self.dictionary = dictionary
        self.solutions = set()   # store unique words found

    def setGrid(self, grid):
        """
        Setter method to update the game grid.

        Parameters:
        grid (2D array of strings): New NxN board of letters
        """
        self.grid = grid
        self.solutions = set()  # reset solutions when grid changes

    def setDictionary(self, dictionary):
        """
        Setter method to update the dictionary.

        Parameters:
        dictionary (list of strings): New list of valid words
        """
        self.dictionary = dictionary
        self.solutions = set()  # reset solutions when dictionary changes

    def getSolution(self):
        """
        Main solver method to find all valid words in the grid.
        
        Returns:
        list[str]: Sorted list of unique words found on the board.
        """
        # Ensure inputs exist
        if not self.grid or self.dictionary is None:
            return []

        size = len(self.grid)

        # Handle empty grid case
        if size == 0:
            return []

        # Grid must be square (NxN)
        if any(len(row) != size for row in self.grid):
            return []

        # Normalize everything to lowercase
        self.grid, self.dictionary = self._normalize_input(self.grid, self.dictionary)

        # Validate grid (all alphabetic tiles)
        if not self._grid_is_valid(self.grid):
            return []

        # Build prefix set + dictionary set for fast lookup
        prefix_set, word_set = self._make_prefix_lookup(self.dictionary)

        visited = [[False] * size for _ in range(size)]

        # Explore from each grid position
        for r in range(size):
            for c in range(size):
                self._search("", r, c, visited, prefix_set, word_set)

        return sorted(self.solutions)

    def _normalize_input(self, grid, dictionary):
        """
        Convert grid letters and dictionary words to lowercase.
        
        Parameters:
        grid (list[list[str]]): Original grid.
        dictionary (list[str]): Original dictionary.
        
        Returns:
        tuple: (lowered_grid, lowered_dict)
        """
        lowered_grid = [[cell.lower() for cell in row] for row in grid]
        lowered_dict = [word.lower() for word in dictionary]
        return lowered_grid, lowered_dict

    def _grid_is_valid(self, grid):
        """
        Check that the grid contains only alphabetic strings.
        
        Parameters:
        grid (list[list[str]]): 2D Boggle board to validate.
        
        Returns:
        bool: True if all cells are strings and alphabetic, False otherwise.
        """
        for row in grid:
            for cell in row:
                if not isinstance(cell, str) or not cell.isalpha():
                    return False
        return True

    def _make_prefix_lookup(self, dictionary):
        """
        Build prefix set and word set from the dictionary for DFS pruning.
        
        Parameters:
        dictionary (list[str]): List of valid words.
        
        Returns:
        tuple: (prefix_set, word_set)
            prefix_set (set[str]): All possible prefixes of dictionary words.
            word_set (set[str]): Full words from the dictionary.
        """
        prefix_set = set()
        word_set = set(dictionary)
        for word in dictionary:
            for i in range(1, len(word) + 1):
                prefix_set.add(word[:i])
        return prefix_set, word_set

    def _search(self, current, row, col, visited, prefix_set, word_set):
        """
        Perform depth-first search (DFS) from a given cell to find words.
        
        Parameters:
        current (str): Current accumulated word along DFS path.
        row (int): Row index of the current cell.
        col (int): Column index of the current cell.
        visited (list[list[bool]]): Tracks cells already used in current path.
        prefix_set (set[str]): Set of valid prefixes for pruning DFS.
        word_set (set[str]): Set of valid words.
        """
        n = len(self.grid)

        # stop if outside grid or already used
        if row < 0 or row >= n or col < 0 or col >= n or visited[row][col]:
            return

        new_word = current + self.grid[row][col]

        # prune if no word starts with this sequence
        if new_word not in prefix_set:
            return

        visited[row][col] = True

        # valid dictionary word, must be >=3 letters
        if new_word in word_set and len(new_word) >= 3:
            self.solutions.add(new_word)

        # explore all 8 neighbors
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                self._search(new_word, row + dr, col + dc, visited, prefix_set, word_set)

        visited[row][col] = False  # backtrack


def main():
    grid = [["T", "W", "Y", "R"],
            ["E", "N", "P", "H"],
            ["G", "St", "Qu", "R"],
            ["O", "N", "T", "A"]]

    dictionary = ["art", "ego", "gent", "get", "net", "new", "newt", "prat",
                  "pry", "qua", "quart", "quartz", "rat", "tar", "tarp",
                  "ten", "went", "wet"]

    game = Boggle(grid, dictionary)
    print(game.getSolution())


if __name__ == "__main__":
    main()
