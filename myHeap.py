class Heap:
	def __init__(self):
		self.heap = [0]
		self.currentSize = 0

	def push(self, item):
		self.heap.append(item)
		self.currentSize += 1
		self.siftUp(self.currentSize)

	def siftUp(self, i):
		while i / 2 > 0:
			if self.heap[i].f < self.heap[i/2].f:
				holder = self.heap[i/2]
				self.heap[i/2] = self.heap[i]
				self.heap[i] = holder 
			elif self.heap[i].f == self.heap[i/2].f:
				if self.heap[i].g < self.heap[i/2].g:
					break
				else: 
					holder = self.heap[i/2]
					self.heap[i/2] = self.heap[i]
					self.heap[i] = holder 
			i = i / 2

	def heappop(self):
		lowest = self.heap[1]
		self.heap[1] = self.heap[self.currentSize]
		self.currentSize -= 1
		self.heap.pop()
		self.siftDown(1)
		return lowest

	def siftDown(self, i):	 
		while (i * 2) <= self.currentSize:
			minChild = self.minChild(i)
			if(self.heap[i].f > self.heap[minChild].f):
				holder = self.heap[i]
				self.heap[i] = self.heap[minChild]
				self.heap[minChild] = holder
			elif(self.heap[i].f == self.heap[minChild].f):
				if self.heap[i].g < self.heap[minChild].g:
					holder = self.heap[i]
					self.heap[i] = self.heap[minChild]
					self.heap[minChild] = holder
				else:
					break
			i = minChild

	def minChild(self, i):
		if ((i*2)+1) > self.currentSize:
			return i*2
		elif(self.heap[i*2].f < self.heap[(i*2)+1].f):
			return i*2
		else:
			return (i*2) + 1