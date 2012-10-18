from __future__ import generators
import appuifw
import audio
import e32
import string
from key_codes import *
import socket


appuifw.app.screen = 'normal'

#kmp code
def KnuthMorrisPratt(text, pattern):
    found  = 0
    # allow indexing into pattern and protect against change during yield
    pattern = list(pattern)

    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen == len(pattern) or \
              matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            found = 1
    return found

# function that handles the bluetooth connection:
def bt_connect():
    print "Hello"
    global sock
    # create a bluetooth socket
    sock=socket.socket(socket.AF_BT,socket.SOCK_STREAM)
    target=''# here you can give the bt address of the other mobile if you know it
    if not target:
        # scan for bluetooth devices
        address,services=socket.bt_discover()
        print "Discovered: %s, %s"%(address,services)
        if len(services)>1:
            choices=services.keys()
            choices.sort()
            # bring up a popup menu and show the available bt devices for selection
            choice=appuifw.popup_menu([unicode(services[x])+": "+x
                                        for x in choices],u'Choose port:')
            target=(address,services[choices[choice]])
        else:
            target=(address,services.values()[0])
    # print "Connecting to "+str(target)
    # connect to the serial port of the PC
    sock.connect(target)
    print "OK."

    # call the text input field function   
    # bt_typetext()

    
def bt_sendID(a):
    global sock
    sock.send(a)

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

#str = "67;77.19008252413587,28.5449468667779;0,77.19008252413587,28.54490963735048,False,"",Reception,1,1,11.0113882279002,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1;1,77.19018684520618,28.5449468667779,False,"",Node0,1,2,31.585356154176708,-1,-1,4,8.145137362192386,-1,-1,0,11.0113882279002,-1,-1,3,8.908536390787575,-1,-1;2,77.19048783601427,28.54504974259647,False,"",Room,1,-1,-1,-1,-1,-1,-1,-1,-1,1,31.585356154176708,-1,-1,-1,-1,-1,-1;3,77.19015124689048,28.54502084717424,False,"",Lifts,1,-1,-1,-1,-1,1,8.908536390787575,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1;4,77.19021580736393,28.5448779665363,False,"",Room 2,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1,8.145137362192386,-1,-1"

