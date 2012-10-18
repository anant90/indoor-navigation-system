                                                                     
                                                                     
                                                                     
                                             

from __future__ import generators
import appuifw
import audio
import e32
import string
from key_codes import *


appuifw.app.screen = 'normal'

class priorityDictionary(dict):
    def __init__(self):
        '''Initialize priorityDictionary by creating binary heap
of pairs (value,key).  Note that changing or removing a dict entry will
not remove the old pair from the heap until it is found by smallest() or
until the heap is rebuilt.'''
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from heap.'''
        if len(self) == 0:
            raise IndexError, "smallest of empty priorityDictionary"
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and \
                        heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]
	
    def __iter__(self):
        '''Create destructive sorted iterator of priorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()
	
    def __setitem__(self,key,val):
        '''Change value stored in dictionary and add corresponding
pair to heap.  Rebuilds the heap if the number of deleted items grows
too large, to avoid memory leakage.'''
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and \
                    newPair < heap[(insertionPoint-1)//2]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair
	
    def setdefault(self,key,val):
        '''Reimplement setdefault to call our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]

    def update(self, other):
        for key in other.keys():
            self[key] = other[key]






def Dijkstra(G,start,end=None):
	D = {}	# dictionary of final distances
	P = {}	# dictionary of predecessors
	Q = priorityDictionary()   # est.dist. of non-final vert.
	Q[start] = 0
	
	for v in Q:
		D[v] = Q[v]
		if v == end: break
		
		for w in G[v]:
			vwLength = D[v] + G[v][w]
			if w in D:
				if vwLength < D[w]:
					raise ValueError, \
  "Dijkstra: found better path to already-final vertex"
			elif w not in Q or vwLength < Q[w]:
				Q[w] = vwLength
				P[w] = v
	
	return (D,P)
			
def shortestPath(G,start,end):
	"""
	Find a single shortest path from the given start vertex
	to the given end vertex.
	The input has the same conventions as Dijkstra().
	The output is a list of the vertices in order along
	the shortest path.
	"""

	D,P = Dijkstra(G,start,end)
	Path = []
	while 1:
		Path.append(end)
		if end == start: break
                end = P[end]
	Path.reverse()
        for i in range(len(Path)):
            Path[i] = Path[i].name
	return Path

class Keyboard(object):
    def __init__(self,onevent=lambda:None):
        self._keyboard_state={}
        self._downs={}
        self._onevent=onevent
    def handle_event(self,event):
        if event['type'] == appuifw.EEventKeyDown:
            code=event['scancode']
            if not self.is_down(code):
                self._downs[code]=self._downs.get(code,0)+1
            self._keyboard_state[code]=1
        elif event['type'] == appuifw.EEventKeyUp:
            self._keyboard_state[event['scancode']]=0
        self._onevent()
    def is_down(self,scancode):
        return self._keyboard_state.get(scancode,0)
    def pressed(self,scancode):
        if self._downs.get(scancode,0):
            self._downs[scancode]-=1
            return True
        return False


class Node(object) :
	def __init__(self,nodeID,lat,lon,iPU,pUT,name, po,n,distn,ne,distne,e,diste,se,distse,s,dists,sw,distsw,w,distw,nw,distnw):
		self.nodeID = nodeID
		self.lat = lat
		self.lon = lon
		self.iPU = iPU
		self.pUT = pUT
		self.name = name
		self.po = po
		self.n = n
		self.distn = distn
		self.ne = ne
		self.distne = distne
		self.e = e
		self.diste = diste
		self.se = se
		self.distse = distse
		self.s = s
		self.dists = dists
		self.sw = sw
		self.distsw = distsw
		self.w = w
		self.distw = distw
		self.nw = nw
		self.distnw = distnw

str = "67;77.19008252413587,28.5449468667779;0,77.19008252413587,28.54490963735048,False,"",Reception,1,1,11.0113882279002,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1;1,77.19018684520618,28.5449468667779,False,"",Node0,1,2,31.585356154176708,-1,-1,4,8.145137362192386,-1,-1,0,11.0113882279002,-1,-1,3,8.908536390787575,-1,-1;2,77.19048783601427,28.54504974259647,False,"",Room,1,-1,-1,-1,-1,-1,-1,-1,-1,1,31.585356154176708,-1,-1,-1,-1,-1,-1;3,77.19015124689048,28.54502084717424,False,"",Lifts,1,-1,-1,-1,-1,1,8.908536390787575,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1;4,77.19021580736393,28.5448779665363,False,"",Room 2,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,8.145137362192386,-1,-1"

segmentednodes = str.split( ';')

bnorth = int(segmentednodes[0])

glob = segmentednodes[1].split( ',')
globx = float(glob[0])
globy = float(glob[1])

nodelist = segmentednodes[2: len(segmentednodes)]
l = []

for item in nodelist:
	i = item.split( ',')
	if i[3] == "false" :
		node = Node(int(i[0]),float(i[1]),float(i[2]),False,i[4],i[5],int(i[6]),int(i[7]),float(i[8]),int(i[9]),float(i[10]),int(i[11]),float(i[12]),int(i[13]),float(i[14]),int(i[15]),float(i[16]),int(i[17]),float(i[18]),int(i[19]),float(i[20]),int(i[21]),float(i[22]))
	else :	
		node = Node(int(i[0]),float(i[1]),float(i[2]),True,i[4],i[5],int(i[6]),int(i[7]),float(i[8]),int(i[9]),float(i[10]),int(i[11]),float(i[12]),int(i[13]),float(i[14]),int(i[15]),float(i[16]),int(i[17]),float(i[18]),int(i[19]),float(i[20]),int(i[21]),float(i[22]))
	l.append(node)

def getnodebynum(num):
	for w in l:
		if w.nodeID == num :
			return w

Gr = {}

for nodes in l:
	Gr[nodes] = {}
	if nodes.n != -1 :
		k = getnodebynum(nodes.n)
		Gr[nodes][k] = nodes.distn
	if nodes.ne != -1 :
		k = getnodebynum(nodes.ne)
		Gr[nodes][k] = nodes.distne
	if nodes.e != -1 :
		k = getnodebynum(nodes.e)
		Gr[nodes][k] = nodes.diste
	if nodes.se != -1 :
		k = getnodebynum(nodes.se)
		Gr[nodes][k] = nodes.distse
	if nodes.s != -1 :
		k = getnodebynum(nodes.s)
		Gr[nodes][k] = nodes.dists
	if nodes.sw != -1 :
		k = getnodebynum(nodes.sw)
		Gr[nodes][k] = nodes.distsw
	if nodes.w != -1 :
		k = getnodebynum(nodes.w)
		Gr[nodes][k] = nodes.distw
	if nodes.nw != -1 :
		k = getnodebynum(nodes.nw)
		Gr[nodes][k] = nodes.distnw

def getnode(s):
	for w in Gr:
		if w.name == s :
			return w


keyboard=Keyboard()


#audio.say("Welcome to Indoor Navigation System for the Visually Impaired") 

#audio.say( "The places you can go to in the bulding are:")
#for w in Gr:
#	audio.say(w.name)


running=1
steplength = 0.7

def quit():
    global running
    running=0
    appuifw.app.set_exit()

    
appuifw.app.exit_key_handler=quit

appuifw.app.title = u"Indoor Navigation App"
canvas=appuifw.Canvas(event_callback=keyboard.handle_event, redraw_callback=None)
appuifw.app.body=canvas


while running :
	if keyboard.pressed(EScancodeStar):
		data = appuifw.query(u"Type a word:", "text")
		audio.say(data)
		pathlist = shortestPath(Gr,l[0], getnode(data))
		for w in pathlist:
			audio.say (w)
	e32.ao_yield()
