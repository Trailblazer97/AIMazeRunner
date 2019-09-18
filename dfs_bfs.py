from tkinter import *
import math
import random
import numpy as np
import time
from random import shuffle, randrange
#import seeker
from collections import deque
        
class theMaze:
    def __init__( self, rows, columns):
        self.root = Tk()
        self.box = dict()
        self.width = math.ceil(1000/20) #root.winfo_screenwidth()
        self.height = math.ceil(1000/20) # root.winfo_screenheight()
        self.roots = Canvas(self.root, height = 6*self.height, width = 6* self.width, bg="#666666", highlightthickness=0, bd = 0)
        self.rows = rows
        self.columns = columns
        self.frame = {}
        self.mapstate = np.ones((self.rows, self.columns))
        # self.make_simple_maze(math.floor(rows*columns/10)*2)
        # self.make_complicated_maze()
        self.make_rand_maze(0.2)
        self.update_the_whole_maze()
        self.updateImg()
        self.roots.pack(fill = "both", expand = True)
        self.root.title("AI Maze")   
        self.dfs = Button(self.root,text='DFS',command=self.depthFirstSearch)   
        self.dfs.pack(side='bottom')
        self.bfs = Button(self.root,text='BFS',command=self.breadthFirstSearch)
        self.bfs.pack(side='bottom')
        self.reset = Button(self.root,text='Reset',command=self.resetButton)
        self.reset.pack(side='bottom')
        self.fringe = None
        self.goal = self.mapstate[self.rows-1, self.columns-1]


    def updateImg(self):  
        # self.make_simple_maze(3)
        self.root.after(1000, self.updateImg)

    def make_rand_maze(self, prob):
        rand = np.random.rand(self.rows, self.columns)
        self.mapstate = np.where(rand<prob, 0, 1)
        self.mapstate[0,0] = 1
        self.mapstate[self.rows-1, self.columns-1] = 1
        self.mapstateCopy = np.copy(self.mapstate)
        self.update_the_whole_maze()


    def update_the_maze(self, index):
        c = index%self.rows
        r = math.floor(index/self.rows)
        if self.mapstate[r,c] == 0:
            self.drawBox("black", r, c)
        elif self.mapstate[r,c] == 1:
            self.drawBox("white", r, c)
        elif self.mapstate[r,c] == 2:
            self.drawBox("green", r, c)
        else:
            self.drawBox("gray", r, c)

    def update_the_maze_simple(self, row,col):
        if self.mapstate[row,col] == 0:
            self.drawBox("black", row, col)
        elif self.mapstate[row,col] == 1:
            self.drawBox("white", row, col)
        elif self.mapstate[row,col] == 2:
            self.drawBox("green", row, col)
        else:
            self.drawBox("gray", row, col)

    def update_the_whole_maze(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.mapstate[i,j] == 0:
                    self.drawBox("black", i, j)
                elif self.mapstate[i,j] == 1:
                    self.drawBox("white", i, j)
                elif self.mapstate[i,j] == 2:
                    self.drawBox("green", i, j)
                else:
                    self.drawBox("gray", i, j)
        self.mapstateCopy = np.copy(self.mapstate)
        self.roots.pack(fill = "both", expand = True)


    def set_state_of_box(self, *args):
        if len(args) == 2:
            self.set_state_of_theId(args[0], args[1])
        if len(args) == 3:
            self.set_state_of_theRC(args[0], args[1], args[2])
    def set_state_of_theId(self, state, index):
        c = index%self.rows
        r = math.floor(index/self.rows)
        self.set_state_of_theRC(state, r, c)       
    def set_state_of_theRC(self, state, r, c):  
        # the r and c both starts from zero
        self.mapstate[r,c] = state

    def drawBox(self, *args):
        if len(args) == 2:
            self.drawBoxById(args[0], args[1])
        if len(args) == 3:
            self.drawBoxByRC(args[0], args[1], args[2])
    def drawBoxById(self, color, index):
        c = index%self.rows
        r = math.floor(index/self.rows)
        self.drawBoxByRC(color, r, c)
    def drawBoxByRC(self, color, r,c):
        # the r and c both starts from zero
        index = self.rows*(r)+c
        self.frame[index] = Frame(self.roots,width=self.width,height=self.height,bg="white")
        self.frame[index].pack_propagate(0)
        self.box[index] = Label(self.frame[index], text=index, borderwidth=10, background=color, width = self.width, height = self.height , fg = "grey", font=("Courier", 19))
        self.box[index].pack(fill="both", expand=True,side='left')
        self.frame[index].place(x=(c)*self.width,y=(r)*self.height)
        self.roots.pack(fill = "both", expand = True)
    
    def wasAlreadyVisited(self,xIndex,yIndex):
        if(self.mapstate[xIndex,yIndex]!=3):
            return True;
        else:
            return False

    def pushNeighboursIfNotVisited(self,xIndex,yIndex,fringe):
        
        
        if(yIndex>0):
            if(self.wasAlreadyVisited(xIndex,yIndex-1) and self.mapstate[xIndex,yIndex-1]!=0):
                fringe.append([xIndex,yIndex-1])
        
        if(xIndex>0):
            if(self.wasAlreadyVisited(xIndex-1,yIndex) and self.mapstate[xIndex-1,yIndex]!=0):
                fringe.append([xIndex-1,yIndex])
        
        if(xIndex<self.rows-1):
            if(self.wasAlreadyVisited(xIndex+1,yIndex) and self.mapstate[xIndex+1,yIndex]!=0):
                fringe.append([xIndex+1,yIndex])
        
        if(yIndex<self.rows-1):
            if(self.wasAlreadyVisited(xIndex,yIndex+1) and self.mapstate[xIndex,yIndex+1]!=0):
                fringe.append([xIndex,yIndex+1])
        
        
        return fringe

    def depthFirstSearch(self):
        self.mapstate = np.ones((self.rows, self.columns))
        self.fringe = []
        self.fringe.append([0,0])
        ## started by pushing the first node in the fringe
        while(len(self.fringe)>0):
            element = self.fringe.pop()
            if(element[0]==self.rows-1 and element[1] == self.columns-1):
                break;
            self.fringe = self.pushNeighboursIfNotVisited(element[0],element[1],self.fringe)
            # print(self.fringe)
            self.mapstate[element[0],element[1]] = 3;
            self.update_the_maze_simple(element[0],element[1])
    
    def breadthFirstSearch(self):   
        self.q = deque()
        self.q.append((0, 0))
        self.visited = []
        self.max_rows, self.max_cols = self.rows, self.columns
        while(len(self.q) > 0):
            self.x, self.y = self.q.popleft()        
            self.visited.append((self.x, self.y))
            # if(self.x, self.y is self.rows-1, self.columns-1):
            #     break
            self.mapstate[self.x, self.y] = 3
            self.update_the_maze_simple(self.x, self.y)
            for coord in [(self.x + 1, self.y), (self.x, self.y + 1), (self.x - 1, self.y), (self.x, self.y - 1)]:
                if coord not in self.q and coord not in self.visited:
                    a, b = coord
                    if a >= 0 and b >= 0 and a < self.rows and b < self.columns:
                        if self.mapstate[a, b]!=0:
                            self.q.append(coord)
        if (self.rows-1, self.columns-1) in self.visited:         
            traced = []
            self.x1, self.y1 = self.rows-1, self.columns-1
            self.mapstate[self.x1, self.y1] = 2
            self.update_the_maze_simple(self.x1, self.y1)
            traced.append((self.x1, self.y1))
            while((0, 0) not in traced):
                neighbours = [(self.x1 + 1, self.y1), (self.x1, self.y1 + 1), (self.x1 - 1, self.y1), (self.x1, self.y1 - 1)]
                ind = []
                act_neighbours = []
                for next in neighbours:
                    if next in self.visited:
                        act_neighbours.append(next)
                        ind.append(self.visited.index(next))
                self.x1, self.y1 = act_neighbours[ind.index(min(ind))]
                self.mapstate[self.x1, self.y1] = 2
                self.update_the_maze_simple(self.x1, self.y1)
                traced.append((self.x1, self.y1))
            print(traced)
                

        print(self.visited)
            
    def resetButton(self):
        self.mapstate = self.mapstateCopy
        self.update_the_whole_maze()


def main():
    maze = theMaze(10, 10)
    maze.root.mainloop()
    # print("Starting Depth First Search")

if __name__ == '__main__':
    main()
