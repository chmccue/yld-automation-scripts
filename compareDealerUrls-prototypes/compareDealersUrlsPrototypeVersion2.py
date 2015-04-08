from selenium import webdriver
import unittest, time, datetime
import win32com.client  # This has to be downloaded and installed for AutoIt to be called by the script
import pyperclip  # This library needs to be downloaded and put into the "Lib" folder in the Python directory


# returns the current date and time when creating the file to write to.
def currentTime():
    return datetime.datetime.now().strftime('%m-%d-%y, %H%M%S')

# returns the current date and time to print into the file with a recognizable format.
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
fileOut = open('Compare Dealers Report - ' + (model) + ' - ' + (currentTime()) + '.txt', 'a+')

base_url = 'http://studiopreviewpages.appspot.com/... insert full base url here ...&zip='


class DealerLinkChecks(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        print 'Start of ' + (section) + ' unit test, ' + timeStamp()
        fileOut.write('Start of ' + (model) + ' ' + (section) + ' unit test, ' + timeStamp() + '\n')
        
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
            fileOut.write('\n' + num + ' - ' + dealerName)
            print act_url + output();
            fileOut.write('\n' + act_url + output())
            print (exp_url) + dealerURL + URL_IS;
            fileOut.write('\n' + (exp_url) + dealerURL + URL_IS)
             
            if output() != dealerURL + URL_IS:
                print "URL does not match - FAIL"
                fileOut.write("\nURL does not match - FAIL\n")
            else:
                print "URL Match - PASS"
                fileOut.write("\nURL Match - PASS\n")
            
            autoit.send("^w")
            
    
    def tearDown(self):
        self.driver.close()
        print '\n' + 'END OF ' + (section) + ' unit test: ' + timeStamp()
        fileOut.write('\n' + '\n' + 'END OF ' + (model) + ' ' + (section) + ' unit test: ' + timeStamp())


if __name__ == "__main__":
    unittest.main()
    