
''' STARTING NOTES ABOUT SCRIPT
Required installs:
    Python 2 (written with version 2.7)
    Selenium Webdriver
    Chrome Driver for Selenium (Chrome browser is the most stable for use with this script)
    

With Chrome Driver, there is an error with the .quit() command in the teardown section of the unittest.  To get around it, 
please follow these steps:
    1 - In Chrome browser, go to chrome://settings/ > Network section > Change proxy settings button
    2 - In the Connections tab, click on the LAN settings button.
    3 - In the LAN settings menu, uncheck the "Bypass proxy server for locatl addresses" checkbox.
    4 - Click on Advanced tab.
    5 - In the Exceptions section, enter 127.0.0.1 and press the OK button.
    reference:  http://stackoverflow.com/questions/22018126/selenium-chromedriver-http-407-on-driver-quit
'''

# =======================================================================================================================================================
# =======================================================================================================================================================
# These are the module imports for the script.
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest, datetime, csv, os, time
from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.options import Options


# ==================================================================================================
# ==================================================================================================
# absolute dir the script is in.  This is for calling the redirect and listed csv files found in script.
script_dir = os.path.dirname(__file__)
# ==================================================================================================
# ==================================================================================================
# =======================================================================================================================================================
# =======================================================================================================================================================
# SETTING THE BROWSER(S) THAT SELENIUM WILL WORK WITH. For this particular script, only 1 browser needs to be reviewed, 
# and Chrome has shown to be the most stable for running this.

'''
chrome_options = Options()
chrome_options.add_argument("--test-type")
wd = webdriver.Chrome(chrome_options=chrome_options)
'''

wd = webdriver.Chrome()

'''
# These are rudimentary controls for Selenium Grid, via using Desired Capabilities.
wd = webdriver.Remote(
command_executor='http://127.0.0.1:4443/wd/hub',
desired_capabilities=DesiredCapabilities.FIREFOX)
'''
# =======================================================================================================================================================
# =======================================================================================================================================================
# =======================================================================================================================================================
# This function compares 2 values (x and y).  If they match, PASS is returned.  If they don't match, FAIL is returned.
# This function compares the expected output from the list to the content found on the web page and throws a pass/fail 
# if the content matches or not.
def matchIt(x, y):
    if x != y:
        return "<=================FAIL=================>"
    else:
        return "PASS"

# =======================================================================================================================================================
# =======================================================================================================================================================
# =======================================================================================================================================================
# This function is for models that appear in the excel doc differently than how they appear in the lease offer.
# eg:  CT appears as CTh in the lease doc, however on the site it appears as CT Hybrid.
def modelNameUpdater(x):
    if len(x) > 2 and x.endswith('h'):
        return x[0:2] + " HYBRID"
    elif x.endswith(' '):
        return x[:-1]
    elif len(x) > 2 and x.endswith('h') == False and x.endswith(' ') == False:
        return x[0:2] + ' ' + x[2:3]
    else:
        return x

# =======================================================================================================================================================
# =======================================================================================================================================================
# =======================================================================================================================================================
# This function removes a blank space at the end of an item in the list, only if there is a blank space.
# This had to be created because the yld offer doc sometimes has these blank spaces    
def spaceRemover(x):
    if x.endswith(' '):
        return x[:-1]
    else:
        return x
 
# =======================================================================================================================================================
# =======================================================================================================================================================
# =======================================================================================================================================================   
# This function runs through a list with 2 variables and if it finds a match, will replace 
# the text that is searched for with the text that matches in the list.  This is for redirecting 
# the market name to the market URL. 
def marketURLConverter(x, y):
    for marketRedirect, url in y:
        if x != marketRedirect:
            pass
        # elif x == None:
            # print (str(x) + " not in conversion list.")
        else:
            return url
            break
# =======================================================================================================================================================
# =======================================================================================================================================================
# =======================================================================================================================================================   
# returns the current date and time for creating the file to print data to.
def currentTime():
    return datetime.datetime.now().strftime('%m-%d-%y, %H%M%S')

# returns the current date and time in a more readable format to be printed in the file.
def timeStamp():
    return datetime.datetime.now().strftime('%m/%d/%y, %H:%M:%S')
 
base_url = 'http://www.yourlexusdealer.com/'

# This is the file that the content is written to
projectName = 'YLD Lease-Finance Offers '
fileOut = open(projectName + 'Report - ' + (currentTime()) + '.txt', 'a+')
print 'YLD Lease-Finance Offers Report - ' + (currentTime())

