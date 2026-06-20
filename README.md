# Path Finder

A desktop pathfinding game built with Python and Tkinter. Path Finder turns the A* search algorithm into something you can play against: trace the shortest route between two points on a grid by hand, then see if you matched what A* actually found.

## Contributors

- [@talal](https://github.com/talal-11)
- [@ahmed](https://github.com/Ah65med)
- [@neha](https://github.com/nehalq)
- [@shayan](https://github.com/sfxdeve)

## Overview

The app opens to a main menu with two modes:

- **Play** — a timed challenge. The game randomly places a start point, an end point, and 10 obstacles on a 10x10 grid. Click cells to trace your guess at the shortest path, then press **Space** to check it against the A* solution. You get 3 tries.
- **Practice** — a sandbox. Click to place your own start point, end point, and obstacles, then press **Space** to watch A* solve the grid and highlight the shortest path in green.

## Features

- A* pathfinding with a Manhattan-distance heuristic, restricted to 4-directional movement (no diagonals)
- Two game modes: a scored "Play" challenge and a freeform "Practice" sandbox
- Randomly generated start/end points and obstacles in Play mode, with a minimum distance enforced between start and end
- Click-to-mark interface for tracing a path, with click-to-unmark support
- Path validation that checks both length (no shortcuts past the optimal path) and adjacency (no skipped cells)
- Visual feedback: correct paths and the A*-computed path are highlighted in green; failed attempts in Play mode are shown in red alongside the correct path
- Retro arcade-style UI using the "Press Start 2P" font

## Controls

| Action | Input |
|---|---|
| Mark / unmark a cell | Left-click |
| Submit your path for checking | Spacebar |
| Return to main menu | Close the game window |

## Color Legend

| Color | Meaning |
|---|---|
| Yellow | Start point |
| Orange | End point |
| Gray | Obstacle |
| Blue | Cell you've marked as part of your path |
| Green | Correct / shortest path |
| Red | Your incorrect path (Play mode, after final try) |
| White | Empty, unmarked cell |

## How Play Mode Works

1. A 10x10 grid is generated with a random start, a random end (guaranteed to be at least `rows // 2` cells away from the start), and 10 random obstacles.
2. Click cells to build your path from start to end. Click again to unmark a cell.
3. Press **Space** to submit. Your path is automatically reordered so the start and end anchor the sequence correctly.
4. The game compares your path to the actual A* shortest path:
   - **Win** — your path matches the shortest path's length and every step is adjacent to the next (no diagonal or skipped moves).
   - **Lost** — your path is the right length but skips a cell (not a valid step-by-step route).
   - **Try Again** — your path is the wrong length and you still have tries remaining; the board resets so you can try again.
   - **Lost (final)** — your path is the wrong length and you're out of tries; your attempt is shown in red next to the correct path in green.
5. You have 3 tries per round.

## How Practice Mode Works

1. The grid starts empty.
2. Click once to place the start point (yellow).
3. Click again to place the end point (orange).
4. Every click after that places an obstacle (gray) on an empty cell.
5. Press **Space** to run A* and see the shortest path highlighted in green.

## Algorithm Notes

- Pathfinding is implemented with a textbook A* search: a cost-so-far map, a Manhattan-distance heuristic, and a priority queue ordered by `cost + heuristic`.
- Movement is restricted to the four cardinal directions (up, down, left, right) — no diagonal steps.
- The search is capped at 10,000 iterations as a safety limit against runaway loops on larger grids.
- If no path exists between start and end, both modes report this explicitly rather than failing silently.

## Requirements

- Python 3.x
- Tkinter (included with most standard Python installations)
- No third-party packages required

For the intended retro look, install the **Press Start 2P** font system-wide; if it isn't installed, Tkinter will silently substitute your system's default font.

## Running the Game

```bash
python main.py
```

This opens the main menu, from which you can launch either Play or Practice mode.

## Project Structure

A single-file application (`main.py`) containing:

- `PriorityQueue` — minimal list-based priority queue used by the A* search
- `astar`, `heuristic` — the pathfinding logic
- `are_cells_adjacent`, `is_path_valid` — path validation helpers used in Play mode
- `GamePlay` — the scored challenge mode
- `GamePractice` — the freeform sandbox mode
- `Main` — the main menu and window management

## Known Limitations

- Grid size is fixed at 10x10 for both modes (hardcoded in `Main`)
- No persistence — scores and grids reset every time you return to the main menu
- No diagonal movement support
- Designed and tested for desktop use; window sizing assumes a standard monitor resolution
