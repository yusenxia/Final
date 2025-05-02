import random
from collections import deque


class Cell:
    __slots__ = ("mine", "opened", "flagged", "adj")

    def __init__(self):
        self.mine = False
        self.opened = False
        self.flagged = False
        self.adj = 0


class MineSweeper:
    def __init__(self, rows: int, cols: int, mines: int):
        if mines >= rows * cols:
            print(f"Mine count {mines} too high for {rows}×{cols} board; setting to {rows*cols-1}.")
            mines = rows * cols - 1
        self.r, self.c, self.m = rows, cols, mines
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.opened_cnt = 0
        self._place_mines()
        self._calc_adj()

    def play(self):
        self._print_help()
        while True:
            self._draw(False)
            try:
                cmd, x, y = input("\nCommand (o/f) row col: ").split()
                x, y = int(x), int(y)
            except ValueError:
                print("Format: o 3 4  or  f 3 4")
                continue
            if not self._in_bounds(x, y):
                print("Out-of-range coordinates")
                continue

            if cmd == "o":
                if not self._open(x, y):
                    self._draw(True)
                    print("Game Over!")
                    break
            elif cmd == "f":
                self.board[x][y].flagged = not self.board[x][y].flagged
            else:
                print("Unknown command")
                continue

            if self.opened_cnt == self.r * self.c - self.m:
                self._draw(True)
                print("You Win!")
                break

    def _in_bounds(self, x, y):
        return 0 <= x < self.r and 0 <= y < self.c

    def _place_mines(self):
        placed = 0
        while placed < self.m:
            x, y = random.randrange(self.r), random.randrange(self.c)
            if not self.board[x][y].mine:
                self.board[x][y].mine = True
                placed += 1

    def _calc_adj(self):
        dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(self.r):
            for j in range(self.c):
                if self.board[i][j].mine:
                    continue
                self.board[i][j].adj = sum(
                    self.board[i + dx][j + dy].mine
                    for dx, dy in dirs
                    if self._in_bounds(i + dx, j + dy)
                )

    def _open(self, x, y):
        cell = self.board[x][y]
        if cell.opened or cell.flagged:
            return True
        cell.opened = True
        self.opened_cnt += 1
        if cell.mine:
            return False
        if cell.adj == 0:
            q = deque([(x, y)])
            dirs = [
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            ]
            while q:
                cx, cy = q.popleft()
                for dx, dy in dirs:
                    nx, ny = cx + dx, cy + dy
                    if self._in_bounds(nx, ny):
                        ncell = self.board[nx][ny]
                        if not ncell.opened and not ncell.mine:
                            ncell.opened = True
                            self.opened_cnt += 1
                            if ncell.adj == 0:
                                q.append((nx, ny))
        return True

    def _draw(self, reveal):
        print("\n   " + " ".join(f"{j:2}" for j in range(self.c)))
        for i in range(self.r):
            print(f"{i:2} ", end="")
            for j in range(self.c):
                c = self.board[i][j]
                if c.opened or reveal:
                    if c.mine:
                        ch = "*"
                    elif c.adj > 0:
                        ch = str(c.adj)
                    else:
                        ch = " "
                elif c.flagged:
                    ch = "F"
                else:
                    ch = "#"
                print(f"{ch:2}", end="")
            print()

    def _print_help(self):
        print("=== Command-Line Minesweeper ===")
        print("Commands:")
        print("  o row and col -> open a cell")
        print("  f row and col -> tag flag on a cell")
        print("Coordinates start at 0.")


def main():
    try:
        r, c, m = map(int, input("Enter rows cols mines (default 9 9 10): ").split())
    except ValueError:
        r, c, m = 9, 9, 10
    game = MineSweeper(r, c, m)
    game.play()


if __name__ == "__main__":
    main()
