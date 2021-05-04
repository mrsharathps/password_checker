import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code!=200:
        raise RuntimeError(f'fetching error {response.status_code}, Check the api and try again')
    return response

def get_password_leak_counts(hashes, hash_to_check):
    hashes=(line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h==hash_to_check:
            return count
    return 0

def pwned_api_check(password):
   sha1password=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
   first5_char, tail = sha1password[:5],sha1password[5:]
   response=request_api_data(first5_char)
   print(first5_char, tail)
   return get_password_leak_counts(response, tail)

def main(args):
    for password in args:
        count=pwned_api_check(password)
        if count:
            print(f'Gosh!{password} was found {count} number of times and should change it')
        else:
            print(f'{password} was not leaked and carry on!!!!!')
    return 'Done'

if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))