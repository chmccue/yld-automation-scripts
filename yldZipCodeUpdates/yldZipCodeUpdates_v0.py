from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest, time, datetime
import win32com.client  # This has to be downloaded and installed for AutoIt to be called by the script
import pyperclip  # This library needs to be downloaded and put into the "Lib" folder in the Python directory
import csv  # This is for the import of the data in csv file format


# returns the current date and time for creating the file to print data to.
def currentTime():
    return datetime.datetime.now().strftime('%m-%d-%y, %H%M%S')

# returns the current date and time in a more readable format to be printed in the file.
def timeStamp():
    return datetime.datetime.now().strftime('%m/%d/%y, %H:%M:%S')


# Prints the name of the section at the start and end of the test under review.
section = "Flash Banner links to dealer specials"
# Prints the name of the model the test is for.  This is primarily for the creation of the report
model = "IS"
# Prints the expected URL along with the expected URL content being called for the specific test.
exp_url = 'expected URL: '
# Prints the actual URL along with the actual URL content being called for the specific test.
act_url = '  actual URL: '

# This is the file that the content is written to
# fileOut = open('Compare Dealers Report - ' + (model) + ' - ' + (currentTime()) + '.txt', 'a+')

zipList =   [
            [10530, "New York"],
            [93015, "Not http://www.yourlexusdealer.com/select_dealer.html"],
            [93016, "Not http://www.yourlexusdealer.com/select_dealer.html"],
            [93023, "Not http://www.yourlexusdealer.com/select_dealer.html"],
            [93024, "Not http://www.yourlexusdealer.com/select_dealer.html"],
            [93040, "Not http://www.yourlexusdealer.com/select_dealer.html"],
            [93060, "Not http://www.yourlexusdealer.com/select_dealer.html"],
            [93105, "Not http://www.yourlexusdealer.com/select_dealer.html"],
            [93130, "Not http://www.yourlexusdealer.com/select_dealer.html"],
            [93222, "http://www.yourlexusdealer.com/select_dealer.html"],
            [93225, "http://www.yourlexusdealer.com/select_dealer.html"],
            [76626, "Dallas-Ft. Worth"],
            [10522, "New York"],
            [10523, "New York"],
            [10530, "New York"],
            [10532, "New York"],
            [10533, "New York"],
            [10591, "New York"],
            [10602, "New York"],
            [10701, "New York"],
            [10706, "New York"],
            [93252, "http://www.dchlexusofsantabarbara.com"],
            [93254, "http://www.dchlexusofsantabarbara.com"],
            [93429, "http://www.dchlexusofsantabarbara.com"],
            [93434, "http://www.dchlexusofsantabarbara.com"],
            [93437, "http://www.dchlexusofsantabarbara.com"],
            [93440, "http://www.dchlexusofsantabarbara.com"],
            [93455, "http://www.dchlexusofsantabarbara.com"],
            [93458, "http://www.dchlexusofsantabarbara.com"],
            [29452, "Savannah"],
            [74301, "http://www.lexusoftulsa.com"],
            [74349, "http://www.lexusoftulsa.com"],
            [17062, "http://www.yourlexusdealer.com/select_dealer.html"],
            [29452, "http://www.yourlexusdealer.com/select_dealer.html"],
            [29817, "http://www.yourlexusdealer.com/select_dealer.html"],
            [93222, "http://www.yourlexusdealer.com/select_dealer.html"],
            [93225, "http://www.yourlexusdealer.com/select_dealer.html"],
            [93252, "http://www.yourlexusdealer.com/select_dealer.html"],
            ]


def matchIt(x, y):
    if x != y:
        return "FAIL//////////\\\\\\\\\\!!!!!!!!!!//////////\\\\\\\\\\!!!!!!!!!!//////////\\\\\\\\\\!!!!!!!!!!//////////\\\\\\\\\\!!!!!!!!!!"
    elif x == y:
        return "PASS"

base_url = 'http://studiopreviewpages...insert full url start here...zip='
# zip code goes in between these 2.
base_url_end = '&year=2014&model=IS&offer=LEASE&eventname=sustain&tracking=&offercolor=&preview=live'

class DealerLinkChecks(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(15)
        # fileOut.write('\nStart of ' + (model) + ' ' + (section) + ' unit test, ' + timeStamp() + '\n')
        print 'Start of ' + (model) + ' ' + (section) + ' unit test, ' + timeStamp()

    def test_dealerLinks(self):
        driver = self.driver
        '''
        # =======================================================================================
        # =======================================================================================
        # This takes the csv file that the script will use to compare what is found on the web page. 
        dealerList = open("C:\<rest of link to csv file goes here>\BannerLinks - IS.csv")
        csv_f = csv.reader(dealerList)
        sqlList = []

        for row in csv_f:
            sqlList.append(row[0:5])
        # =======================================================================================
        # =======================================================================================
        '''
        # This is the csv file that will compare the market and convert the market to the correct URL.
        marketToURLFile = open("C:\<rest of link to csv file goes here>\YLD-num_region_market_url.csv")
        csv_a = csv.reader(marketToURLFile)
        marketCompareList = []
        for row in csv_a:
            marketCompareList.append(row[2:4])

        for zip_code, dealerURL in zipList:
            driver.get(base_url + str(zip_code) + base_url_end)
            time.sleep(10)

 # commands that use autoit.  This works with autoit and pywin32 installed.
            autoit = win32com.client.Dispatch("AutoItX3.Control")
            autoit.MouseClick("left", 897, 718, 1, 15)
            time.sleep(3)
            autoit.MouseClick("left", 750, 50, 1)
            autoit.send("^a")
            time.sleep(1)
            autoit.send("^c")
            time.sleep(1)
            
            output = pyperclip.paste
            '''
            fileOut.write('\n' + num + ' - ' + dealerName)
            fileOut.write('\n' + act_url + output())
            fileOut.write('\n' + (exp_url) + dealerURL + endURL)
            '''
            print '\n' + str(zip_code) + ' - zip code used'
            print (exp_url) + dealerURL
            print act_url + output();
            print matchIt(dealerURL, output())
            
            autoit.send("^w")
            
    
    def tearDown(self):
        self.driver.close()
        # fileOut.write('\n' + '\n' + 'END OF ' + (model) + ' ' + (section) + ' unit test: ' + timeStamp())
        print '\n' + 'END OF ' + (model) + ' ' + (section) + ' unit test: ' + timeStamp()

if __name__ == "__main__":
    unittest.main()
    
