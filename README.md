# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *Student should provide answer here*
Refers to solution.py, I summarized all in one function. The step is as follows.
1. Using "unitlist" that consists of 9+9+9+2 = 29 units, I run into each unit (In this case, each unit will be called local unit)
2. For Each local unit, because it is in term of key from dictionary, I create "unitvalue" to represent value from dictionary
3. Then, I identify each naked twins by in of each box in that local unit by check if len()==2 and there is more than one occurance by using .count()>=2
4. If there is naked twins identified, then
     a. identify naked twins value in naked_twins_value
	 b. create location list in that local unit that has naked twins values in naked_twins_location
	 c. go through box that is in local unit but not in naked_twins_location, then reduce each digit away by loop. (Use loop by each digit not two digit at once)
5. Screen naked twins across all 29 units.
6. In reduce_puzzle(values) function, insert naked_twins function AFTER eliminate(values) function but before only_choice(values) function to add naked twins strategy

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Student should provide answer here*
In this part, diagonal sudoku is considered another two units. It is created by using following codes
diagonal_1=list([x+y for x,y in zip(list(rows),list(cols))])
diagonal_2=list([x+y for x,y in zip(list(rows),sorted(list(cols),reverse=True))])
diagonal_units=[]   #Return 2 diagonal units
diagonal_units.append(diagonal_1)
diagonal_units.append(diagonal_2)
The diagonal_units will be list of two and each sublist represent diagonal box in sudoku grid.
Then in "unitlist", plus diagonal unit into list 
unitlist = row_units + column_units + square_units + diagonal_units  
Then the code will account diagonal unit as another two constraints when the code is looking in peers.
For example, peers in A1 will has 4 list of units (rowunit, boxunit, columnunit, diagonalunit) while peers in A2 will has 3 list of units (rowunit, boxunit, and columnunit)
Therefore, in eliminate and only_choice function, they will additionally account for diagonal unit as another constraints in propagation.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

