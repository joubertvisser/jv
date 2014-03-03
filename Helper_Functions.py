#Selenium imports
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchFrameException
#Python imports
import time
import unittest
import csv

class HelperFunctions():
    #Variables to store values from config file
    product = None
    username = None
    password = None

    xpaths = None
    
    def __init__(self, driver):
        self.driver = driver

    #Don't access the config file every time a test needs a value, access the file once and then store the value in a variable    
    def get_product(self):
        if self.product is None:
            self.product = self.__get_config_value("Product")
            return self.product
        else:
            return self.product

    def get_username(self):
        if self.username is None:
            self.username = self.__get_config_value("Username")
            return self.username
        else:
            return self.username

    def get_password(self):
        if self.password is None:
            self.password = self.__get_config_value("Password")
            return self.password
        else:
            return self.password

    #Gets value from config.txt file which is set up as a series of name/value pair separated by '='. Input parameter should match one of the left side values in the config file.
    #The function will return the value to the right of the '=' in the file (e.g. Password=12345678 in config file will return 12345678 when 'Password' is passed to this function).
    #This is a private function that is not accessible by the test cases.     
    def __get_config_value(self, value):
        try:
            file = open('config/config.txt', 'r')
            found = False
            for line in file:
                if not line.find(value) == -1:
                    #partition returns a 3-tuple (left side value, separator, right side value)
                    line_tuple = line.partition("=")
                    found = True
                    break
            if not found:
                return value + " not found"
            else:
                return line_tuple[2].strip()
            
        except IOError, e: return "Error accessing config file"

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def load_xpath_dictionary(self):
        if self.xpaths is None:
            with open('config/xpath.csv', 'rb') as file:
                reader = csv.reader(file)
                self.xpaths = {rows[0]:rows[1] for rows in reader}
            
    #Store the xpath values all in one place. 
    def get_xpath(self, what, text=""):
        if text == "":
            return self.xpaths[what]
        else:
            for case in switch(what):
                #The Asks cell for the given price
                if case('mdt_asks_cell_at_price'):
                    return "//div[div[contains(text(),'" + text + "')]]/div[contains(@class, 'ask-cell')]"
                #The Bids cell for the given price
                if case('mdt_bids_cell_at_price'):
                    return "//div[div[contains(text(),'" + text + "')]]/div[contains(@class, 'bid-cell')]"

        return ""
            
    def is_valid_connection(self):
        what = "online-ind"
        if not self.is_element_present("id", what):
            return "Could not find '" + what + "'"
        iterator = 0
        while iterator < 10:
            element = self.driver.find_element_by_id(what)
            attribute = element.get_attribute("data-original-title")
            if attribute == 'Connected':
                break
            else:
                iterator += 1
                time.sleep(1)
        return attribute

    def send_order(self, is_buy=True, qty=1, price=0):
        for case in switch(qty):
            if case(1):
                #Set Qty to 1
                what = self.get_xpath("mdt_qty1_btn")
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
                self.driver.find_element_by_xpath(what).click()
                break
            if case(2, 3, 4, 6, 7, 8, 9):
                what = self.get_xpath("mdt_qty1_btn")
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
                for i in range(0, qty):
                    self.driver.find_element_by_xpath(what).click()
                break
            if case(5):
                #Set Qty to 5
                what = self.get_xpath("mdt_qty5_btn")
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
                self.driver.find_element_by_xpath(what).click()
                break
            if case(10):
                #Set Qty to 10
                what = self.get_xpath("mdt_qty10_btn")
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
                self.driver.find_element_by_xpath(what).click()
                break
            if case(25):
                #Set Qty to 25
                what = self.get_xpath("mdt_qty25_btn")
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
                self.driver.find_element_by_xpath(what).click()
                break
            if case(50):
                #Set Qty to 50
                what = self.get_xpath("mdt_qty50_btn")
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
                self.driver.find_element_by_xpath(what).click()
                break
            if case(100):
                #Set Qty to 100
                what = self.get_xpath("mdt_qty100_btn")
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
                self.driver.find_element_by_xpath(what).click()
                break
            if case(0):
                #Use whatever value is in the next qty field
                break

        #If price is 0 then just enter bid at any price that has a bid qty or offer at any price that has an offer qty
        if price == 0:
            if is_buy:
                self.driver.find_element_by_xpath(self.get_xpath("mdt_bid_has_value")).click()
                #Verify bid is resting in the market
                what = self.get_xpath("mdt_working_order_bid")
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
            else:
                self.driver.find_element_by_xpath(self.get_xpath("mdt_ask_has_value")).click()
                #Verify ask is resting in the market
                what = self.get_xpath("mdt_working_order_ask")
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        else: 
            if is_buy:
                self.driver.find_element_by_xpath(self.get_xpath("mdt_bids_cell_at_price", str(price))).click()
                #Verify bid is resting in the market
                what = self.get_xpath("mdt_working_order_bid")
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
            else:
                self.driver.find_element_by_xpath(self.get_xpath("mdt_asks_cell_at_price", str(price))).click()
                #Verify ask is resting in the market
                what = self.get_xpath("mdt_working_order_ask")
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))

    def validate_order(self, is_buy=True, qty=1, contract=None, price=None, tif="DAY"):
        #Use the last row in the order book
        orders = self.driver.find_elements_by_xpath(self.get_xpath("ob_window_orders"))
        num_orders = len(orders)
        
        if is_buy:
            b_s = 'B'
        else:
            b_s = 'S'
        element = orders[num_orders - 1].find_element_by_xpath(self.get_xpath("ob_buy_sell"))
        if b_s != element.text:
            return "Buy/Sell is incorrect, expected: '" + b_s + "' actual: '" + element.text + "'"

        element = orders[num_orders - 1].find_element_by_xpath(self.get_xpath("ob_qty"))
        if str(qty) != element.text:
            return "Qty is incorrect, expected: " + str(qty) + " actual: " + element.text

        #Don't validate the price if it is not passed in to the function
        if price is not None:
            element = orders[num_orders - 1].find_element_by_xpath(self.get_xpath("ob_price"))
            if str(price) != element.text:
                return "Price value is incorrect, expected: " + str(price) + " actual: " + element.text     

        #Don't validate the contract if it is not passed in to the function
        if contract is not None:
            element = orders[num_orders - 1].find_element_by_xpath(self.get_xpath("ob_contract"))
            if contract != element.text:
                return "Contract value is incorrect, expected: " + contract + " actual: '" + element.text

        element = orders[num_orders - 1].find_element_by_xpath(self.get_xpath("ob_tif"))
        if tif != element.text:
            return "TIF value is incorrect, expected: '" + tif + "' actual: '" + element.text + "'"

        return "OK"

    def populate_workspace(self, windows_to_open):
        for item in windows_to_open:
            for case in switch(item):
                if case('mdt'):
                    #Enter product in search field
                    element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.get_xpath("instrument_search"))))
                    product = self.get_product()
                    element.send_keys(product)

                    #Click on the first search result and verify that MDT for that contract appears
                    what = self.get_xpath("instrument_search_results")
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
                    elements = self.driver.find_elements_by_xpath(what)
                    search_result_title = elements[0].text
                    elements[0].click()
                    what = self.get_xpath("mdt_title")
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
                    #Wait for the prices to display
                    what = self.get_xpath("mdt_bid_has_value")
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
                    break
                if case('order_book'):
                    element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.get_xpath("plus_icon"))))
                    element.click()
                    element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.get_xpath('add_new_order_book'))))
                    element.click()
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.get_xpath('ob_window'))))
                    break
                if case('fills'):
                    element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.get_xpath("plus_icon"))))
                    element.click()
                    element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.get_xpath('add_new_fills_window'))))
                    element.click()
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, self.get_xpath('fills_window'))))
                    break
                #default
                if case(): 
                    return False

        return True

    def open_new_workspace(self, workspace_name):
        what = self.get_xpath("launch_workspace_btn")
        before_workspace_count = len(self.driver.find_elements_by_xpath(what))

        what = self.get_xpath("create_workspace_btn")
        create_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
        create_button.click()

        #Enter workspace name and save it
        what = "entityName"
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.NAME, what)))
        element.send_keys(workspace_name)
        what = self.get_xpath("save_workspace_btn")
        element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, what)))
        element.click()

        #Wait for the new workspace button to appear
        what = self.get_xpath("launch_workspace_btn")
        elements = self.driver.find_elements_by_xpath(what)
        after_workspace_count = len(elements)
        count = 0
        while before_workspace_count != (after_workspace_count - 1):
            time.sleep(1)
            elements = self.driver.find_elements_by_xpath(what)
            after_workspace_count = len(elements)
            print after_workspace_count
            if count >= 5:
                return "Timed out waiting for new workspace to appear"

        #Find new workspace and click on it
        found = False
        workspace_id = 1
        for element in elements:
            if workspace_name in element.text:
                found = True
                break
            workspace_id += 1
        if not found:
            return "Could not find the workspace name " + workspace_name
        else:
            self.driver.find_element_by_xpath("//div[@id='user-workspaces']/fieldset[@id='workspaces_section']/a[" + str(workspace_id) + "]").click()

        return "OK"

    def open_existing_workspace(self, workspace_name):
        what = self.get_xpath("launch_workspace_btn")
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))

        #Search for the workspace and click on it
        found = False
        workspace_id = 1
        elements = self.driver.find_elements_by_xpath(what)
        for element in elements:
            print element.text
            if workspace_name in element.text:
                found = True
                break
            workspace_id += 1
        if not found:
            return "Could not find the workspace name " + workspace_name
        else:
            self.driver.find_element_by_xpath("//div[@id='user-workspaces']/fieldset[@id='workspaces_section']/a[" + str(workspace_id) + "]").click()
        
        return "OK"

    def delete_workspace(self):
        #Don't delete the default "Take the Tour" workspace, just close the workspace
        if self.driver.title == "Take the Tour":
            self.driver.close()
            return True

        #Click on the cog icon and then select the delete workspace option
        what = self.get_xpath("cog_icon")
        cog_icon = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
        cog_icon.click()
        what = self.get_xpath("delete_workspace")
        delete_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
        delete_button.click()

        #If there are no widgets then clicking the delete workspace option will close the workspace so wait a few seconds for it to close and then switch to the open window
        #(TODO: Figure out a better way to wait for the window to close)
        time.sleep(2)
        self.driver.switch_to_window(self.driver.window_handles[-1])

        #The confirmation page will only appear if there are widgets on the workspace so ignore the timeout if the confimration doesn't appear
        what = self.get_xpath("delete_workspace_confirmation")
        wait = WebDriverWait(self.driver, 5)
        try:
            confirmation_window = wait.until(EC.element_to_be_clickable((By.XPATH, what)))
        except TimeoutException, e:
            return True
        if self.is_element_present("xpath", what):
            what = self.get_xpath("delete_workspace_confirmation_yes_btn")
            yes_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
            yes_button.click()
            #Wait a few seconds for the workspace window to close (TODO: Figure out a better way to wait for the window to close)
            time.sleep(2)

#Python does not provide a 'switch' statement so this class (taken from http://code.activestate.com/recipes/410692/) replicates the 'switch' functionality
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
