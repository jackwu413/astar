class Heap:
	"""	a heap really just needs an insert, a sift up and a sift down """

	#head is a HeapNode
	def __init__(self,head):
		self.minHeap = [0]
		self.currentsize = 0 
		
	#when adding to a heap all we really need to do is
	def push(self, item):
		#find the next smallest 
		self.minHeap.append(item)
		self.currentsize+=1
		siftup(self.minHeap)

	def siftup(minHeap, item):
		#swap parent and child
		index=minHeap.currentsize
		parent = minHeap(index/2)
		child = minHeap(index)
		while index!=0:
			if(parent.f==child.f):
				#check the gvalues
				if child.g<parent.g:
					#swap and update index
					minHeap[index/2]=child
					minHeap[index]=parent
					index=index/2
				else:
					break
			elif(child.f<parent.f):
				#swap and update index
				minHeap[index/2]=child
				minHeap[index]=parent
				index=index/2
			else:
				break
		#End while
		return

	def pop(self):
		#swap the last item (which will definitely be the largest/larger)
		root = self.minHeap[1]
		lastItem=self.minHeap[self.currentsize]

		self.minHeap[1]= lastItem
		self.minHeap.pop(self.currentsize)
		self.currentsize-=1

		#sift down

	#to sift down i just check the f values and see parent vs child, i have to if i can sift left or right 
	#try sifting left first and if left is less/ euqal try sifting right, if right is less/equal, then 
	#
	def siftDown(minHeap):
		siftptr=minHeap[1]
		index=1
		while(index*2<=minHeap.currentsize):
			if(minHeap[index].f<minHeap[minChild(index)].f):
				#swap and update index and siftptr--
				minHeap[index]=minHeap[minChild(index)]
				minHeap[minChild(index)]=siftptr

				siftptr=minHeap[minChild(index)]
				index=minChild(index)
			elif(siftptr.f==minHeap[minChild(index)].f):
				#check g
				if(siftptr.g<minHeap[minChild(index)].g):
					#swap and update index and siftptr
					minHeap[index]=minHeap[minChild(index)]
					minHeap[minChild(index)]=siftptr

					siftptr=minHeap[minChild(index)]
					index=minChild(index)
				else:
					return
			else:
				return

def minChild(self,i):
    if i * 2 + 1 > self.currentSize:
        return i * 2
    else:
        if self.heapList[i*2].f < self.heapList[i*2+1].f:
            return i * 2
        elif self.heapList[i*2].f == self.heapList[i*2+1].f:
        	if self.heapList[i*2].g < self.heapList[i*2+1].g:
        		return i*2
        	else:
        		return i*2+1
        else:
            return i * 2 + 1