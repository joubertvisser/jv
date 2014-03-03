#Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#Python imports
import time
from datetime import datetime
import unittest
import HTMLTestRunner
#Local imports
import Helper_Functions

import logger 

class TestMarketDepthTrader(unittest.TestCase):

    #chrome_options = Options()
    #chrome_options.add_argument("-silent")
    #driver = webdriver.Chrome(chrome_options=chrome_options)

    driver = webdriver.Chrome()

    helper = Helper_Functions.HelperFunctions(driver)

    @classmethod
    def setUpClass(cls):
        cls.helper.load_xpath_dictionary()

        cls.driver.get("https://falcon.debesys.net")
        wait = WebDriverWait(cls.driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))

        #Login page
        element = cls.driver.find_element_by_name("email")
        element.send_keys(cls.helper.get_username())
        element = cls.driver.find_element_by_name("password")
        element.send_keys(cls.helper.get_password())
        element = cls.driver.find_element_by_tag_name("button")
        element.click()

        WebDriverWait(cls.driver, 10).until(EC.title_contains("Workspaces"))
    
    #@classmethod
    #def tearDownClass(cls):
    #    cls.driver.quit()

    #def setUp(self):
        
    def tearDown(self):
        #Delete all resting orders
        what = self.helper.get_xpath("ob_delete_all_btn")
        if self.helper.is_element_present("xpath", what):            
            self.driver.find_element_by_xpath(what).click()
        if self.helper.is_element_present("xpath", self.helper.get_xpath("ob_delete_all_confirm")):
            self.driver.find_element_by_xpath(self.helper.get_xpath("ob_delete_all_confirm_yes_btn")).click()

        self.helper.delete_workspace()

        #Switch back to the main window and refresh the page
        self.driver.switch_to_window(self.driver.window_handles[-1])
        what = "Trade"
        element = self.driver.find_element_by_link_text(what).click()
        
    #****** Test Cases *******
    #@unittest.skip("Skip for now")
    def test_MDT_enter_bid(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "MDT Enter Bid"
        return_msg = self.helper.open_new_workspace(workspace_name)

	logger.store_result('test_MDT_enter_bid','Call open new_workspace',datetime.today(),return_msg)

        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        print return_msg, "**** Enter bid ****" 
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
	
	logger.store_result('test_MDT_connection','Verify call to is_valid_connection',datetime.today(),return_msg)
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT and order book windows
        workspace_windows = ['mdt', 'order_book']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        #Set Qty to 1
        what = self.helper.get_xpath("mdt_qty1_btn")
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
        self.driver.find_element_by_xpath(what).click()

        #Find bid price with qty in MDT window and enter order
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_bid_has_value")).click()

        #Verify bid is resting in the market
        what = self.helper.get_xpath("mdt_working_order_bid")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        element = self.driver.find_element_by_xpath(what)
        self.assertIn('B:0', element.text, "B:0 not found")
        self.assertIn('W:1', element.text, "W:1 not found")

        #Get the price of the resting order
        element = self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_working_bid_price"))
        order_price = element.text

        #Get the name of the contract based on the title of the MDT window
        element = self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_title"))
        contract_name = (element.text).split(":")[0]
        
        #Verify values in order book
        return_msg = self.helper.validate_order(price=order_price, contract=contract_name)

	logger.store_result('test_MDT_enter_bid','Verify call to validate_order',datetime.today(),return_msg)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")
        
    @unittest.skip("Skip for now")
    def test_MDT_enter_bid_invalid_qty(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "MDT Enter Bid Invalid Qty"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT window
        workspace_windows = ['mdt']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        #Find bid price with qty in MDT window and attempt to enter order
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_bid_has_value")).click()

        #Verify message box appears for invalid order quantity
        what = self.helper.get_xpath("mdt_invalid_qty")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        element = self.driver.find_element_by_xpath(what)
        self.assertEqual(element.text, "Invalid order quantity: 0", "Invalid order quantity message not found")

        #Verify there is no bid price with a working qty (i.e. the order was never entered)
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.helper.get_xpath("mdt_working_bid_price"))))

        #Close message box and verify it is no longer visible
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_invalid_qty_close_btn")).click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.helper.get_xpath("mdt_invalid_qty"))))

    @unittest.skip("Skip for now")
    def test_MDT_open_new(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "Open New MDT"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")

        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Enter product in search field
        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("instrument_search"))))
        product = self.helper.get_product()
        element.send_keys(product)

        #Make sure the product entered in the search field matches each of the results returned
        what = self.helper.get_xpath("instrument_search_results")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        elements = self.driver.find_elements_by_xpath(what)
        for element in elements:
            self.assertIn(product, element.text, "Search string '" + product + "' not found in result '" + element.text + "'")

        #Click on the first search result and verify that MDT for that contract appears
        search_result_title = elements[0].text
        elements[0].click()
        what = self.helper.get_xpath("mdt_title")
        element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        self.assertIn(search_result_title, element.text, "Search result instrument (" + search_result_title + ") was not found in title of MDT (" + element.text + ")")

    @unittest.skip("Skip for now")
    def test_MDT_LTQ(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "LTQ"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")

        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Enter product in search field
        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("instrument_search"))))
        product = self.helper.get_product()
        element.send_keys(product)
        what = self.helper.get_xpath("instrument_search_results")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        elements = self.driver.find_elements_by_xpath(what)

        #Click on the second search result (market should not be as active) and verify that MDT for that contract appears
        search_result_title = elements[1].text
        elements[1].click()
        what = self.helper.get_xpath("mdt_title")
        element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        self.assertIn(search_result_title, element.text, "Search result instrument (" + search_result_title + ") was not found in title of MDT (" + element.text + ")")

        #TODO: LTQ does not update with our trades. If the simulation environment is changed to allow this then we can enters orders and verify that LTQ updates properly.
        #For now all we can do is validate that there is a LTQ value in MDT. 
        what = self.helper.get_xpath("mdt_LTQ")
        element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        current_ltq = element.text
        what = self.helper.get_xpath("mdt_LTQ_price")
        price = self.driver.find_element_by_xpath(what)

    @unittest.skip("Skip for now")
    def test_MDT_delete_buttons(self):
        workspace_name = "MDT Delete"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT window
        workspace_windows = ['mdt']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        #Verify all the delete buttons are disabled
        what = self.helper.get_xpath("mdt_del_sell_btn_disabled")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        what = self.helper.get_xpath("mdt_del_all_btn_disabled")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        what = self.helper.get_xpath("mdt_del_buy_btn_disabled")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))

        #Send bid
        self.helper.send_order()

        #Delete sell button is still disabled but delete buy and delete all are enabled
        what = self.helper.get_xpath("mdt_del_sell_btn_disabled")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        what = self.helper.get_xpath("mdt_del_all_btn_disabled")
        self.assertFalse(self.helper.is_element_present("xpath", what), "Delete all button should be enabled")
        what = self.helper.get_xpath("mdt_del_buy_btn_disabled")
        self.assertFalse(self.helper.is_element_present("xpath", what), "Delete buy button should be enabled")

        #Verify qty values on delete buy and delete all buttons 
        self.assertEqual(self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_buy_qty")).text, "1", "Qty on delete buy button is incorrect")
        self.assertEqual(self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_all_qty")).text, "1", "Qty on delete all button is incorrect")

        #Click del buy button
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_buy_btn")).click()
        
        #Verify there is no bid price with a working qty
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.helper.get_xpath("mdt_working_bid_price"))))

        #Send offer
        self.helper.send_order(is_buy=False)

        #Delete buy button is still disabled but delete sell and delete all are enabled
        what = self.helper.get_xpath("mdt_del_buy_btn_disabled")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        what = self.helper.get_xpath("mdt_del_all_btn_disabled")
        self.assertFalse(self.helper.is_element_present("xpath", what), "Delete all button should be enabled")
        what = self.helper.get_xpath("mdt_del_sell_btn_disabled")
        self.assertFalse(self.helper.is_element_present("xpath", what), "Delete sell button should be enabled")

        #Verify qty values on delete sell and delete all buttons 
        self.assertEqual(self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_sell_qty")).text, "1", "Qty on delete sell button is incorrect")
        self.assertEqual(self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_all_qty")).text, "1", "Qty on delete all button is incorrect")

        #Click del sell button
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_sell_btn")).click()
        
        #Verify there is no ask price with a working qty
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.helper.get_xpath("mdt_working_ask_price"))))

        #Send bid and offer
        self.helper.send_order()
        self.helper.send_order(is_buy=False)

        #All delete buttons should be enabled
        what = self.helper.get_xpath("mdt_del_buy_btn_disabled")
        self.assertFalse(self.helper.is_element_present("xpath", what), "Delete buy button should be enabled")
        what = self.helper.get_xpath("mdt_del_all_btn_disabled")
        self.assertFalse(self.helper.is_element_present("xpath", what), "Delete all button should be enabled")
        what = self.helper.get_xpath("mdt_del_sell_btn_disabled")
        self.assertFalse(self.helper.is_element_present("xpath", what), "Delete sell button should be enabled")

        #Verify qty values on delete sell, delete buy and delete all buttons
        self.assertEqual(self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_buy_qty")).text, "1", "Qty on delete buy button is incorrect")
        self.assertEqual(self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_sell_qty")).text, "1", "Qty on delete sell button is incorrect")
        self.assertEqual(self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_all_qty")).text, "2", "Qty on delete all button is incorrect")

        #Click del all button
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_del_all_btn")).click()

        #Verify there is no ask or bid price with a working qty
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.helper.get_xpath("mdt_working_ask_price"))))
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.helper.get_xpath("mdt_working_bid_price"))))

    @unittest.skip("Skip for now")
    def test_MDT_delete_orders_at_same_price(self):
        workspace_name = "MDT Delete Orders At Same Price"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT window
        workspace_windows = ['mdt']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        #Send two offers at the same price
        self.helper.send_order(is_buy=False)
        working_price = (self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_working_ask_price"))).text
        self.helper.send_order(is_buy=False, price=working_price, qty=5)

        #Expand MDT to display all the orders at the same price
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_working_show_orders")).click()

        #Get the list of orders and delete the "oldest" (i.e. the 1 lot)
        elements = self.driver.find_elements_by_xpath(self.helper.get_xpath("mdt_working_order_list"))
        elements[1].click()

        #Verify only the 2 lot is working
        what = self.helper.get_xpath("mdt_working_order_ask")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        element = self.driver.find_element_by_xpath(what)
        self.assertIn('W:2', element.text, "W:2 not found, actual value is " + element.text)

    #@unittest.skip("Skip for now")
    def test_MDT_enter_market_bid(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "MDT Enter Market Bid"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT, fills and order book windows
        workspace_windows = ['mdt', 'order_book', 'fills']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        #Set Qty to 1
        what = self.helper.get_xpath("mdt_qty1_btn")
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
        self.driver.find_element_by_xpath(what).click()

        #Select Market order
        what = self.helper.get_xpath("mdt_market_order")
        self.driver.find_element_by_xpath(what).click()

        #Find bid price with qty in MDT window and enter order
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_bid_has_value")).click()

        #Use the last row in the fills window
        what = self.helper.get_xpath("fills_window_fills")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        fills = self.driver.find_elements_by_xpath(what)
        num_fills = len(fills)

        what = self.helper.get_xpath("fills_window_contract")
        contract = fills[num_fills - 1].find_element_by_xpath(what).text
        what = self.helper.get_xpath("fills_window_status")
        status = fills[num_fills - 1].find_element_by_xpath(what).text
        what = self.helper.get_xpath("fills_window_buy_sell")
        buy_sell = fills[num_fills - 1].find_element_by_xpath(what).text
        what = self.helper.get_xpath("fills_window_qty")
        fill_qty = fills[num_fills - 1].find_element_by_xpath(what).text

        product = self.helper.get_product()
        self.assertIn(product, contract, "Contract for fill is incorrect, expected: " + product + ", actual: " + contract)
        self.assertEqual(status, "Filled", "Status is incorrect, expected: Filled, actual: " + status)
        self.assertEqual(buy_sell, "B", "Fill side is incorrect, expected: 'B', actual: '" + buy_sell + "'")
        self.assertEqual(fill_qty, "1", "Fill type is incorrect, expected: 1, actual: " + fill_qty)

        #Verify bid is filled and is not resting in the market
        what = self.helper.get_xpath("mdt_working_order_bid")
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, what)))

    @unittest.skip("Skip for now")
    def test_MDT_open_new_via_widget(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "Open New MDT Via Widget"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")

        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open a new MDT via the add new widget
        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("plus_icon"))))
        element.click()
        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath('add_new_MDT'))))
        element.click()
        what = self.helper.get_xpath("mdt_title")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_add_new_instrument"))))
        element.click()

        #Enter product in search field
        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_instrument_search"))))
        product = self.helper.get_product()
        element.send_keys(product)

        #Click on the first search result and verify that MDT for that contract appears
        what = self.helper.get_xpath("instrument_search_results")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        elements = self.driver.find_elements_by_xpath(what)
        search_result_title = elements[0].text
        elements[0].click()

        #Wait for the prices to display
        what = self.helper.get_xpath("mdt_bid_has_value")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))

    @unittest.skip("Skip for now")
    def test_MDT_GTC(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "MDT GTC"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT window
        workspace_windows = ['mdt', 'order_book']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        element = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_GTC_order"))))
        element.click()

        self.helper.send_order()

        #Get the name of the contract based on the title of the MDT window
        element = self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_title"))
        contract_name = (element.text).split(":")[0]

        #Verify values in order book
        return_msg = self.helper.validate_order(tif="GTC", contract=contract_name)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")

    @unittest.skip("Skip for now")
    def test_MDT_Position(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "MDT Position"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT window
        workspace_windows = ['mdt']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        #Store the current position
        element = self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_position"))

        #Need to handle the case where the position is "-". It will throw an error so catch it and set starting_position to 0
        
        starting_position = element.text
        #Check for flat position which is represented by '-' symbol
        if starting_position == u'\u2014':
            starting_position = 0

        #Set Qty to 10
        what = self.helper.get_xpath("mdt_qty10_btn")
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
        self.driver.find_element_by_xpath(what).click()

        #Select Market order
        what = self.helper.get_xpath("mdt_market_order")
        self.driver.find_element_by_xpath(what).click()

        #Find bid price with qty in MDT window and enter order
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_bid_has_value")).click()

        #Verify bid is filled and is not resting in the market
        what = self.helper.get_xpath("mdt_working_order_bid")
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, what)))

        #Check the position, it should be 10 longer than the previous position
        element = self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_position"))
        
        new_position = element.text
        #Check for flat position which is represented by '-' symbol
        if new_position == u'\u2014':
            new_position = 0
            
        expected_position = int(starting_position) + 10
        self.assertEqual(int(new_position), expected_position, "Position after market bid is incorrect, expected: " + str(expected_position) + " actual: " + str(new_position))

        #Set Qty to 5
        what = self.helper.get_xpath("mdt_qty5_btn")
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, what)))
        self.driver.find_element_by_xpath(what).click()

        #Select Market order
        what = self.helper.get_xpath("mdt_market_order")
        self.driver.find_element_by_xpath(what).click()

        #Find offer price with qty in MDT window and enter order
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_ask_has_value")).click()

        #Verify offer is filled and is not resting in the market
        what = self.helper.get_xpath("mdt_working_order_ask")
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, what)))

        #Check the position, it should be 5 shorter than the previous position
        element = self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_position"))
        new_position = element.text
        #Check for flat position which is represented by '-' symbol
        if new_position == u'\u2014':
            new_position = 0
        new_expected_position = int(expected_position) - 5
        self.assertEqual(int(new_position), new_expected_position, "Position after market bid is incorrect, expected: " + str(new_expected_position) + " actual: " + str(new_position))

    @unittest.skip("Skip for now")
    def test_MDT_qty_buttons(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "MDT Qty Button"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT and order book windows
        workspace_windows = ['mdt', 'order_book']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        #Get the name of the contract based on the title of the MDT window
        element = self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_title"))
        contract_name = (element.text).split(":")[0]

        #Set Qty to 1 (i.e. click 1 lot button once) and send order
        self.helper.send_order()

        #Verify values in order book
        return_msg = self.helper.validate_order(contract=contract_name)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")

        #Set Qty to 2 (i.e. click 1 lot button twice) and send order
        self.helper.send_order(qty=2)

        #Verify values in order book
        return_msg = self.helper.validate_order(contract=contract_name, qty=2)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")

        #Set Qty to 5 (i.e. click 5 lot button once) and send order
        self.helper.send_order(qty=5)

        #Verify values in order book
        return_msg = self.helper.validate_order(contract=contract_name, qty=5)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")

        #Set Qty to 10 (i.e. click 10 lot button once) and send order
        self.helper.send_order(qty=10)

        #Verify values in order book
        return_msg = self.helper.validate_order(contract=contract_name, qty=10)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")

        #Set Qty to 25 (i.e. click 25 lot button once) and send order
        self.helper.send_order(qty=25)

        #Verify values in order book
        return_msg = self.helper.validate_order(contract=contract_name, qty=25)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")

        #Set Qty to 50 (i.e. click 50 lot button once) and send order
        self.helper.send_order(qty=50)

        #Verify values in order book
        return_msg = self.helper.validate_order(contract=contract_name, qty=50)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")

        #Set Qty to 100 (i.e. click 100 lot button once) and send order
        self.helper.send_order(qty=100)

        #Verify values in order book
        return_msg = self.helper.validate_order(contract=contract_name, qty=100)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")

    @unittest.skip("Skip for now")
    def test_MDT_clear_reset(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("create_workspace_btn"))))

        workspace_name = "MDT Clear Reset"
        return_msg = self.helper.open_new_workspace(workspace_name)
        self.assertEqual(return_msg, "OK", "Call to open_new_workspace failed: '" + return_msg + "'")
        
        #Verify the name of the workspace window that pops up
        self.driver.switch_to_window(self.driver.window_handles[-1])
        window_name = self.driver.title
        self.assertEqual(window_name, workspace_name, "Workspace window does not match name of workspace")

        #Make sure the user has a valid connection
        return_msg = self.helper.is_valid_connection()
        self.assertEqual(return_msg, "Connected", "Call to is_valid_connection failed: '" + return_msg + "'")

        #Open MDT and order book windows
        workspace_windows = ['mdt', 'order_book']
        self.assertTrue(self.helper.populate_workspace(workspace_windows), "Call to populate_workspace failed")

        #Click confiuration drop down icon and then click Configure, update default qty to 2 and then save the default value
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_configuration_dropdown")))).click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_configure")))).click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_default_qty")))).send_keys("2")
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_configure_save")))).click()

        #Click 'C' button to clear qty
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_clear")))).click()

        #Find bid price with qty in MDT window and attempt to enter order
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_bid_has_value")).click()

        #Verify message box appears for invalid order quantity
        what = self.helper.get_xpath("mdt_invalid_qty")
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, what)))
        element = self.driver.find_element_by_xpath(what)
        self.assertEqual(element.text, "Invalid order quantity: 0", "Invalid order quantity message not found")

        #Verify there is no bid price with a working qty (i.e. the order was never entered)
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.helper.get_xpath("mdt_working_bid_price"))))

        #Close message box and verify it is no longer visible
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_invalid_qty_close_btn")).click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.helper.get_xpath("mdt_invalid_qty"))))

        #Set qty to 1 and the click reset button to set qty back to 2
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_qty1_btn")))).click()
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, self.helper.get_xpath("mdt_reset")))).click()

        #Find bid price with qty in MDT window and attempt to enter order
        self.driver.find_element_by_xpath(self.helper.get_xpath("mdt_bid_has_value")).click()

        #Verify values in order book
        return_msg = self.helper.validate_order(qty=2)
        self.assertEqual(return_msg, "OK", "Call to validate_order failed: '" + return_msg + "'")        

if __name__ == '__main__':
    unittest.main()
