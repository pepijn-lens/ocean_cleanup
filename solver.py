import openpyxl

# Directions: 0: N, 1: NE, 2: E, 3: SE, 4: S, 5: SW, 6: W, 7: NW
DELTAS = [
    (-1, 0),  # 0: N
    (-1, 1),  # 1: NE
    (0, 1),   # 2: E
    (1, 1),   # 3: SE
    (1, 0),   # 4: S
    (1, -1),  # 5: SW
    (0, -1),  # 6: W
    (-1, -1)  # 7: NW
]

DISTANCES = [5, 7, 5, 7, 5, 7, 5, 7]
GRID_ROWS = 20
GRID_COLS = 30
MAX_DAYS = 5
MAX_DIST_PER_DAY = 50

class State:
    def __init__(self, r, c, direction, day, dist, collected, path, score):
        self.r = r
        self.c = c
        self.direction = direction
        self.day = day
        self.dist = dist
        self.collected = collected
        self.path = path
        self.score = score
        self.finished = False

    def __lt__(self, other):
        return self.score < other.score

def load_grid():
    # Read directly from the Excel file
    filename = "toc-challenge-data.xlsx"
    wb = openpyxl.load_workbook(filename)
    sheet = wb.active
    grid = []
    
    # The grid is 20 rows x 30 columns
    for row in range(1, 21):
        row_data = []
        for col in range(1, 31):
            cell_value = sheet.cell(row=row, column=col).value
            # Default to 0 if empty or None
            if cell_value is None:
                row_data.append(0)
            else:
                row_data.append(int(cell_value))
        grid.append(row_data)
    return grid

def is_valid_pos(r, c):
    return 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS

def is_on_boundary(r, c):
    return r == 0 or r == GRID_ROWS - 1 or c == 0 or c == GRID_COLS - 1

def get_next_pos(r, c, direction):
    dr, dc = DELTAS[direction]
    return r + dr, c + dc

def solve():
    grid = load_grid()
    
    # Start: T11 -> Col 19, Row 10
    start_r, start_c = 10, 19
    start_dir = 2 # East
    
    initial_plastic = grid[start_r][start_c]
    initial_collected = {(start_r, start_c)}
    
    initial_state = State(
        r=start_r,
        c=start_c,
        direction=start_dir,
        day=0,
        dist=0,
        collected=initial_collected,
        path=[[]], 
        score=initial_plastic
    )
    
    beam = [initial_state]
    beam_width = 50
    final_states = []
    max_iterations = 300
    
    for i in range(max_iterations):
        next_beam = []
        
        # Optimization: use a dict to keep only best score for same (r, c, dir, day, dist) signature?
        # Might reduce diversity. Beam search usually keeps distinct paths.
        
        print(f"Iteration {i}, Beam size: {len(beam)}")
        
        for state in beam:
            if state.finished:
                final_states.append(state)
                continue
            
            moves_tried = False
            
            # 1. Try moving (-1, 0, 1)
            for move in [-1, 0, 1]:
                ndir = (state.direction + move) % 8
                cost = DISTANCES[ndir]
                
                # Check budget
                if state.dist + cost > MAX_DIST_PER_DAY:
                    continue
                
                # Check bounds
                nr, nc = get_next_pos(state.r, state.c, ndir)
                if not is_valid_pos(nr, nc):
                    continue
                
                # Valid move within day
                new_collected = state.collected.copy()
                added_score = 0
                if (nr, nc) not in new_collected:
                    added_score = grid[nr][nc]
                    new_collected.add((nr, nc))
                
                new_path = [d[:] for d in state.path]
                new_path[-1].append(move)
                
                new_state = State(
                    r=nr,
                    c=nc,
                    direction=ndir,
                    day=state.day,
                    dist=state.dist + cost,
                    collected=new_collected,
                    path=new_path,
                    score=state.score + added_score
                )
                next_beam.append(new_state)
                moves_tried = True
                
            # 2. Try Ending Day
            # Allowed if:
            # a) No moves possible (forced) OR
            # b) We have moved significantly (e.g. > 40km) (optional choice)
            
            # Also CHECK CONSTRAINT: Days 0,1,2,3 CANNOT end on boundary.
            # Day 4 (5th day) CAN end on boundary.
            
            can_end_day_pos = True
            if state.day < MAX_DAYS - 1: # Not the last day
                if is_on_boundary(state.r, state.c):
                    can_end_day_pos = False
            
            if can_end_day_pos:
                # Allow ending day if forced (moves_tried is False) OR voluntarily if dist >= 40
                # Note: If moves_tried is True, we effectively branched. 
                # Now we add the branch where we STOP.
                
                if not moves_tried or state.dist >= 40:
                    # Transition to next day
                    if state.day < MAX_DAYS - 1:
                        new_path = [d[:] for d in state.path]
                        new_path.append([]) 
                        
                        new_state = State(
                            r=state.r,
                            c=state.c,
                            direction=state.direction,
                            day=state.day + 1,
                            dist=0,
                            collected=state.collected.copy(),
                            path=new_path,
                            score=state.score
                        )
                        next_beam.append(new_state)
                    else:
                        # End of Day 5
                        # Boundary check for Day 5 is relaxed (can end anywhere)
                        state.finished = True
                        final_states.append(state)

        if not next_beam:
            break
            
        # Prune
        # Sort by score
        next_beam.sort(key=lambda s: s.score, reverse=True)
        beam = next_beam[:beam_width]
        
        if len(beam) == 0:
            break

    if final_states:
        best_state = max(final_states, key=lambda s: s.score)
        print("Best Score:", best_state.score)
        
        print("\n--- Solution ---")
        for day_idx, day_moves in enumerate(best_state.path):
            dist = 0
            # Re-calculate dist to verify
            # (Logic to verify dist is correct)
            print(f"{' '.join(map(str, day_moves))}")
            
    else:
        print("No solution found.")

if __name__ == "__main__":
    solve()

