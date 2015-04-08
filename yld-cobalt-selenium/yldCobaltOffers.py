from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, datetime, csv, time, os
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# ==================================================================================================
# ==================================================================================================
# absolute dir the script is in.  This is for calling the redirect and listed csv files found in script.
script_dir = os.path.dirname(__file__)

# ==================================================================================================
# ==================================================================================================

# SETTING THE BROWSER(S) THAT SELENIUM WILL WORK WITH. For this particular script, only 1 browser needs to be reviewed, 
# and Chrome has shown to be the most stable for running this.
chrome_options = Options()
chrome_options.add_argument("--test-type")
wd = webdriver.Chrome(chrome_options=chrome_options)

'''
# These are rudimentary controls for Selenium Grid, via using Desired Capabilities.
wd = webdriver.Remote(
command_executor='http://127.0.0.1:4443/wd/hub',
desired_capabilities=DesiredCapabilities.FIREFOX)


self.driver = webdriver.Remote(
command_executor='http://127.0.0.1:4443/wd/hub',
desired_capabilities=DesiredCapabilities.IE)
'''
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# This function compares 2 values (x and y).  If they match, PASS is returned.  If they don't match, FAIL is returned.
# This function compares the expected output from the list to the content found on the web page and throws a pass/fail 
# if the content matches or not.
def matchIt(x, y):
    if x != y:
        return "FAIL======================!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!=========!!!!!!!!!!!!"
    elif x == y:
        return "PASS"
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================   
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
    if x.endswith(' ') or x.endswith('  '):
        return x[:-1]
    else:
        return x
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# returns the current date and time for creating the file to print data to.
def currentTime():
    return datetime.datetime.now().strftime('%m-%d-%y, %H%M%S')

# returns the current date and time in a more readable format to be printed in the file.
def timeStamp():
    return datetime.datetime.now().strftime('%m/%d/%y, %H:%M:%S')
 
base_url = 'http://www.yourlexusdealer.com/cobalt/?dealerZip='

# This is the file that the content is written to
testName = "Cobalt Lease-Finance Offers - Top 15 Markets"
fileOut = open(testName + ' Report - ' + (currentTime()) + '.txt', 'a+')

# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
cobaltTab01 = ".//*[@id='createTab']/li[1]/a/img"
cobaltTab02 = ".//*[@id='createTab']/li[2]/a/img"
# cobaltTab_byModel = "a[class=\'IS\']"   # CSS SELECTOR location.  Example is for IS model

# example of final result: "a[class=\'" + model letters + "\']"
#  cobaltTab_byModel1 + model letters + cobaltTab_byModel2

cobaltTab_byModel1 = "a[class=\'"   # CSS SELECTOR location
cobaltTab_byModel2 = "\']"   # CSS SELECTOR location

# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================
# Test offers that simulate what is in the csv file.
# leaseOffer1 should return correct actual/expected matching content found in the first offer slot.

'''
# This checks offer 21 on a page and also checks if IS C reformats properly by adding the extra space in the name.
leaseOffer6 = ['6', 'LEASE*', 'Southern', 'Orlando/Melbourne', '2014', 'ISC', '250', '', '$479', '36', '$4,649']
# This checks how the program handles if there is a model in the list yet no match on the site.  Currently it's 
# throwing a NoSuchElementException that is halting the script from completing.
# leaseOffer7 = ['7', 'LEASE*', 'Southern', 'Orlando', '32792', '2015', 'IS', '350', 'AWD', '$399', '27', '$2,999']

# This checks how the program reformats the CTh model name to match content from the web page.

# THIS OFFER CURRENTLY THROWS AN ERROR THAT HALTS THE SCRIPT.  HIGH PRIORITY ISSUE FIX NEEDED.
# leaseOffer8 = ['8', 'LEASE*', 'Western', 'Los Angeles', '90245', '2014', 'CTh', '', '', '$299', '27', '$4,649']

# this will test how the script handles a model that does not appear on the web page.
# THIS OFFER CURRENTLY THROWS AN ERROR THAT HALTS THE SCRIPT.  HIGH PRIORITY ISSUE FIX NEEDED.
# leaseOffer9 = ['9', 'LEASE*', 'Western', 'Los Angeles', '90245', '2014', 'ISC', '250', '', '$479', '36', '$4,649']
# leaseOffer10 = ['1771',"LEASE*","WESTERN","Portland","2014","LX","570",'',"$1,289","36","$3,999 "]

leaseOffer1 = ['1', 'LEASE*', 'Western', 'Los Angeles', '2014', 'ES', '350', '', '$349', '27', '$2,499']
leaseOffer2 = ['2', 'FINANCE*', 'Western', 'Los Angeles', '2014', 'ES', '350', '', '0.9%', '60', '']
# leaseOffer2 should try/catch an exception error and keep going, since there is no offer in the 2 offer slots.
leaseOffer3 = ['3', 'FINANCE*', 'Western', 'Los Angeles', '2014', 'GS', '350', '', '0.9%', '60', '']
leaseOffer4 = ['4', 'FINANCE*', 'Eastern', 'New York', '2014', 'IS', '250', '', '0.9%', '60', '']
leaseOffer5 = ['5', 'LEASE*', 'Eastern', 'New York', '2015', 'IS', '350', 'AWD', '$399', '27', '$2,999']
#leaseOffersList = [leaseOffer1, leaseOffer2, leaseOffer3, leaseOffer4, leaseOffer5, leaseOffer6, leaseOffer7]
#leaseOffersList = [leaseOffer1, leaseOffer2, leaseOffer3, leaseOffer4, leaseOffer5, leaseOffer6]
#leaseOffersList = [leaseOffer6]
'''
# ==================================================================================================
# ==================================================================================================
# ==================================================================================================

