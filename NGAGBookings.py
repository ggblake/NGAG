import sys
import random
import pandas as pd
from IPython.display import display
import IPython
import docplex.cp


import sys
import docplex

from docplex.cp.model import *
from sys import stdout

#number = int(input("Enter a number <7: "))
number =random.randint(1,6)

GRNG = range(6)
ARTISTS = ['Blake', 'Keith','Moran','Sterling','Valliant/Harding','Simpson']
MONTHS = ['Jan-Feb','Mar-Apr','May-Jun','Jul-Aug','Sep-Oct', 'Nov-Dec']
VENUES = ['Salamanders', 'Bistro', 'Cooperators', 'Reckmans','Country Ways','Library']
SUDOKU_PROBLEM_1 = ( (number, 0, 0,  0, 0, 0),
                     (0, 0, 0,  0, 0, 0),
                     (0, 0, 0,  0, 0, 0),
                     (0, 0, 0,  0, 0, 0),
                     (0, 0, 0,  0, 0, 0),
                     (0, 0, 0,  0, 0, 0),
                   )

print(SUDOKU_PROBLEM_1[0][0])

try:
    import numpy as np
    import matplotlib.pyplot as plt
    VISU_ENABLED = True
except ImportError:
    VISU_ENABLED = False

# In[9]:

def print_grid(grid):
    """ Print Sudoku grid """
    for l in GRNG:
        if (l > 0) and (l % 3 == 0):
           stdout.write('\n')
        for c in GRNG:
            v = grid[l][c]
            stdout.write('   ' if (c % 3 == 0) else ' ')
            stdout.write(str(v) if v > 0 else '.')
        stdout.write('\n')


def draw_grid(values):
   
    fig, ax = plt.subplots(figsize =(4,4))
    min_val, max_val = 0, 6
    R =  range(0,6)
    for l in R:
        for c in R:
            v = values[c][l]
            s = " "
            if v > 0:
                s = str(v)
            ax.text(l+0.5,5.5-c, s, va='center', ha='center')
        ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.set_xticks(np.arange(max_val))
    ax.set_yticks(np.arange(max_val))
    ax.grid()
    plt.show()
    


def display_grid(grid, name):
    stdout.write(name)
    stdout.write(":\n")
    if VISU_ENABLED:
        draw_grid(grid)
    else:
        print_grid(grid)


problem = SUDOKU_PROBLEM_1
mdl = CpoModel(name="Sudoku")
grid = [[integer_var(min=1, max=6, name="C" + str(l) + str(c)) for l in GRNG] for c in GRNG]
      
    


# In[14]:
for l in GRNG:
    mdl.add(all_diff([grid[l][c] for c in GRNG]))


# In[15]:

for c in GRNG:
    mdl.add(all_diff([grid[l][c] for l in GRNG]))


# In[16]:


def getRandom():
    Start = 0
    Stop = 6
    limit = 6
# List of random integers chosen from a range
    r = random.sample(range(Start, Stop), limit)
    #print(r)
    return r


# In[17]:

i = getRandom()
for l in GRNG:
    for c in GRNG:
        v = problem[l][c]
        if v > 0:
            grid[l][c].set_domain((i[0],i[0]))   


# In[18]:
print("\nSolving model....")
msol = mdl.solve(TimeLimit=10)


# In[19]:
#display_grid(problem, "Initial problem")
if msol:
    sol = [[msol[grid[l][c]] for c in GRNG] for l in GRNG]
    stdout.write("Solve time: " + str(msol.get_solve_time()) + "\n")
    #display_grid(sol, "Solution")
else:
    stdout.write("No solution found\n")


# In[20]:

df = pd.DataFrame(sol,index =VENUES, columns = MONTHS)
df = df.applymap(str)

# In[21]:


def getArtist(index):
    return ARTISTS[int(index)-1]


for m in MONTHS:
    for v in VENUES:
        index =df.at[v,m]
        df.at[v,m]=getArtist(index)

# In[134]:


import tempfile
import win32api
import win32print

#win32api.ShellExecute (0, "print","figure1.pdf", None, ".", 0)


# In[27]:


import os
#os.startfile('figure1.pdf')


from prettytable import PrettyTable
x = PrettyTable()
column_names = ["Venue","Jul-Aug", "Sep-Oct", "Nov-Dec"]
x.add_column(column_names[0],VENUES)
for i in range(3):
    x.add_column(column_names[i+1],df.loc[:,MONTHS[i]])
#print(x)

print(x.get_string())
text_file = open("Output.txt", "w")
text_file.write("Rnd:" + str(number) +'\n'+ x.get_string())
text_file.close()
#win32api.ShellExecute (0, "print","Output.txt", None, ".", 0)
import subprocess as sp
programName = "notepad.exe"
fileName = "Output.txt"
sp.Popen([programName, fileName])