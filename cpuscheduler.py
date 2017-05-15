# Haider Tiwana
# Operating Systems
# Lab 4
# CPU Scheduler: implementing FCFS, RR, and STRF

from queue import Queue
from queue import PriorityQueue

class process(object):
 	def __init__(self, pid, arrival, burst):
 		self.pid = pid
 		self.arrival = arrival
 		self.burst = burst

def fcfs(plist):
	arrived = []
	response = {}
	readyQ = Queue()
	clock = 0
	idleTime = 0
	waitTime = 0
	responseTime = 0
	turnaroundTime = 0
	print("Simulation starting: ") 

	while True:

		for p in plist:
			if p.arrival == clock:
				print(clock, p.pid, "arriving")
				readyQ.put(p)
				arrived.append(p)
				continue

		if not readyQ.empty():
			peek = readyQ.queue
			curr = peek[0] # process next in queue

			if curr.burst != 0 and curr.burst != 1:
				print(clock, curr.pid, "running")
				if curr not in response:
					response[curr] = clock
				curr.burst -= 1
				clock += 1

			elif curr.burst == 1:
				print(clock, curr.pid, "running")
				curr.burst -= 1
				#print(clock, curr.pid, "finished")
				clock += 1
				readyQ.get()
				turnaroundTime += clock - curr.arrival

				# get the next process in queue and calculate wait time
				if not readyQ.empty():
					nextonQ = readyQ.queue
					nextp = nextonQ[0]
					waitTime += (clock - nextp.arrival)
					#responseTime += clock


		if readyQ.empty() and len(arrived) != len(plist):
			print("idling...........")
			idleTime += 1
			clock += 1

		if len(arrived) == len(plist) and readyQ.empty():
			# indicates last process is finished
			#responseTime += clock
			for item in response:
				responseTime += response[item] - item.arrival

			print("Average waiting time:", round(waitTime/len(plist),2))
			print("Average response time:", round(responseTime/len(plist),2))
			print("Average turnaround time:", turnaroundTime/len(plist))
			print("Average CPU usage:", str(((clock-idleTime)/clock)*100)+ "%")
			return

def rr(plist, quantum):

	wait = {}
	response = {}
	firstrun = {}
	completed = []
	readyQ = Queue()
	clock = 0
	idleTime = 0
	waitTime = 0 
	responseTime = 0
	turnaroundTime = 0
	qtime = 0
	enqueue = None

	while True:

		for p in plist:
			if p.arrival == clock:
				print(clock, p.pid, "arriving")
				readyQ.put(p)
				wait[p] = 0
				continue

		if enqueue != None:
			readyQ.put(enqueue)
			enqueue = None

		if not readyQ.empty():
			peek = readyQ.queue
			curr = peek[0] # process next in queue

		#for i in range(0,quantum):
		if qtime <= quantum:

			# this loops twice if the burst is not done
			if curr.burst != 1 and curr.burst != 0:
				print(clock, curr.pid, "running")
				for k in wait:
					if curr != k:
						wait[k] += 1
				if curr not in response:
					response[curr] = clock
				curr.burst -= 1
				clock += 1

			elif curr.burst == 1:
				print(clock, curr.pid, "running")

				curr.burst -= 1
				clock += 1
				print(clock, curr.pid, "finished")
				completed.append(curr)
				#readyQ.get()
				turnaroundTime += clock - curr.arrival

			# get the next process in queue and calculate wait time
			if not readyQ.empty():
				nextonQ = readyQ.queue
				nextp = nextonQ[0]

			qtime += 1

			if qtime == quantum:
				enqueue = readyQ.get()
				#readyQ.put(enqueue)
				qtime = 0

		if readyQ.empty() and len(arrived) != len(plist):
			print("idling...........")
			idleTime += 1
			clock += 1

		if len(completed) == len(plist):
			# indicates last process is finished
			for item in wait:
				waitTime += wait[item]

			for item in response:
				responseTime += response[item] - item.arrival

			print("Average waiting time:", round(waitTime/len(plist),2))
			print("Average response time:", round(responseTime/len(plist),2))
			print("Average turnaround time:", round(turnaroundTime/len(plist),2))
			print("Average CPU usage:", str(((clock-idleTime)/clock)*100)+ "%")
			return

# check during each arrival if burst is less than current, if so append to queue
# maintain queue of [process burst][burst]
def strf(plist):
	arrived = []
	response = {}
	readyQ = PriorityQueue()
	clock = 0
	idleTime = 0
	waitTime = 0
	responseTime = 0
	turnaroundTime = 0
	print("Simulation starting: ") 

	while True:

		for p in plist:
			if p.arrival == clock:
				print(clock, p.pid, "arriving")
				readyQ.put((p.burst, p))
				arrived.append(p)
				continue

		if not readyQ.empty():
			peek = readyQ.queue
			#peak [0][0] is burst
			#peak [0] [1] is process
			# print(peek[0][0])
			curr = peek[0][1] # process next in queue
			# print("curr is ", curr.pid, "with burst", curr.burst)


			if curr.burst != 0 and curr.burst != 1:
				print(clock, curr.pid, "running")

				if curr not in response:
					response[curr] = clock
				curr.burst -= 1
				clock += 1
				continue

			elif curr.burst == 1:
				print(clock, curr.pid, "running")
				curr.burst -= 1
				#print(clock, curr.pid, "finished")
				clock += 1
				readyQ.get()
				turnaroundTime += clock - curr.arrival

				# get the next process in queue and calculate wait time
				if not readyQ.empty():
					nextonQ = readyQ.queue
					nextp = nextonQ[0][1]
					waitTime += (clock - nextp.arrival)
					#responseTime += clock


		if readyQ.empty() and len(arrived) != len(plist):
			print("idling...........")
			idleTime += 1
			clock += 1

		if len(arrived) == len(plist) and readyQ.empty():
			# indicates last process is finished
			#responseTime += clock
			for item in response:
				responseTime += response[item] - item.arrival

			print("Average waiting time:", round(waitTime/len(plist),2))
			print("Average response time:", round(responseTime/len(plist),2))
			print("Average turnaround time:", turnaroundTime/len(plist))
			print("Average CPU usage:", str(((clock-idleTime)/clock)*100)+ "%")
			return


def main():
	processes = []

	which = int(input("Which file would you like to test algorithms on: (1) small or (2) big? "))

	if which == 1:
		file = open("small.txt", 'r')
	elif which == 2:
		file = open("big.txt", 'r')

	for line in file:
		pieces = line.strip().split(" ")
		if (pieces[0] == '0') and (pieces[1] == '0') and (pieces[2] == '0'):
			break

		p = process(int(pieces[0]), int(pieces[1]), int(pieces[2]))
		processes.append(p)

	play = int(input("Which algorithm would you like to run: (1) FCFS, (2) RR, (3) STRF? "))

	if play == 1:
		fcfs(processes)
	elif play == 2:
		quan = int(input("Enter quantum size: "))
		rr(processes, quan)
	elif play == 3:
		strf(processes)

main()