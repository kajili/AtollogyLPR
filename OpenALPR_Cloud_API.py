# This is a script made to send a file to the OpenALPR Cloud API Service for recognition
# The image path needs to be changed manually for now
# The Secret Key is from my OpenALPR Cloud API Account (cloud.openalpr.com)
# Usage: `python OpenALPR_Cloud_API.py <image-path>`

# To set up environment see: https://github.com/kajili/AtollogyLPR/wiki#to-setup-the-openalpr_cloud_apipy-script


import time
import json
import openalpr_api
import sys
from openalpr_api.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = openalpr_api.DefaultApi()
image = sys.argv[1] # file | The image file that you wish to analyze 

secret_key = 'sk_01a75f02eca170f3a5d23073' # str | The secret key used to authenticate your account.  You can view your  secret key by visiting  https://cloud.openalpr.com/ 

country = 'us' # str | Defines the training data used by OpenALPR.  \"us\" analyzes  North-American style plates.  \"eu\" analyzes European-style plates.  This field is required if using the \"plate\" task  You may use multiple datasets by using commas between the country  codes.  For example, 'au,auwide' would analyze using both the  Australian plate styles.  A full list of supported country codes  can be found here https://github.com/openalpr/openalpr/tree/master/runtime_data/config 

recognize_vehicle = 0 # int | If set to 1, the vehicle will also be recognized in the image This requires an additional credit per request  (optional) (default to 0)

state = '' # str | Corresponds to a US state or EU country code used by OpenALPR pattern  recognition.  For example, using \"md\" matches US plates against the  Maryland plate patterns.  Using \"fr\" matches European plates against  the French plate patterns.  (optional) (default to )

return_image = 0 # int | If set to 1, the image you uploaded will be encoded in base64 and  sent back along with the response  (optional) (default to 0)

topn = 10 # int | The number of results you would like to be returned for plate  candidates and vehicle classifications  (optional) (default to 10)

prewarp = '' # str | Prewarp configuration is used to calibrate the analyses for the  angle of a particular camera.  More information is available here http://doc.openalpr.com/accuracy_improvements.html#calibration  (optional) (default to )

try: 
    api_response = api_instance.recognize_file(image, secret_key, country, recognize_vehicle=recognize_vehicle, state=state, return_image=return_image, topn=topn, prewarp=prewarp)
    
    #print(api_response)
    if not api_response.results:
	print("No license plates found.")
    else:
	parsedResponse = api_response.results[0].plate
	print(parsedResponse)
	# Uncomment if you want to check how many credits have been used
    	#pprint(api_response.credits_monthly_used)
except ApiException as e:
    print "Exception when calling DefaultApi->recognize_file: %s\n" % e
