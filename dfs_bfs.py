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
		self.width = math.ceil(500/rows) #root.winfo_screenwidth()
		self.height = math.ceil(500/columns) # root.winfo_screenheight()
		self.roots = Canvas(self.root, height = rows*self.height, width = columns* self.width, bg="#666666", highlightthickness=0, bd = 0)
		self.rows = rows
		self.columns = columns
		self.frame = {}
		self.mapstate = np.ones((self.rows, self.columns))
		self.initial_the_canvas()
		self.make_rand_maze(0.2)
		self.roots.pack(fill = "both", expand = True)
		self.root.title("AI Maze")   
		self.dfs = Button(self.root,text='DFS',command=self.depthFirstSearch)   
		self.dfs.pack(side='bottom')
		self.bfs = Button(self.root,text='BFS',command=self.breadthFirstSearch)
		self.bfs.pack(side='bottom')

		self.aStarEuc = Button(self.root,text='A*euc',command=self.a_star_euc)
		self.aStarEuc.pack(side='bottom')
		self.aStarMan = Button(self.root,text='A*man',command=self.a_star_man)
		self.aStarMan.pack(side='bottom')

		self.reset = Button(self.root,text='Reset',command=self.resetButton)
		self.reset.pack(side='bottom')
		self.fringe = None
		self.goal = self.mapstate[self.rows-1, self.columns-1]


	def updateImg(self):  
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
			self.drawBox("orange", r, c)

	def update_the_maze_simple(self, row,col):
		if self.mapstate[row,col] == 0:
			self.drawBox("black", row, col)
		elif self.mapstate[row,col] == 1:
			self.drawBox("white", row, col)
		elif self.mapstate[row,col] == 2:
			self.drawBox("green", row, col)
		else:
			self.drawBox("orange", row, col)

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
					self.drawBox("orange", i, j)
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
	def initial_the_canvas(self):
		for r in range(0,self.rows):
			for c in range(0,self.columns):
				index = self.rows*(r)+c
				self.frame[index] = Frame(self.roots,width=self.width,height=self.height,bg="white")
				self.frame[index].pack_propagate(0)
	def drawBoxByRC(self, color, r,c):
		# the r and c both starts from zero
		index = self.rows*(r)+c
		self.frame[index] = Frame(self.roots,width=self.width,height=self.height,bg=color)
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
		if(xIndex<self.rows-1):
			if(self.wasAlreadyVisited(xIndex+1,yIndex) and self.mapstate[xIndex+1,yIndex]!=0):
				fringe.append([xIndex+1,yIndex])
		
		if(yIndex<self.rows-1):
			if(self.wasAlreadyVisited(xIndex,yIndex+1) and self.mapstate[xIndex,yIndex+1]!=0):
				fringe.append([xIndex,yIndex+1])
		
		if(yIndex>0):
			if(self.wasAlreadyVisited(xIndex,yIndex-1) and self.mapstate[xIndex,yIndex-1]!=0):
				fringe.append([xIndex,yIndex-1])
		
		if(xIndex>0):
			if(self.wasAlreadyVisited(xIndex-1,yIndex) and self.mapstate[xIndex-1,yIndex]!=0):
				fringe.append([xIndex-1,yIndex])
		return fringe

	def depthFirstSearch(self):
		s = time.time()
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
		print("DFS %s", time.time()-s)
	def breadthFirstSearch(self):   
		s = time.time()
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
		print("BFS %s", time.time()-s)
	def a_star_euc(self):
		s = time.time()
		self.a_star("euc")
		print("euc %s", time.time()-s)
	def a_star_man(self):
		s = time.time()
		self.a_star("man")
		print("man %s", time.time()-s)
	def a_star(self, heuristic):
		fstate = np.ones((self.rows, self.columns))
		fstate = fstate*(math.pow(2,15)-1)       
		w = self.rows
		h = self.columns
		class node():
			def __init__(self, px, py, x, y):
				self.n = [x,y]
				self.p = [px,py]
		class aListWithState():
			def __init__(self):
				self.list = []
			def add(self, px, py, x, y, f):
				n = node(px, py, x, y)
				self.list.append(n)
				fstate[x,y] = f
			def popMin(self):
				fs = []
				for node in self.list:
					x, y = node.n
					fs.append(fstate[x,y])
				index = fs.index(min(fs))
				node = self.list.pop(index)
				return node.n, node.p

		def get_the_f(qx, qy, x, y):
			return get_the_g(qx, qy, x, y)+get_the_h(x,y)
		def get_the_g(qx, qy, x, y):  
			return distance(qx, qy, x, y)
		def get_the_h(x, y):
			return distance(x, y, w-1, h-1)
		def distance(qx, qy, x, y):
			if "man" in heuristic:
				return manhattan_distance(qx, qy, x, y)
			elif "euc" in heuristic:
				return euclidean_distance(qx, qy, x, y)
			else:
				return False
		def manhattan_distance(qx, qy, x, y):
			xD = math.fabs(qx-x)
			yD = math.fabs(qy-y)
			return xD+yD
		def euclidean_distance(qx, qy, x, y):
			xD2 = math.pow(qx-x,2)
			yD2 = math.pow(qy-y,2)
			return math.pow(xD2+yD2,1/2)
		def best_route(theList):
			nList = []
			pList = []
			bestRoute = []
			for node in theList:
			    nList.append(node.n)
			    pList.append(node.p)
			n = nList.pop()
			oldP = pList.pop()
			bestRoute.insert(0,n)
			while len(nList)>0:
			    while oldP!=n and len(nList)>0:
			        n = nList.pop()
			        p = pList.pop() 
			    bestRoute.insert(0,n)
			    oldP = p
			for node in bestRoute:
				x,y = node
				self.mapstate[x,y] = 2
				self.update_the_maze_simple(x,y)
				print(node)
			return bestRoute

		openList = aListWithState()
		closedList = aListWithState()
		openList.add(-1, -1, 0, 0, 0)
		self.fringe = []
		self.fringe.append([0,0])

		while(len(openList.list)>0):
			q, parents = openList.popMin()
			qx, qy = q
			pqx, pqy = parents
			d = [(qx - 1, qy), (qx, qy + 1), (qx + 1, qy), (qx, qy - 1)]
			shuffle(d)
			for (xx, yy) in d:
				if xx==w-1 and yy==h-1:
					closedList.add(pqx,pqy,qx,qy,fstate[qx,qy])
					self.fringe.append([qx,qy])
					self.mapstate[qx,qy] = 3
					self.update_the_maze_simple(qx,qy)
					closedList.add(qx,qy,xx,yy,fstate[qx,qy])
					self.fringe.append([xx,yy])
					self.mapstate[xx,yy] = 3
					self.update_the_maze_simple(xx,yy)
					print("A* algorithm completed!")
					return best_route(closedList.list)
				if xx<0 or xx>=w or yy<0 or yy>=h:
					continue
				if self.mapstate[xx,yy]==0:
					continue
				f = get_the_f( qx, qy, xx, yy)
				if fstate[xx,yy] <= f:
					continue
				else:
					fstate[xx,yy] = f
				if [xx,yy] in openList.list:
					continue
				openList.add(qx,qy,xx,yy,f)
			closedList.add(pqx,pqy,qx,qy,fstate[qx,qy])
			self.fringe.append([qx,qy])
			self.mapstate[qx,qy] = 3
			self.update_the_maze_simple(qx,qy)


		print("A* algorithm failed!")
		closedList.add(pqx,pqy,qx,qy,fstate[qx,qy])
		self.fringe.append([qx,qy])
		self.mapstate[qx,qy] = 3
		self.update_the_maze_simple(qx,qy)
		return False            
	
	def bi_directional_BFS(self):
		self.fringe = []
		self.fringe.append([0,0])

		reverseFringe = [[0,0]]
		endsDidMeet = False;
		## started by pushing the first node in the fringe
		while(len(self.fringe)>0 and len(reverseFringe)>0):
			element = self.fringe[0]
			self.fringe.remove(element)
			if(element[0]==self.rows-1 and element[1] == self.columns-1):
			    self.mapstate[element[0],element[1]] = 3;
			    self.update_the_maze_simple(element[0],element[1])
			    break;
			self.fringe = self.pushNeighboursIfNotVisited(element[0],element[1],self.fringe)
			# print(self.fringe)
			self.mapstate[element[0],element[1]] = 3;
			self.update_the_maze_simple(element[0],element[1])


	def resetButton(self):
		print(self.mapstate)
		for r in range(0, self.rows):
			for c in range(0, self.columns):
				if self.mapstate[r,c] != self.mapstateCopy[r,c]:
					self.mapstate[r,c] = self.mapstateCopy[r,c]
					self.update_the_maze_simple(r,c)			



def main():
	maze = theMaze(20, 20)
	maze.root.mainloop()
	# print("Starting Depth First Search")

if __name__ == '__main__':
	main()