# =======================================================================================================================================================
# =======================================================================================================================================================
# =======================================================================================================================================================
# Internal script sandbox test offers that simulate what is in the csv file.  This is for testing purposes only and should be 
# commented out when the csv lease file is in use.

leaseOffer10 = ['41',"LEASE*", "Central", "Cleveland",'2015',"NX ","200t","","$369",'36',"$3,699"]
leaseOffer11 = ['42',"LEASE*", "Central", "Cleveland",'2015',"NX","200t","","$369",'36', "$3,699"]
'''
leaseOffer12 = ['43',"LEASE*", "Southern","Altoona",'2015',"IS ","350","AWD","$399",'27',"$2,999 "]
leaseOffer13 = ['44',"LEASE*", "Central", "Altoona",'2015',"IS ","350","AWD ","$350",'27', "$1,999 "]
leaseOffer14 = ['45',"LEASE*", "Central", "Altoona",'2014',"IS ","150","","$350",'28', "$1,999 "]
'''
leaseOffersList = [leaseOffer10, leaseOffer11]

# =======================================================================================================================================================
# =======================================================================================================================================================
# =======================================================================================================================================================

class yldLeaseOffers(unittest.TestCase):
    def setUp(self):
        self.driver = wd
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        fileOut.write('\nStart of YLD Lease/Finance Offers unit test, ' + timeStamp() + '\n')
        fileOut.write('\nOnly Fails, possible errors and absent messages will display in this file.  \nIf nothing appears below, no fails or errors were found by the script.' + timeStamp() + '\n')
        
    def test_yldOffers(self):
        driver = self.driver

        # This is the csv file that will compare the market and convert the market to the correct URL.
        marketToURLFile = open(script_dir + "\yldcsvfiles\YLD-num_region_market_url.csv")
        csv_a = csv.reader(marketToURLFile)
        marketCompareList = []
        for row in csv_a:
            marketCompareList.append(row[2:4])
    
        
        # This is where the yld lease offer doc that is updated monthly is input for review.  The file must first be parsed and converted 
        # as a csv file.  Fields needed from original excel doc:  offerCategory, region, market, year, model, description1, description2, 
        # offerAmount, offerTerm, downPayment
        '''
        leaseOffersFile = open(script_dir + "\yldcsvfiles\yld_010915.csv")
        csv_b = csv.reader(leaseOffersFile)
        leaseOffersList = []
        for row in csv_b:
            leaseOffersList.append(row[0:])
        '''

        for num, offerCategory, region, market, year, model, description1, description2, offerAmount, offerTerm, downPayment  in leaseOffersList:
            # This compares the market in the csv file with the market in the redirect file and provides us with 
            #  the correct URL to go to.
            marketURL = marketURLConverter(market, marketCompareList)
            # This loads the URL with information from the csv file.
            driver.get(base_url + marketURL + model)
            actualTitle = (driver.title)
            actualURL = (driver.current_url)
            time.sleep(2)

            print num
            # print 'Region: ' + region + ', Market: ' + market
            # This converts a model that falls under the modelNameUpdater function statements
            # into how it appears on the lease offer page.
            expModel = modelNameUpdater(model)
            expectedModelContent = spaceRemover(year) + spaceRemover(expModel) + spaceRemover(description1) + spaceRemover(description2)
            
            # This is the list for each possible offer number on the page.        
            offerRange = range(0,6)
            OFFERXPATH_PART1 = ".//*[@id='offer"
            # This variable is only needed if offer0 is on the page, however is not a Lease of Finance
            # offer.  There are some instances in markets where this is the case, and this variable 
            # helps resolve that issue when it's placed in the except of the below try/except.
            # offerType00 = ".//*[@id='offer0']/div[1]/span[1]"
            for i in offerRange:
                try:
                    offType = OFFERXPATH_PART1 + str(i) + "']/div[1]/span[1]"
                    modYear = OFFERXPATH_PART1 + str(i) + "']/div[1]/div[1]/span[1]"
                    modLetters = OFFERXPATH_PART1 + str(i) + "']/div[1]/div[1]/span[2]"
                    modNumbers = OFFERXPATH_PART1 + str(i) + "']/div[1]/div[1]/span[3]"
                    modDesc = OFFERXPATH_PART1 + str(i) + "']/div[1]/div[1]/span[4]"
                    # These are the offer variable locations that change month to month and need to be authenticated.
                    monPrice = OFFERXPATH_PART1 + str(i) + "']/div[1]/div[2]/span[1]"
                    monLongLease = OFFERXPATH_PART1 + str(i) + "']/div[1]/div[2]/span[3]"
                    DownPayment = OFFERXPATH_PART1 + str(i) + "']/div[1]/div[3]/span[1]"
                    monLongFinance = OFFERXPATH_PART1 + str(i) + "']/div[1]/div[3]/span[2]"

                    offerType = driver.find_element(By.XPATH, offType)
                    modelYear = driver.find_element(By.XPATH, modYear)
                    modelLetters = driver.find_element(By.XPATH, modLetters)
                    modelNumbers = driver.find_element(By.XPATH, modNumbers)
                    modelDescription = driver.find_element(By.XPATH, modDesc)
                    monthlyPrice = driver.find_element(By.XPATH, monPrice)
            
                    actualModelContent = modelYear.text + modelLetters.text + modelNumbers.text + modelDescription.text
                    time.sleep(2)
                    if offerCategory == offerType.text and (expectedModelContent) == (actualModelContent):
                        
                        if offerCategory == "LEASE*":
                            monthsLong = driver.find_element(By.XPATH, monLongLease)
                            expofferAmount = spaceRemover(offerAmount)
                            expofferTerm = spaceRemover(offerTerm)
                            expdownPayment = spaceRemover(downPayment)
                            
                            expectedPriceLease = (offerCategory + ', ' + expectedModelContent + 
                            ', ' + expofferAmount + ', ' + expofferTerm + ', ' + expdownPayment)
                            leaseDownPayment = driver.find_element(By.XPATH, DownPayment)
                            
                            actualPrice = (offerType.text + ', ' + actualModelContent + ', ' 
                                           + monthlyPrice.text + ', ' + monthsLong.text 
                                           + ', ' + leaseDownPayment.text)

                            if expectedPriceLease == actualPrice:
                                '''
                                # matchIt compares the expected vs actual content and prints "PASS" if they match.
                                fileOut.write('\n' + expectedPriceLease + ' - ' + matchIt(expectedPriceLease, actualPrice))
                                '''
                                print expectedPriceLease + ' - ' + matchIt(expectedPriceLease, actualPrice)
                                # print matchIt(expectedPriceLease, actualPrice)
                                break
                            else:
                                # The content in the else statement is printed if the expected and actual content don't match.
                                # Theexpected offerCategory content (if it is a LEASE* or FINANCE* offer) is matched to the offerType.text on the website.

                                fileOut.write('\n' + num)
                                fileOut.write('\n' + actualTitle)
                                fileOut.write('\n' + actualURL)
                                fileOut.write("\n" + region + "\n" + market)
                                fileOut.write("\nExpected Offer Type: " + offerCategory)
                                fileOut.write("\n  Actual Offer Type: " + offerType.text)
                                fileOut.write("\nExpected Model Name: " + expectedModelContent)
                                fileOut.write("\n  Actual Model Name: " + actualModelContent)
                                fileOut.write("\nExpected Monthly Price: " + offerAmount)
                                fileOut.write("\n  Actual Monthly Price: " + monthlyPrice.text)
                                fileOut.write("\nExpected Months Long: " + offerTerm)
                                fileOut.write("\n  Actual Months long: " + monthsLong.text)
                                fileOut.write("\nExpected Downpayment: " + downPayment)
                                fileOut.write("\n  Actual Downpayment: " + leaseDownPayment.text)
                                fileOut.write('\n' + expectedPriceLease + '\n' + actualPrice)
                                # This throws a pass/fail if the actual content matches or differs from the expected content.
                                fileOut.write('\n' + matchIt(expectedPriceLease, actualPrice))
                                
                                
                                print 'Region: ' + region + ', Market: ' + market
                                print actualTitle
                                print actualURL
                                print "Expected Offer Type: " + offerCategory
                                print "  Actual Offer Type: " + offerType.text
                                print "Expected Model Name: " + expectedModelContent
                                print "  Actual Model Name: " + actualModelContent
                                print "Expected Monthly Price: " + offerAmount
                                print "  Actual Monthly Price: " + monthlyPrice.text
                                print "Expected Months Long: " + offerTerm
                                print "  Actual Months long: " + monthsLong.text
                                print "Expected Downpayment: " + downPayment
                                print "  Actual Downpayment: " + leaseDownPayment.text
                                # print 'Expected Line: ' + expectedPriceLease + '\n  Actual Line: ' + actualPrice
                                print matchIt(expectedPriceLease, actualPrice) + '\n'
                                
                                break
                            
                        elif offerCategory == "FINANCE*":
                            monthsLongFinance = driver.find_element(By.XPATH, monLongFinance)
                            expofferAmount = spaceRemover(offerAmount)
                            expofferTerm = spaceRemover(offerTerm)
                            expectedPriceFinance = offerCategory + ', ' + expectedModelContent + ', ' + expofferAmount + ', ' + expofferTerm
                            actualPrice = offerType.text + ', ' + actualModelContent + ', ' + monthlyPrice.text + ', ' + monthsLongFinance.text
                            if expectedPriceFinance == actualPrice:
                                '''
                                fileOut.write('\n' + expectedPriceFinance + ' - ')
                                fileOut.write(matchIt(expectedPriceFinance, actualPrice))
                                '''
                                print expectedPriceFinance + ' - ' + matchIt(expectedPriceFinance, actualPrice)
                                # print matchIt(expectedPriceFinance, actualPrice)
                                break
                            else:
                                fileOut.write('\n' + num)
                                fileOut.write('\n' + actualTitle)
                                fileOut.write('\n' + actualURL)
                                fileOut.write("\nExpected Offer Type: " + offerCategory)
                                fileOut.write("\n  Actual Offer Type: " + offerType.text)
                                fileOut.write("\nExpected Model Name: " + expectedModelContent)
                                fileOut.write("\n  Actual Model Name: " + actualModelContent)
                                fileOut.write("\nExpected Monthly Price: " + offerAmount)
                                fileOut.write("\n  Actual Monthly Price: " + monthlyPrice.text)
                                fileOut.write("\nExpected Financing Up To: " + offerTerm)
                                fileOut.write("\n  Actual Financing Up To: " + monthsLongFinance.text)
                                fileOut.write('\nExpected Line: ' + expectedPriceFinance + '\n  Actual Line: ' + actualPrice)
                                # This throws a pass/fail if the actual content matches or differs from the expected content.
                                fileOut.write('\n' + matchIt(expectedPriceFinance, actualPrice))
                                

                                print 'Region: ' + region + ', Market: ' + market
                                print actualTitle
                                print actualURL
                                print "Expected Offer Type: " + offerCategory
                                print "  Actual Offer Type: " + offerType.text
                                print "Expected Model Name: " + expectedModelContent
                                print "  Actual Model Name: " + actualModelContent
                                print "Expected Monthly Price: " + offerAmount
                                print "  Actual Monthly Price: " + monthlyPrice.text
                                print "Expected Financing Up To: " + offerTerm
                                print "  Actual Financing Up To: " + monthsLongFinance.text
                                print 'Expected Line: ' + expectedPriceFinance + '\n  Actual Line: ' + actualPrice
                                print matchIt(expectedPriceFinance, actualPrice) + '\n'
                                
                                break
                    else:
                        continue
                        '''
                        fileOut.write("\nskipped : " + offerCategory + ' - ' + expectedModelContent)
                        print "\nskipped expected: " + offerCategory + ' - ' + expectedModelContent
                        '''
                except NoSuchElementException:
                    # Added below if statement to skip the first offer if the offers do not start on the offer0 location.  
                    # Some markets had a "Contact your local Lexus dealer" text in this place, and therefore all offers after 
                    # offer0 were not being checked in these markets because the loop would break and move on to the next offer 
                    # in the list. Tested on 9/10/2014 and confirmed this works for skipping offer 0 if offer 0 does not comply 
                    # with above if/elif statements.
                    offerType00 = ".//*[@id='offer0']/div[1]/span[1]"
                    if offerCategory != "LEASE*" or offerCategory != "FINANCE*" and offType == offerType00:
                        continue
                    else:
                        fileOut.write("\n" + num)
                        fileOut.write("\nRegion: " + region + ', Market: ' + market)
                        fileOut.write("\n" + actualTitle + "\n" + actualURL)
                        fileOut.write("\nOffer Absent on page - expected: " + offerCategory + ' - ' + expectedModelContent)
                        fileOut.write("\nCheck offer on website manually.")
                        
                        print 'Region: ' + region + ', Market: ' + market
                        print actualTitle
                        print actualURL
                        print "Offer Absent on page - expected: " + offerCategory + ' - ' + expectedModelContent
                        print "Check offer on website manually." + '\n'
                        break
                    

    def tearDown(self):
        
        fileOut.write('\n' + '\n' + 'END OF YLD Lease/Finance Offers unit test: ' + timeStamp())
        fileOut.close()   
        print '\n' + 'END OF YLD Lease/Finance Offers unit test: ' + timeStamp()   
        self.driver.quit()    

if __name__ == "__main__":
    unittest.main()
