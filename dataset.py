# Packages
from requests import exceptions
import argparse
import requests
import cv2
import os

# Setup the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-s","--search", required=True, help="Add in the name of query")
ap.add_argument("-o", "--output", required=True, help="Add in the output directory")
args=vars(ap.parse_args())

# Setup for API Call to Bing Image Search
API_KEY = "7e54da1a8e8648c3a3efaf78a5e4271f"
maxResult = 450
GROUP = 50
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

# Exception Setup
EXCEPTIONS = set([IOError, FileNotFoundError, exceptions.RequestException,
                  exceptions.HTTPError,	exceptions.ConnectionError, exceptions.Timeout])

# # create folders
# try: 
#     os.mkdir("dataset")
#     os.mkdir("dataset/"+args["output"])
# except:
#         print("dataset folder exist")

# Setup API Call
search_item = args["search"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": search_item, "offset": 0, "count": GROUP}

# Perform search to get estimated number of results
print("Performing search on term: {}".format(search_item))
searchResult = requests.get(URL, headers=headers, params=params)
searchResult.raise_for_status()
results = searchResult.json()
estNumResults = min(results["totalEstimatedMatches"], maxResult)
numImages = 0

# Loop through all the groups 
for offset in range(0,estNumResults,GROUP):
    params["offset"] = offset
    search = requests.get(URL,headers=headers,params=params)
    search.raise_for_status()
    results = search.json()

    print("Saving group,{}, for item,{}".format(offset,search_item))

    # Download the image of each group
    for v in results["value"]:
        try:
            print("Trying save imapge: {}".format(v["contentUrl"]))
            image=requests.get(v["contentUrl"], timeout=30)
            
            ext = v["contentUrl"][v["contentUrl"].rfind("."):]
            p = os.path.sep.join([args["output"], "{}{}".format(str(numImages).zfill(8), ext)])
            
            # Save Image
            f = open(p, "wb")
            f.write(image.content)
            f.close()
        
        except Exception as e:
            if type(e) in EXCEPTIONS:
                print("Skipping image: {}".format(v["contentUrl"]))
                continue
        
        # Test that the download actually worked 
        image = cv2.imread(p)
        if(image is None):
            print("Cannot read. Deleting: {}".format(p))
            os.remove(p)
            continue
        
        numImages += 1
        




