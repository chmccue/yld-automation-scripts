from selenium import webdriver
import unittest, time, datetime
import win32com.client  # This has to be downloaded and installed for AutoIT to be called by the script
import pyperclip  # This library needs to be downloaded and put into the "Lib" folder in the Python directory

# Global print statements.

# returns the current date and time
def currentTime():
    return datetime.datetime.now().strftime('%m/%d/%y, %H:%M:%S')
# Prints the name of the section at the start and end of the test under review.
section = "Flash Banner links to dealer specials"
# Prints the expected URL along with the expected URL content being called for the specific test.
exp_url = 'expected URL: '
# Prints the actual URL along with the actual URL content being called for the specific test.
act_url = '  actual URL: '


base_url = 'http://studiopreviewpages.appspot.com/... enter full base url here ...&zip='


class DealerLinkChecks(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        print 'Start of ' + (section) + ' unit test, ' + currentTime()

    def test_dealerLinks(self):
        driver = self.driver
        bigList = [ ['1', 'Reinhardt Lexus', '36117', 'http://www.reinhardtlexus.com', '/NewModelsPageDetails?p=2014_is'], ['2', 'Lexus of Mobile', '36606', 'http://www.lexusofmobile.com', '/NewModelsPageDetails?p=2015_is'], ['3', 'Tom Williams Lexus', '35210', 'http://www.tomwilliamslexus.com', '/NewModelsPageDetails?p=2015_is'] ]
 #       URL_IS = '/NewModelsPageDetails?p=2015_is'
        
        for num, dealerName, zip_code, dealerURL, URL_IS in bigList:
            driver.get(base_url + zip_code)
            time.sleep(3)

 # commands that use autoit.  This works with autoit and pywin32 installed.
            autoit = win32com.client.Dispatch("AutoItX3.Control")
            autoit.MouseClick("left", 897, 718, 1, 15)
            time.sleep(5)
            autoit.MouseClick("left", 750, 50, 1)
            autoit.send("^a")
            time.sleep(1)
            autoit.send("^c")
            time.sleep(1)
            
            output = pyperclip.paste
            print '\n' + num + ' - ' + dealerName
            print act_url + output();
            print (exp_url) + dealerURL + URL_IS;
            
             
            if output() != dealerURL + URL_IS:
                print "URL does not match - FAIL"
            else:
                print "URL Match - PASS"
            
            autoit.send("^w")
            
    
    def tearDown(self):
        self.driver.close()
        print '\n' + 'END OF ' + (section) + ' unit test: ' + currentTime()

if __name__ == "__main__":
    unittest.main()
    
