import requests
import argparse
import re
import os

RED = "\033[1;31m"
GREEN = "\033[1;32;0m"
OKBLUE = "\033[94m"
WHITE = "\033[0;37m"

parser = argparse.ArgumentParser(description="Subdomain Takeover Scanner")
parser.add_argument(
	'-l',
	'--list',
	default='',
	help='python3 ItsOver.py [-l, --list] file contain list of domains'
)

args = parser.parse_args()
domainList = args.list

print(""" ______   __               _____                           
/\__  _\ /\ \__           /\  __`\                         
\/_/\ \/ \ \ ,_\   ____   \ \ \/\ \  __  __     __   _ __  
   \ \ \  \ \ \/  /',__\   \ \ \ \ \/\ \/\ \  /'__`\/\`'__\\
    \_\ \__\ \ \_/\__, `\   \ \ \_\ \ \ \_/ |/\  __/\ \ \/ 
    /\_____\\\\ \__\/\____/    \ \_____\ \___/ \ \____\\\\ \_\ 
    \/_____/ \/__/\/___/      \/_____/\/__/   \/____/ \/_/ 

-- Coded By SaadAhmed a.k.a InjectorPCA 
""")

if len(str(domainList)) > 0:
	if os.path.isfile(domainList):
		readWords = open(domainList, 'r')

	else:
		exit("{}File Not Found Unable To Load Targets".format(RED))	
	
	print("{}[+] Loading Targets.... [+]\033[94m\n".format(WHITE))			
	subList = []
	vuln = []	
	validUrls = open('validUrls.txt', 'a')
	Takeover = open('Takeover.txt', 'a')

	for words in readWords:
		if not words.isspace():
			words = words.rstrip()
			words = words.replace("https://", "")
			words = words.replace("http://", "")
			words = words.replace("https://www.", "")
			words = words.replace("http://www.", "")
			words = words.replace("/", "")
			words = "http://{}".format(words)
			
			try:
				requests.get("{}".format(words.rstrip()), timeout=5)

			except (ConnectionError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.InvalidURL):
				print(RED,"!! Error => {}\033[94m".format(words.rstrip()))

			else:
				print("-- Adding {}".format(words))
				subList.append(words)
				validUrls.write("{}\n".format(words))
	
	validUrls.close()
	readWords.close()

	if len(subList) > 0:
		print(WHITE,"\n[!] Total {} Targets Loaded [!]\033[94m".format(len(subList)))
		print("{}[!] Checking For Subdomain Takeover..... [!]\n\033[94m".format(WHITE))
		
		VulnContents = ["<strong>Trying to access your account",
		"Use a personal domain name",
		"The request could not be satisfied",
		"Sorry, We Couldn't Find That Page",
		"Fastly error: unknown domain",
		"The feed has not been found",
		"You can claim it now at",
		"Publishing platform",                        
		"There isn't a GitHub Pages site here",                       
		"No settings were found for this company",
		"Heroku | No such app",
		"<title>No such app</title>",                        
		"You've Discovered A Missing Link. Our Apologies!",
		"Sorry, couldn&rsquo;t find the status page",                        
		"NoSuchBucket",
		"Sorry, this shop is currently unavailable",
		"<title>Hosted Status Pages for Your Company</title>",
		"data-html-name=\"Header Logo Link\"",                        
		"<title>Oops - We didn't find your site.</title>",
		"class=\"MarketplaceHeader__tictailLogo\"",                        
		"Whatever you were looking for doesn't currently exist at this address",
		"The requested URL was not found on this server",
		"The page you have requested does not exist",
		"This UserVoice subdomain is currently available!",
		"but is not configured for an account on our platform",
		"<title>Help Center Closed | Zendesk</title>",
		"Sorry, We Couldn't Find That Page Please try again"]

		for domain in subList:
			print("{}[-] Checking {} [-]\033[94m".format(WHITE, domain))		
			try:
				subDoamin = requests.get("{}".format(domain.rstrip()), timeout=5).text
				for VulnContent in VulnContents:
					if VulnContent in subDoamin:
						print("{}    >>-----> Vulnerable {}\033[94m \n".format(GREEN, domain))
						vuln.append(domain)
						Takeover.write(domain)

				if not domain in vuln:
					print("{}  -- Not Vulnerable {}\033[94m\n".format(OKBLUE, domain))
					
			except requests.exceptions.ReadTimeout:
					print(RED,"!! Timeout => {}\033[94m".format(words.rstrip()))			
		
		Takeover.close()				
else:
	print("\nSubdomain Takeover Scanner\nAuthor: SaadAhmed a.k.a InjectorPCA\nContact: http://facebook/InjectorPCA\n\n\t--help, -h: Show Help\n\t--list, -l: file contain list of domains\n")   	
