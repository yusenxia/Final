import pytest
from minesweeper import MineSweeper, Cell

def test_board_dimensions():
    game = MineSweeper(5, 6, 3)
    assert len(game.board) == 5
    assert len(game.board[0]) == 6

def test_mine_count_correct():
    game = MineSweeper(4, 4, 5)
    mines = sum(cell.mine for row in game.board for cell in row)
    assert mines == 5

def test_open_empty_cell_success():
    game = MineSweeper(5, 5, 0)
    result = game._open(2, 2)
    assert result is True
    assert game.board[2][2].opened

def test_open_mine_fail():
    game = MineSweeper(3, 3, 0) 
    game.board[0][0].mine = True  
    result = game._open(0, 0)
    assert result is False

def test_flagging_and_unflagging():
    game = MineSweeper(3, 3, 0)
    assert not game.board[1][1].flagged
    game.board[1][1].flagged = True
    assert game.board[1][1].flagged
    game.board[1][1].flagged = False
    assert not game.board[1][1].flagged

def test_in_bounds_true():
    game = MineSweeper(5, 5, 0)
    assert game._in_bounds(0, 0)
    assert game._in_bounds(4, 4)

def test_in_bounds_false():
    game = MineSweeper(5, 5, 0)
    assert not game._in_bounds(-1, 0)
    assert not game._in_bounds(5, 5)

def test_open_already_opened_cell():
    game = MineSweeper(5, 5, 0)
    game.board[2][2].opened = True
    original_opened_cnt = game.opened_cnt
    result = game._open(2, 2)
    assert result is True
    assert game.opened_cnt == original_opened_cnt

def test_adjacent_mine_count():
    game = MineSweeper(3, 3, 0)
    game.board[0][1].mine = True
    game._calc_adj()
    assert game.board[0][0].adj == 1
    assert game.board[1][1].adj == 1

def test_win_condition():
    game = MineSweeper(2, 2, 1)
    # Open all non-mine cells
    for i in range(2):
        for j in range(2):
            if not game.board[i][j].mine:
                game._open(i, j)
    assert game.opened_cnt == 3
    assert game.opened_cnt == (game.r * game.c - game.m)

