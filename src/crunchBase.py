import pandas as pd
import requests
import json
import os

class Crunchbase:
   '''
   A object desigend to utalize the Crunchbase Rest API with Python to extract and find different companies
   Delcaration Example: database = Crunchbase("698e40ad22a4bd98abbaac2e909a64b5")
   Note: USE YOUR OWN API KEY 
   '''

   def __init__(self,  USER_API):
      self.USER_API = USER_API
      self.cards = []
   
   def findError(self, jsonObj):
      try:
         if (jsonObj["code"] == "CS404"):
            print("Company dosent exsist: ", jsonObj)
            return False
         else:
            print("Something eles happneded in finding error: ",jsonObj)
            return False
      except:
         return True

   # This creates for an excel file
   def return_company_from_excelFile(self, file_path):
      '''
      This will return a list of companies under the column called 'COMPANY'
      As well as make the companies all lower case

      Calling example: x = return_company_from_excelFile("spreadsheet.xlsx")
      '''
      # Create a list and read from the excel file
      company_list = list()
      self.df = pd.read_excel(file_path)
      for company in self.df['COMPANY']:
         # Make sure the instance is a company and a string
         if isinstance(company, str):
            company_list.append(company.lower())
      return company_list

   def make_permalink(self, company_list):
      '''
      This function will take a list of lowercase companies name, and create/return them into permalinks
      in order to use for Crunchbase REST API

      Calling example: x = make_permalink(company_list)
      '''
      permalinks = []
      for company in company_list:
         temp = company.replace(" ", "-")
         permalinks.append(temp)
      return permalinks
   
   def getNumberOfFundingRounds(self, permalink):
      '''
      Returns the number of funding rounds of a particular permalink.
      '''
      #Returns the json tree with specific card_ids
      try:
         URL = "https://api.crunchbase.com/api/v4/entities/organizations/" + permalink + "?card_ids=investors&user_key=" + self.USER_API
         response = requests.get(URL)
         jsonObj = response.json()
         # TO DO: Enter error function
         return len(response["cards"]["investors"])
      except json.decoder.JSONDecodeError:
         print("Json Decoding Error")
         print("Attempted to decode: ", response)
         return "n/a"
      except:
         print("Something elese went wrong")
         print(response)
         return "n/a"

      

   def getNumberOfRaisedFundingRounds(self, permalink):
      '''
      Returns the number of funding events of a particular permalink.
      '''
      try:
         URL = "https://api.crunchbase.com/api/v4/entities/organizations/" + permalink + "?card_ids=raised_funding_rounds&user_key=" + self.USER_API
         response = requests.get(URL)
         jsonObj = response.json()
         if(self.findError(jsonObj)):
            return len(jsonObj['cards']['raised_funding_rounds'])
      except json.decoder.JSONDecodeError:
         print("Json Decoding Error")
         print("Attempted to decode: ", response)
         return "n/a"
      except:
         print("Something elese went wrong")
         print(response)
         return "n/a"

   def getTotalFunding(self, permalink):
      '''
      Returns the total amount of investment in $ amount for a particular permalink.
      '''
      
      try:
         URL = "https://api.crunchbase.com/api/v4/entities/organizations/" + permalink + "?card_ids=raised_funding_rounds&user_key=" + self.USER_API
         response = requests.get(URL)
         jsonObj = response.json()
      except json.decoder.JSONDecodeError:
         print("Json Decoding Error")
         print("Attempted to decode: ", response)
         return "n/a"
      except:
         print("Something elese went wrong")
         return "n/a"

      if(self.findError(jsonObj)):
         try:
            return jsonObj["cards"]["raised_funding_rounds"][0]["funded_organization_funding_total"]["value_usd"]
         except IndexError:
            print("No funding rounds exist")
         except:
            print("Something went wrong")
            
      return "n/a"
      

      
   def getInvestments(self):
      '''

      '''
      pass

#Loop to add all investmnets
   def determineIfLocationCA(self, permalink):
      '''
      This function determines if the compnay is in "california"
      The requirments for if the compnay is in california:
      1. Check if company is based in California
      2. If not, check if each investor is (As long as one investor is in californa, its true)
      3. If not, its not base in california
      '''
      # Check if company is in california

      try:
         URL = "https://api.crunchbase.com/api/v4/entities/organizations/" + permalink + "?card_ids=headquarters_address&user_key=" + self.USER_API
         response = requests.get(URL)
         companyLocation = response.json()
      except json.decoder.JSONDecodeError:
         print("Json Decoding Error")
         print("Attempted to decode: ", response)
         return "n/a"
      except:
         print("Something elese went wrong")
         return "n/a"

      if(self.findError(companyLocation) == False):
         return "n/a"      

      try:
         if(companyLocation["cards"]["headquarters_address"][0]["region_code"] == "CA"):
            return True
      except:
         print(companyLocation)
         return False

      # if not, check if each investor is in california
      # if there is, put true for the company being in california
      try:
         investors = requests.get("https://api.crunchbase.com/api/v4/entities/organizations/" + permalink + "?card_ids=investors&user_key=" + self.USER_API).json()
      except json.decoder.JSONDecodeError:
         print("Json Decoding Error")
         print("Attempted to decode: ", response)
         return "n/a"
      except:
         print("Something elese went wrong")
         return "n/a"
      for i in range(0, len(investors["cards"]["investors"])):
         try:
            if(investors["cards"]["investors"][i]["location_identifiers"][1]["value"] == "California"):
               return True
         except KeyError:
            print("Problem with finding data in Json File")
            return False

      # if not, put false
      # the false/true attribute is a column in spreadsheet
      return False

   def getWebistes(self,permalink):
      '''
      Return websites for a given permalink
      '''
      try:
         URL = "https://api.crunchbase.com/api/v4/entities/organizations/" + permalink + "?card_ids=fields&user_key=" + self.USER_API
         response = requests.get(URL)
         websites = response.json()
      except json.decoder.JSONDecodeError:
         print("Json Decoding Error")
         print("Attempted to decode: ", response)
         return "n/a"

      if(self.findError(websites) == False):
         return "n/a"  
      try:
         return websites["cards"]["fields"]["website"]["value"]
      except KeyError:
         print(websites)
         




