# Place holder for now.
from crunchBase import Crunchbase
import pandas as pd
import time



def main():

   API_KEY = "KEY GOES HERE"
   df = pd.DataFrame()

   api = Crunchbase(API_KEY)

   #inputting excel sheet into dataframe
   df = pd.read_excel("sheet.xlsx")

   #Getting a list of names from base excel sheet
   comapnyNames = api.return_company_from_excelFile("./sheet.xlsx")

   #Getting list of permalinks
   stuff = api.make_permalink(comapnyNames)

   #Getting number of event rounds
   numOfEvents = []
   #Getting total numerical funding
   totalFunding = []
   #Returning if "comapny" exists in California
   inCalifornia = []
   #Return websites
   websites = []
   
   for link in range(0,len(stuff)):
      time.sleep(5)
      numOfEvents.append(api.getNumberOfRaisedFundingRounds(stuff[link]))
      time.sleep(5)
      totalFunding.append(api.getTotalFunding(stuff[link]))
      time.sleep(5)
      inCalifornia.append(api.determineIfLocationCA(stuff[link]))
      time.sleep(5)
      websites.append(api.getWebistes(stuff[link]))
   
   #Inputting information in Data Frame
   #Inputting total events
   print(df.count())
   print(len(numOfEvents))
   print(len(totalFunding))
   print(len(inCalifornia))
   print(len(websites))

   df["Total Events"] = numOfEvents

   #Inputting information into 
   df["Total Funding"] = totalFunding

   #Inputting in Californa
   df["In California?"] = inCalifornia

   #Websites
   df["Website"] = websites

   df.to_excel("./output.xlsx")


if __name__ == "__main__":
   main()