class Test(unittest.TestCase):

    def setUp(self):
        # self.driver = webdriver.Chrome()
        
        self.driver = wd
        self.driver.maximize_window()
        self.driver.implicitly_wait(15)
        fileOut.write('\nStart of ' + testName + ' unit test, ' + timeStamp() + '\n')
        fileOut.write('\nOnly Fails, possible errors and absent messages will display in this file.  \nIf nothing appears below, no fails or errors were found by the script.' + timeStamp() + '\n')
        print 'Start of ' + testName + ' unit test, ' + timeStamp() + '\n'
        
    def tearDown(self):
        self.driver.quit()
        fileOut.write('\n' + '\n' + 'END OF ' + testName + ' unit test: ' + timeStamp())
        print '\n' + 'END OF ' + testName + ' unit test: ' + timeStamp() 

    def testName(self):
        driver = self.driver
        wait = WebDriverWait(driver, 20)

        # This is the csv file that will compare the market and convert the market to the correct URL.
        marketToURLFile = open(script_dir + "\yldcsvfiles\YLD-num_region_market_zip_url.csv")
        csv_a = csv.reader(marketToURLFile)
        marketCompareList = []
        for row in csv_a:
            marketCompareList.append(row[2:5])
            
            
        # This is where the yld lease offer doc that is updated monthly is input for review.  The file must first be parsed and converted 
        # as a csv file.  Fields needed from original excel doc:  offerCategory, region, market, year, model, description1, description2, 
        # offerAmount, offerTerm, downPayment
        leaseOffersFile = open(script_dir + "\yldcsvfiles\yld_030515_top15.csv")
        csv_b = csv.reader(leaseOffersFile)
        leaseOffersList = []
        for row in csv_b:
            leaseOffersList.append(row[0:])

        for num, offerCategory, region, market, year, model, description1, description2, offerAmount, offerTerm, downPayment  in leaseOffersList:
            
            def marketURLConverter(x):
                for marketRedirect, zip, url in marketCompareList:
                    if x == marketRedirect:
                        return zip
                        break
                    elif x != marketRedirect:
                        continue

            
            marketURL = marketURLConverter(market)
            
            driver.get(base_url + marketURL)
            actualTitle = (driver.title)
            actualURL = (driver.current_url)

            # This converts a model that falls under the modelNameUpdater function statements
            # into how it appears on the lease offer page.            
            expModel = modelNameUpdater(model)
            modelUpdatedForTabClick = spaceRemover(model)
            expectedModelContent = spaceRemover(year) + spaceRemover(expModel) + spaceRemover(description1) + spaceRemover(description2)
            try:
                cobaltTab_byModel = "a[class=\'" + modelUpdatedForTabClick + "\']"
                PAGE_TAB = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, cobaltTab_byModel)))
                # This is the range offer that will fill in the offer number in the locators.  This glues part 1 to part 2.
                offerRange = range(0,23)
                offerXPATH_PART1 = ".//*[@id='offer"
                for i in offerRange:
                    try:
                        PAGE_TAB.click()
                        time.sleep(2)
                        modLetters = offerXPATH_PART1 + str(i) + "']/div[1]/div[2]/div/div[1]/span[2]"
                        modelLetters = driver.find_element(By.XPATH, modLetters)
                        # modelTabCompare = modelNameUpdater(modelUpdatedForTabClick)
                        '''
                        if modelLetters.text != modelTabCompare:
                            print "searching..."
                            continue
                        '''

                        if len(modelLetters.text) == 0:
                            continue
                            # print "offer " + str(i)
                            # print "offer not yet found to match model name."
                            # print "searching..."

                        else:
                            offType = offerXPATH_PART1 + str(i) + "']/div[1]/div[1]/span"
                            modYear = offerXPATH_PART1 + str(i) + "']/div[1]/div[2]/div/div[1]/span[1]"
                            # modLetters = offerXPATH_PART1 + str(i) + "']/div[1]/div[2]/div/div[1]/span[2]"
                            modNumbers = offerXPATH_PART1 + str(i) + "']/div[1]/div[2]/div/div[1]/span[3]"
                            modDesc = offerXPATH_PART1+ str(i) + "']/div[1]/div[2]/div/div[1]/span[4]"
                            # These are the offer variable locations that change month to month and need to be authenticated.
                            monPrice = offerXPATH_PART1 + str(i) + "']/div[1]/div[2]/div/div[2]/span[1]"
                            monLongLease = offerXPATH_PART1 + str(i) + "']/div[1]/div[2]/div/div[2]/span[3]"
                            DownPayment = offerXPATH_PART1 + str(i) + "']/div[1]/div[2]/div/div[3]/span[1]"
                            monLongFinance = offerXPATH_PART1 + str(i) + "']/div[1]/div[2]/div/div[3]/span[2]"
    
                            offerType = driver.find_element(By.XPATH, offType)
                            # offerType = wait.until(EC.element_to_be_clickable((By.XPATH, offType)))
                            modelYear = driver.find_element(By.XPATH, modYear)
                            # modelLetters = driver.find_element(By.XPATH, modLetters)
                            modelNumbers = driver.find_element(By.XPATH, modNumbers)
                            modelDescription = driver.find_element(By.XPATH, modDesc)
                            monthlyPrice = driver.find_element(By.XPATH, monPrice)
                            actualModelContent = modelYear.text + modelLetters.text + modelNumbers.text + modelDescription.text
    
                            
                            if actualModelContent != expectedModelContent or (actualModelContent == expectedModelContent and offerType.text != offerCategory):
                                time.sleep(3)
                                # print "offer " + str(i)
                                # print "Either model name or offer Type do not match.  Next offer tab clicked."
                                # print "still searching..."
                                # i = i + 2
                                # print "'i' just before the try part: " + str(i)
                                try:
                                    i = i + 1
                                    # print "'i' in the try part: " + str(i)
                                    NEXT_OFFER_CLICK = driver.find_element(By.XPATH, offerXPATH_PART1 + str(i) + "']/div[1]/div[1]/span")
                                    NEXT_OFFER_CLICK.click()
                                    continue
                                except ElementNotVisibleException:  # NoSuchElementException
                                    print "\noffer element number on web site: " + str(i)
                                    print "offer number in list: " + num
                                    print 'Region: ' + region + ', Market: ' + market
                                    print actualTitle
                                    print actualURL
                                    print 'exception encountered when switching between offers on page.'
                                    i = i + 2
                                    print "'i' in the except part: " + str(i)
                                    NEXT_OFFER_CLICK = driver.find_element(By.XPATH, offerXPATH_PART1 + str(i) + "']/div[1]/div[1]/span")
                                    NEXT_OFFER_CLICK.click()
                                    continue
                                # finally:
                                    # NEXT_OFFER_CLICK.click()
                                    # continue
                            elif actualModelContent == expectedModelContent and offerType.text == offerCategory:
                                print "\noffer element number on web site: " + str(i)
                                print "offer number in list: " + num
                                print 'Region: ' + region + ', Market: ' + market
                                print actualTitle
                                print actualURL
                                # print "Model name and offer Type match"
                                
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
                                        # print "expected: " + expectedPriceLease  #+ matchIt(expectedPriceLease, actualPrice)
                                        print "  actual: " + actualPrice + " - " + matchIt(expectedPriceLease, actualPrice)
                                        break
                                    else:
                                        # The content in the else statement is printed if the expected and actual content don't match.
                                        # Theexpected offerCategory content (if it is a LEASE* or FINANCE* offer) is matched to the offerType.text on the website.


                                        fileOut.write("\noffer element number on web site: " + str(i))
                                        fileOut.write("\noffer number in list: " + num)
                                        fileOut.write('\nRegion: ' + region + ', Market: ' + market)
                                        fileOut.write('\n' + actualTitle)
                                        fileOut.write('\n' + actualURL)
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
                                        
                                        
                                        # print 'Region: ' + region + ', Market: ' + market
                                        # print actualTitle
                                        # print actualURL
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
                                        print 'Expected Line: ' + expectedPriceLease + '\n  Actual Line: ' + actualPrice
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
                                        # print expectedPriceFinance + ' - ' + matchIt(expectedPriceFinance, actualPrice)
                                        
                                        # print "expected: " + expectedPriceFinance  #+ matchIt(expectedPriceFinance, actualPrice)
                                        print "  actual: " + actualPrice + " - " + matchIt(expectedPriceFinance, actualPrice)
                                        # print matchIt(expectedPriceFinance, actualPrice)
                                        break
                                    else:
                                        fileOut.write("\noffer element number on web site: " + str(i))
                                        fileOut.write("\noffer number in list: " + num)
                                        fileOut.write('\nRegion: ' + region + ', Market: ' + market)
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
                                        
        
                                        # print 'Region: ' + region + ', Market: ' + market
                                        # print actualTitle
                                        # print actualURL
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
                                # print "offer " + str(i)
                                #print "offer was not found while going through offers.  Please check expected offer content "
                                #print "with actual offer content on webpage manually.  If that appears correct, it's likely "
                                #print "a problem with the script that needs to be corrected."
                                print "else statement received."

                    except NoSuchElementException, ElementNotVisibleException:
                        if i > 22:
                            
                            fileOut.write("\noffer element number on web site: " + str(i))
                            fileOut.write("\nAbsent on page.")
                            fileOut.write("\nAll offers were checked on the page and the following offer was not found: \n" + actualTitle + '\n' + actualURL)
                            fileOut.write("\nExpected Offer Type: " + offerCategory)
                            fileOut.write("\nExpected Model Name: " + expectedModelContent)
                            fileOut.write("\nExpected Monthly Price: " + offerAmount)
                            fileOut.write("\nExpected Months Long: " + offerTerm)
                            fileOut.write("\nExpected Downpayment: " + downPayment)
                            fileOut.write("\nPlease check URL (listed above) for lease offer on page.  If the offer is on the web page,")
                            fileOut.write("\nthen the issue lies within the script and will need to be reviewed for a possible fix.")
                            
                            print "\noffer element number on web site: " + str(i)
                            print "Absent on page."
                            print "All offers were checked on the page and the following offer was not found: "
                            print actualTitle
                            print actualURL
                            print "Expected Offer Type: " + offerCategory
                            print "Expected Model Name: " + expectedModelContent
                            print "Expected Monthly Price: " + offerAmount
                            print "Expected Months Long: " + offerTerm
                            print "Expected Downpayment: " + downPayment
                            print "Please check URL (listed above) for lease offer on page.  If the offer is on the web page, "
                            print "then the issue lies within the script and will need to be reviewed for a possible fix."
                            print "this is the exception from the second (inner) try/except wrap."
                            continue
                        if ElementNotVisibleException == True:
                            fileOut.write("\n Absent on page.")
                            fileOut.write("\noffer number in list: " + num)
                            fileOut.write('\nRegion: ' + region + ', Market: ' + market)
                            fileOut.write('\n' + actualTitle)
                            fileOut.write('\n' + actualURL)
                            print "\n Absent on page."
                            print "Offer wasn't found when clicking on the offer tabs within the model tab."
                            print "Please check URL (listed above) for lease offer on page.  If the offer is on the web page, "
                            print "then the issue lies within the script and will need to be reviewed for a possible fix."
                            print "this error message appeared because an ElementNotVisibleException was reached in the script."
                        else:
                            # print "offer " + str(i)
                            # print "searching... (exception was received)"
                            continue

            except NoSuchElementException, TimeOutException:
                fileOut.write("\nModel Tab absent on page checking offer " + str(i))
                fileOut.write("\n" + actualTitle + "\n" + actualURL + '\n' + model)
                print "\nModel Tab absent on page." + " checking offer" + str(i)
                print actualTitle
                print actualURL
                print model
                print "This indicates the top tab is either not present on the page or there was an error getting to"
                print "the top tab in the code.  Check if the tab is present on the actual web page, and if it is, then"
                print "check the code to see how the element is being located."
                print "this is the exception from the first (outer) try/except wrap."
                continue    


if __name__ == "__main__":
    unittest.main()
    #import sys;sys.argv = ['', 'Test.testName']