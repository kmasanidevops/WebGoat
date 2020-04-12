import sys
import requests
from pprint import pprint
import json

version = sys.argv[1]
appenv  = sys.argv[2]

url = 'http://app{env}.dev.masani.xyz'.format(env=appenv)

# Validation#1
print (" - Checking if the endpoint is reachable. ")
for num in range(10):
    response = requests.get(url, verify=False)

    if response.ok:
        print (" - Got successful response from the endpoint")
        pprint (response.text)

        if version in response.text:
            print(" - Expected version found.")
            sys.exit(0)
        else:
            print ("ERR: Version mismatch.")
            print ("Expected {} and found {}".format(version, response.text))
            sys.exit(1)

    else:
        print (" * Could not connect to the endpoint .. will retry again.")
        time.sleep(2)


