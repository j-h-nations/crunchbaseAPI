import requests
import json

class Crunchbase(object):

   '''
   A object desigend to utalize the Crunchbase Rest API with Python to extract and find different companies
   Delcaration Example: database = Crunchbase("698e40ad22a4bd98abbaac2e909a64b5")
   Note: USE YOUR OWN API KEY 
   '''

   def __init__(self,  USER_API):
      self.USER_API = USER_API

   def look4Org (self):
      pass

