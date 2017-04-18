assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]
boxes = cross(rows, cols)      #Return list of 81 grids
row_units = [cross(r, cols) for r in rows]  #Return 9 row 
column_units = [cross(rows, c) for c in cols]   #Return 9 column
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]  #Return 9 squares
diagonal_1=list([x+y for x,y in zip(list(rows),list(cols))])
diagonal_2=list([x+y for x,y in zip(list(rows),sorted(list(cols),reverse=True))])
diagonal_units=[]   #Return 2 diagonal units
diagonal_units.append(diagonal_1)
diagonal_units.append(diagonal_2)
unitlist = row_units + column_units + square_units + diagonal_units  #Sum of 4 unit types; around 9+9+9+2 = 29 units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)   #List of 81 grids. Each represent row unit, column unit, square unit, and diagonal unit
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)    #List of 81 grids. Each represent 20+ peers
print("123")
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    for unit in unitlist:   #for each 29 unit of 4 unit type
        unitvalue=[]
        unitvalue=[values[box] for box in unit] #Create value list for search                     
        for box in unit:              
            if len(values[box])==2 and unitvalue.count(values[box])>=2: #Identify naked twins of each box in each local unit
                naked_twins_value=values[box]     #Store 2 digits found #Naked twin could occurs more than once in one unit
                naked_twins_location=[]           #Find location of box that has naked value      
                for findpreservebox in unit:      #Identify location  
                    if values[findpreservebox]==naked_twins_value:
                        naked_twins_location.append(findpreservebox)                
                for delbox in unit:                 #Search to delete across unit
                    if delbox not in naked_twins_location:
                        for digitdel in naked_twins_value:    #Delete digit by digit
                            values[delbox]=values[delbox].replace(digitdel,'')
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_list=list(grid)
    assert isinstance(grid_list, list)==True
    values=[]
    all_digits='123456789'
    for c in grid_list:
        if c == '.':
            values.append(all_digits)
        else:
            values.append(c)
    return dict(zip(boxes,values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values=[]
    for box in values.keys():#Identify solved box location
        if len(values[box])==1:
            solved_values.append(box)
    for box in solved_values:   #For each solved box
        digit=values[box]       #Get that digit
        for peer in peers[box]:  #For each peers from that (each) solved box
            values[peer] = values[peer].replace(digit,'')   #Set value of peers be removed by digit
    return values

def only_choice(values):
    for unit in unitlist:   #Going in each 27 row units, column units, and square units
        for digit in '123456789':   #For each digits of 1 to 9; Suppose 3
            dplaces=[]
            for box in unit:     #for each box in unit of 9 box (box is A1,A2,A3,...)
                if digit in values[box]:        #if digit (suppose 3) is identified in that box
                    dplaces.append(box)         #Fill box location in dplaces; add it as list using append
            if len(dplaces)==1:                 #If list length=1, place it with digits. Notably, len when use to list will return amount of list
                values[dplaces[0]] = digit      #Input digit in values dict if there is only one box associate with it
    return values

def reduce_puzzle(values):
    stalled = False     #Set up boolean variable
    while not stalled:
        # Check how many boxes have a determined value by looking how many box has integer len ==1
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Further eliminate using naked twins strategy
        values = naked_twins(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value; Again. Looking at how many box has interger len ==1
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]: #For each of integers in the cell that has fewest possibilities
        new_sudoku = values.copy()  #Create new sudoku
        new_sudoku[s] = value       #Assign the integer (value=8) to location(G2) to that new sudoku
        attempt = search(new_sudoku)    #When it ultimately search to the most, there is only two choice; Answer found or False. 
    #The key is in reduce_puzzle that detect zero such that if wrong number(value in values[s]) is insert in attempt, 
    #it will result in zero box in some area that will ultimately cause code to be Fault.
        if attempt:     #If attempt is false, do nothing. Loop until it found answer
            return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid = grid_values(grid)
    return search(grid)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