str = "69;77.19014821926426,28.54492815056406;0,77.19014821926426,28.54492815056406,False,"",SeminarRoom,1,1,11.611399446412973,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1;1,77.19025945749688,28.54496459981439,False,"",DHD Lab,1,2,2.242062412174274,-1,-1,-1,-1,-1,-1,0,11.611399446412973,-1,-1,-1,-1,-1,-1;2,77.19028121425875,28.54497093823186,False,"",PathNode0,1,5,4.412350771840456,-1,-1,-1,-1,-1,-1,1,2.242062412174274,-1,-1,3,3.001403865644699,-1,-1;3,77.19027068629167,28.54499637423362,False,"",Lift0,1,-1,-1,-1,-1,2,3.001403865644699,-1,-1,-1,-1,-1,-1,4,6.3702187762009785,-1,-1;4,77.19024759993795,28.54505011606412,False,"",Toilet0,1,-1,-1,-1,-1,3,6.3702187762009785,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1;5,77.19032332695862,28.54498515934826,False,"",Stairs,1,6,2.4859895564978287,-1,-1,-1,-1,-1,-1,2,4.412350771840456,-1,-1,-1,-1,-1,-1;6,77.19034682856388,28.54499367390863,False,"",FPGA Lab,1,7,2.5372670896378264,-1,-1,-1,-1,-1,-1,5,2.4859895564978287,-1,-1,-1,-1,-1,-1;7,77.19037094494148,28.54500207884988,False,"",Prof Balakrishnan,1,8,3.624091064096253,-1,-1,-1,-1,-1,-1,6,2.5372670896378264,-1,-1,-1,-1,-1,-1;8,77.19040571885814,28.54501332393493,False,"",Prof Anshul Kumar,1,9,3.6662130506711033,-1,-1,-1,-1,-1,-1,7,3.624091064096253,-1,-1,-1,-1,-1,-1;9,77.19044059441215,28.54502540421495,False,"",Discussion Area,1,10,4.215699491644891,-1,-1,-1,-1,-1,-1,8,3.6662130506711033,-1,-1,-1,-1,-1,-1;10,77.19048136388592,28.54503768868221,False,"",Prof Ragesh Jaiwal,1,11,3.7815290891881217,-1,-1,-1,-1,-1,-1,9,4.215699491644891,-1,-1,-1,-1,-1,-1;11,77.19051765605259,28.54504940393853,False,"",Prof SN Maheshwari,1,12,4.313062191600041,-1,-1,-1,-1,-1,-1,10,3.7815290891881217,-1,-1,-1,-1,-1,-1;12,77.19055836570675,28.54506431411116,False,"",Philips VLSI Lab,1,13,5.355399019099763,-1,-1,-1,-1,-1,-1,11,4.313062191600041,-1,-1,-1,-1,-1,-1;13,77.19060920728944,28.5450821897095,False,"",GCL,1,-1,-1,-1,-1,-1,-1,-1,-1,12,5.355399019099763,-1,-1,14,4.689541474931781,-1,-1;14,77.19059134376384,28.54512145330926,False,"",PathNode1,1,-1,-1,-1,-1,13,4.689541474931781,-1,-1,15,3.0909451900836817,-1,-1,16,1.501842528354849,-1,-1;15,77.19056166649858,28.54511190843219,False,"",Toliet1,1,14,3.0909451900836817,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1;16,77.19058578896964,28.54513408553932,False,"",Server Room,1,-1,-1,-1,-1,14,1.501842528354849,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"

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

bt_connect()

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
 
orientation = 0
startnode = l[0]

def getnode(s):
	for w in Gr:
		if w.name == s :
			return w

def instr(ori, diff, dist):
	global orientation 
	orientation =  diff
	diff1 = (orientation - ori) % 360
	if (diff1<180 and diff1 >0) :
		return ("Turn right by %d and move straight for %d meters"%(diff1, dist))
	elif ( diff1 == 0 ) :
		return ("Move straight for %d meters"%(dist,))
	else:
		return ("Turn left by %d nd move straight for %d meters"%(360-diff1, dist))

