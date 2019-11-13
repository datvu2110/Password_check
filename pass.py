import requests
import hashlib
import sys

def main(args):
	for password in args:
		count = pwned_api_check(password)
		if count:
			print(f'{password} was found {count} times... you should probably change you password!!!')
		else:
			print(f'{password} was not found. Your password is safe!') 
	return "Done"

def pwned_api_check(password):
	decoded_pass = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	first5 = decoded_pass[:5]
	last   = decoded_pass[5:]
	url = 'https://api.pwnedpasswords.com/range/' + first5
	api_data = requests.get(url)

	if api_data.status_code != 200:
		raise RuntimeError("Check the API again")
		
	list_pass = (line.split(":") for line in api_data.text.splitlines())
	for h, count in list_pass:
		if h == last:
			return count
	return 0


main(sys.argv[1:])