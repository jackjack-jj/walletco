#!/usr/bin/env python

# walletco.py 1.0
#
# walletco.py reads the keys (including hidden ones) of a wallet and import them into a new one
#
# Joric's Pywallet.py (https://github.com/joric/pywallet) must be installed to use walletco
# If your new wallet.dat has been created by a 0.3.25+ client, Joric's pywallet won't import keys, in that case use my fork: https://github.com/jackjack-jj/pywallet


import json
import sys, datetime, time
import os


def disp(a):
	sys.stdout.write ('[')
	for j in range(int(a*15)):
		sys.stdout.write ('=')
	sys.stdout.write ('>')
	for j in range(int(15-a*15-0.001)):
		sys.stdout.write (' ')
	sys.stdout.write (']   Importing:  %3.2f%%'%(100*a) + chr(13))
	sys.stdout.flush()


from optparse import OptionParser

def main():

	json_db = {}
	i = 0
	walletfilenamepw = ""
	walletpathpw = ""
	nwalletfilenamepw = ""
	nwalletpathpw = ""

	parser = OptionParser(usage="%prog [options]\nAll directories must be entered with the ending path separator", version="%prog 1.0")

	parser.add_option("-p", "--pwpath", dest="pwpath", 
		help="pywallet.py directory (default = ./)",
		default=".")

	parser.add_option("-w", "--wpath", dest="wpath",
		help="old wallet.dat directory (default = bitcoin default)")

	parser.add_option("-W", "--wfilename", dest="wfilename",
		help="old wallet.dat filename (default = wallet.dat)",
		default="wallet.dat")

	parser.add_option("-n", "--nwpath", dest="nwpath",
		help="new wallet.dat directory (default = bitcoin default)")

	parser.add_option("-N", "--nwfilename", dest="nwfilename",
		help="new wallet.dat filename (default = wallet.dat)",
		default="wallet.dat")

	(options, args) = parser.parse_args()

	if options.wpath is not None:
		walletpathpw = " --datadir " + options.wpath + " ";
	walletpathpw = " --wallet " + options.wfilename + " ";

	if options.nwpath is not None:
		nwalletpathpw = " --datadir " + options.nwpath + " ";
	nwalletpathpw = " --wallet " + options.nwfilename + " ";

	if not os.path.isfile(options.pwpath + 'pywallet.py'):
		print "\nError: " + options.pwpath + "pywallet.py doesn't exist!\n"
		parser.print_help()
		exit(0)

	if options.wpath is not None and not os.path.isfile(options.wpath + options.wfilename):
		print "\nError: " + options.wpath + options.wfilename + " doesn't exist!\n"
		parser.print_help()
		exit(0)

	if options.nwpath is not None and not os.path.isfile(options.nwpath + options.nwfilename):
		print "\nError: " + options.nwpath + options.nwfilename + " doesn't exist!\n"
		parser.print_help()
		exit(0)

	if options.nwpath == options.wpath and options.nwfilename == options.wfilename :
		print "\nNew wallet MUST NOT be old wallet\n"
		parser.print_help()
		exit(0)


	print("Dumping...")
	a=os.popen(options.pwpath + "pywallet.py --dumpwallet " + walletpathpw + walletfilenamepw, "r")
	json_db = json.loads(a.read())
	a.close()
	print("OK")


	for value in json_db['keys']:
		i+=1
		os.system(options.pwpath + "pywallet.py --importprivkey=" + value['sec'] + nwalletpathpw + nwalletfilenamepw)
		disp(1.0*i/len(json_db['keys']))


	print("")
	print("Done") 


if __name__ == '__main__':
	main()



