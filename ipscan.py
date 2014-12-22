#!/python27

import Queue
import threading
import subprocess as sp
from socket import gethostbyaddr as rdns
import sys
import os
from operator import itemgetter

class bcolors:
    grey = '\033[0;30m'
    greybold = '\033[1;30m'
    red = '\033[0;31m'
    redbold = '\033[1;30m'
    green = '\033[0;32m'
    greenbold = '\033[1;32m'
    ENDC = '\033[0m'

    def disable(self):
        self.END = ''
        self.grey = ''
        self.greybold = ''
        self.red = ''
        self.redbold = ''
        self.green = ''
        self.greenbold = ''


args = sys.argv
alive = {}
data = {}

def pinger(ip):
	global data
	global alive
	t = str(data['timeout'])
	n = str(data['count'])
	a = int(data['ipA'])
	b = int(data['ipB'])
	c = int(data['ipC'])
	d = int(data['ipD'])
	cmd = 'ping ' + ip + ' -w ' + t + ' -n ' + n + ' > nul'
	res = os.system(cmd)
	if int(res) < 1:
		up = '[X]   '
		try:
			dns = rdns(ip)[0]
		except:
			dns = ' '
		alive.update({ip:(ip,dns,up,a,b,c,d)})
		return
	else:
		if data['all'] == True:
			up = '[ ]   '
			dns = ' '
			alive.update({ip:(ip,dns,up,a,b,c,d)})
		return

def parse_data(args):
	try:
		if len(sys.argv) > 1:
			for i in args:
				if "help" in i or "-h" in i or "man" in i:
					print ""
					print "IPScan is an IP address scanner."
					print ""
					print "Possible arguemnts are:"
					print "-h / help   Shows this help dialog."
					print "-a / all    Shows all hosts in results regardless of response."
					print "timeout=[x] Specifies the ICMP timeout in ms, where x is the value."
					print "count=[x]   Specifies the number of ICMP packets to send, where x is the number."
					print ""
					print "Example:"
					print "#> ipscan 192.168.1.1/24 timeout=200 count=2"
					print ""
					print "(Scans the 192.168.1.0/24 subnet block with 2 packets for each IP with a time out 200ms."
					print  ""
					print "NOTE: IPScan only supports /32 /24 /26 /8 subnets at this time."
					quit()

				if "timeout" in i:
					t = i.split('=')
					data.update({'timeout': t[1] })
				else:
					data.update({'timeout': '300'})
				if "count" in i:
					c = i.split('=')
					data.update({'count': c[1] })
				else:
					data.update({'count': '1'})
				if "all" in i or "-a" in i:
					data.update({'all': True})
				else:
					data.update({'all': False})
			block = args[1].split('/')
			ip = block[0].split('.')
			data.update({'ip': block[0],'netmask': int(block[1]),'ipA': ip[0],'ipB': ip[1],'ipC': ip[2],'ipD': ip[3]})
			return 1
		else:
			print "IPScan takes at least one (1) argument. Type 'ipscan -h' for help."
			quit()
	except:
		return 0

def worker():
	ip = q.get()
	pinger(ip)
	q.task_done()
	return 1

def create_queue():
	#print "queue"
	try:
	
		
		return 1
	except:
		return 0

def iterator():
	#print "iterator"
	if data['netmask'] == 32:
		ip = data['ip']
		q.put(ip)
		return 1
	if data['netmask'] == 24:
		ipD = 1
		while ipD < 256:
			ip = data['ipA'] + '.' + data['ipB'] + '.' + data['ipC'] + '.' + str(ipD)
			q.put(ip)
			ipD = ipD + 1 #increment
		return 1
	elif data['netmask'] == 16:
		ipC = 0
		ipD = 0
		while ipC < 255:
			while ipD < 256:
				ip = data['ipA'] + '.' + data['ipB'] + '.' + str(iPC) + '.' + str(ipD)
				q.put(ip)
				ipD = ipD + 1
			ipC = ipC + 1
		return 1
	elif data['netmask'] == 8:
		ipB = 0
		ipC = 0
		ipD = 0
		while ipB < 255:
			while ipC < 255:
				while ipD < 256:
					ip = data['ipA'] + '.' + str(ipB) + '.' + str(iPC) + '.' + str(ipD)
					q.put(ip)
					ipD = ipD + 1
				ipC = ipC + 1
			ipB = ipC + 1
		return 1
	else:
		return 0

def show_data(alive):
	line = 0
	print ""
	print 'UP     IP ADDRESS          DNS'
	print '---    ---------------     ----------------------------------------'
	for i in sorted(alive, key=itemgetter(7,8,9,10)):
		spaces = ''
		count = 0
		sp = 18 - (len(i))
		while count < sp:
			spaces = spaces + ' '
			count = count + 1
		print '%s %s %s %s' % (alive[i][2], alive[i][0], spaces, alive[i][1])
		line = line + 1
		if line > 25:
			raw_input('PAUSED -- Press <ENTER> to continue...')
			line = 0
	print ""
	print ""
	return 1


def main():
	a = parse_data(args)
	if a == 0:
		print "\nThere was an error parsing the arguments. Exiting."
		exit()
	e = iterator()
	if e == 0:
		print "\nThere was a problem with the iterator."
	print ""
	print "Scanning...",

if __name__ == '__main__':
	q = Queue.Queue()
	main()
	for i in range(300):
		t = threading.Thread(target=worker)
		t.daemon = True
		t.start()
	q.join()
	show_data(alive)
	exit()