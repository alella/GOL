import sys
import matplotlib
from copy import deepcopy
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from time import sleep
from random import random, sample
import os
from datetime import datetime as dt

matplotlib.rc('axes',edgecolor='#101010')
matplotlib.rc('xtick',color='#101010')
matplotlib.rc('ytick',color='#101010')
matplotlib.rc('lines', linewidth=2)
matplotlib.rc('text', color="#aaaaaa")

population_factor = .9
iterations = 60
grid_x = 150
grid_y = 150
marker = sample(["s","o"],1)[0]
marker = "o"
graph_x_offset = int(grid_x*.250)
graph_x_offset = 0

def println(content):
    sys.stdout.write("\r"+str(content+" "*10))
    sys.stdout.flush()

class Node:
    def __init__(self,x,y,set_state=0):
        self.x_pos = x
        self.y_pos = y
        self.state=set_state
        self.color = "#101010"
        self.max_state = 20

    def neighbour_count(self, grid):
        grid_x = len(grid)
        grid_y = len(grid[0])
        neighbours = [
            (self.x_pos+1,self.y_pos-1),
            (self.x_pos+1,self.y_pos+1),
            (self.x_pos-1,self.y_pos-1),
            (self.x_pos-1,self.y_pos+1),
            (self.x_pos,self.y_pos+1),
            (self.x_pos,self.y_pos-1),
            (self.x_pos-1,self.y_pos),
            (self.x_pos+1,self.y_pos)
        ]
        count = 0
        for x_n, y_n in neighbours:
            if x_n<=1 or x_n>=grid_x:
                return 0
            if y_n<=1 or y_n>=grid_y:
                return 0
            
            if grid[x_n][y_n].state == self.max_state:
                count += 1

        return count

    def update(self, grid):
        neighbour_count = self.neighbour_count(grid)
        if self.state == self.max_state:
            if neighbour_count in [2,3]:
                self.ressurect()
            else:
                self.kill()
        else:
            if neighbour_count == 3:
                self.ressurect()
            else:
                self.kill()
 

    def ressurect(self):
        self.state = self.max_state
        self.color = "#402424"
        
    def kill(self):
        self.fade()
        self.state = max(0, self.state-1)

    def fade(self):
        color_map = {20:"#2e2424",
                     19:"#292424",
                     18:"#272024",
                     17:"#252023",
                     16:"#232022",
                     15:"#222023",
                     14:"#222023",
                     13:"#222023",
                     12:"#222022",
                     11:"#222022",
                     10:"#222022",
                     9:"#222021",
                     8:"#222021",
                     7:"#222021",
                     6:"#222020",
                     5:"#181818",
                     4:"#171717",
                     3:"#151515",
                     2:"#131413",
                     1:"#121112",
                     0:"#101010"}
        self.color = color_map.get(self.state,color_map[3])

    def __repr__(self):
        return "Node ({},{}): {}".format(self.x_pos,self.y_pos, self.state)



grid = [[0 for i in range(0,grid_y)] for j in range(0,grid_x)]
for i in range(0,grid_x):
    for j in range(0,grid_y):
        grid[i][j] = Node(i,j)

        
for i in range(0,grid_x):
    for j in range(0,grid_y):
        if random()>population_factor:
            grid[i][j].ressurect()

def fetch_draw(grid):
    x=[]
    y=[]
    c_map = []
    for i in range(0,grid_x):
        for j in range(0,grid_y):
            if grid[i][j].state:
                x.append(i)
                y.append(j)
                c_map.append(grid[i][j].color)
    return x,y,c_map

def normalize_buffer(buffer):
    max_val = max(buffer)
    min_val = min(buffer)
    delta = float(max_val - min_val)
    buffer = [8+5*(x-min_val)/delta for x in buffer]
    return buffer

def grid_update(grid, live_buffer):
    new_grid = deepcopy(grid)
    live = 0
    for i in range(0,grid_x):
        for j in range(0,grid_y):
            new_grid[i][j].update(grid)
            if new_grid[i][j].neighbour_count(grid)==1:
                if random()>.999: #mutation
                    new_grid[i][j].ressurect()
                    new_grid[i][j].color = "#5e1010"
            if new_grid[i][j].state == 20:
                live += 1

    if len(live_buffer)< grid_x:
        live_buffer.append(live)
    else:
        live_buffer = live_buffer[-(grid_x-1):]+[live]
    return new_grid, live_buffer


count = 0
live_buffer = [600, 1201]
# for count in range(0, iterations):
while True:
    norm_buffer = normalize_buffer(live_buffer)
    start_time = dt.now()
    count += 1
    
    println("[{}]:{}".format(count, "Fetching grid"))
    x,y,c_map=fetch_draw(grid)
    println("[{}]:{}".format(count, "Rendering grid"))
    
    plt.clf()
    plt.scatter(x,y, marker=marker, c=c_map, alpha=1, linewidth=0, s=3)
    plt.plot(range(graph_x_offset, graph_x_offset+len(norm_buffer)), norm_buffer, c="#ee2424", alpha=.3, lw=1)
    plt.xlim([0,grid_x])
    plt.ylim([0,grid_y])
    plt.savefig("img{0:0=5d}.png".format(count), dpi=150, facecolor="#101010", transparent=True)
    os.popen("feh --bg-center img{0:0=5d}.png".format(count))
    println("[{}]:{}".format(count, "Updating grid"))
    grid, live_buffer = grid_update(grid, live_buffer)
    end_time = dt.now()
    ts_diff = end_time-start_time
    # sleep(10)
    println("[ {} | {} ]:{} milli sec".format(count, live_buffer[-1], int(ts_diff.total_seconds()*1000)))
    print