def search():
	
	data = appuifw.query(u"Type destination:", "text")
	dumlist = []
	for w in l:
		found = KnuthMorrisPratt(w.name, data)
		if(found == 1 ) :
			dumlist.append(w.name)
	if ( len(dumlist) == 1 ):
		return dumlist[0]
	elif ( len(dumlist) == 0 ) :
		audio.say("No destination containing the name "+data)
		audio.say("type destination")
		return (search())
	else :
		audio.say("destinations containing the name " + data)
		for t in dumlist :
			audio.say(t)
		audio.say("type the one you want")
		return ( search() ) 	
	

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
		audio.say("type destination")
		data1 = search()
		audio.say(data1)
		pathlist = shortestPath(Gr,startnode, getnode(data1))

		audio.say("You are currently at "+ startnode.name)
		audio.say("and having orientation %d" % (orientation,) )
		startnode = getnode(data1)		
		for i in range(len(pathlist)-1):
			if (pathlist[i].n == pathlist[i+1].nodeID):
				audio.say(instr(orientation,0,pathlist[i].distn))
				flag = True
				while flag:
					audio.say("Press 1 to confirm, 2 to repeat and 3 for buzzer")
					if keyboard.pressed(EScancode2):
						audio.say(instr(orientation,0, pathlist[i].distn))
					if keyboard.pressed(EScancode1):
						flag = False
					if keyboard.pressed(EScancode3):
						bt_sendID("%d"%(pathlist[i+1].nodeID,))
			flag = True
			if (pathlist[i].ne == pathlist[i+1].nodeID):
				audio.say(instr(orientation,45,pathlist[i].distne))
				while flag:
					audio.say("Press 1 to confirm, 2 to repeat and 3 for buzzer")
					if keyboard.pressed(EScancode2):
						audio.say(instr(orientation,45, pathlist[i].distne))
					if keyboard.pressed(EScancode1):
						flag = False
					if keyboard.pressed(EScancode3):
						bt_sendID("%d"%(pathlist[i+1].nodeID,))
			flag = True	
			if (pathlist[i].e == pathlist[i+1].nodeID):
				audio.say(instr(orientation,90,pathlist[i].diste))
				while flag:
					audio.say("Press 1 to confirm, 2 to repeat and 3 for buzzer")
					if keyboard.pressed(EScancode2):
						audio.say(instr(orientation,90, pathlist[i].diste))
					if keyboard.pressed(EScancode1):
						flag = False
					if keyboard.pressed(EScancode3):
						bt_sendID("%d"%(pathlist[i+1].nodeID,))
			flag  = True

			if (pathlist[i].se == pathlist[i+1].nodeID):
				audio.say(instr(orientation,135,pathlist[i].distse))
				while flag:
					audio.say("Press 1 to confirm, 2 to repeat and 3 for buzzer")
					if keyboard.pressed(EScancode2):
						audio.say(instr(orientation,135, pathlist[i].distse))
					if keyboard.pressed(EScancode1):
						flag = False
					if keyboard.pressed(EScancode3):
						bt_sendID("%d"%(pathlist[i+1].nodeID,))
			flag  = True
			if (pathlist[i].s == pathlist[i+1].nodeID):
				audio.say(instr(orientation,180,pathlist[i].dists))
				while flag:
					audio.say("Press 1 to confirm, 2 to repeat and 3 for buzzer")
					if keyboard.pressed(EScancode2):
						audio.say(instr(orientation,180, pathlist[i].dists))
					if keyboard.pressed(EScancode1):
						flag = False
					if keyboard.pressed(EScancode3):
						bt_sendID("%d"%(pathlist[i+1].nodeID,))
			flag  = True
			if (pathlist[i].sw == pathlist[i+1].nodeID):
				audio.say(instr(orientation,225,pathlist[i].distsw))
				while flag:
					audio.say("Press 1 to confirm, 2 to repeat and 3 for buzzer")
					if keyboard.pressed(EScancode2):
						audio.say(instr(orientation,225, pathlist[i].distsw))
					if keyboard.pressed(EScancode1):
						flag = False
					if keyboard.pressed(EScancode3):
						bt_sendID("%d"%(pathlist[i+1].nodeID,))
			flag  = True
			if (pathlist[i].w == pathlist[i+1].nodeID):
				audio.say(instr(orientation,270,pathlist[i].distw))
				while flag:
					audio.say("Press 1 to confirm, 2 to repeat and 3 for buzzer")
					if keyboard.pressed(EScancode2):
						audio.say(instr(orientation,270, pathlist[i].distw))
					if keyboard.pressed(EScancode1):
						flag = False
					if keyboard.pressed(EScancode3):
						bt_sendID("%d"%(pathlist[i+1].nodeID,))
			flag  = True			
			if (pathlist[i].nw == pathlist[i+1].nodeID):
				audio.say(instr(orientation,315,pathlist[i].distnw))
				while flag:
					audio.say("Press 1 to confirm, 2 to repeat and 3 for buzzer")
					if keyboard.pressed(EScancode2):
						audio.say(instr(orientation,315, pathlist[i].distnw))
					if keyboard.pressed(EScancode1):
						flag = False
					if keyboard.pressed(EScancode3):
						bt_sendID("%d"%(pathlist[i+1].nodeID,))
			flag  = True

	e32.ao_yield()