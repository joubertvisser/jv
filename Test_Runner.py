from unittest import TestLoader, TestSuite
import HTMLTestRunner
import datetime
import os
from TC_Market_Depth_Trader import TestMarketDepthTrader
from TC_Workspace import TestWorkspace

class RegressionSuite():

    if __name__ == "__main__":

        #Create results folder if it doesn't exist already
        if not os.path.exists("results"):
            os.makedirs("results")
        file_name = datetime.datetime.now().strftime("results/%Y_%m_%d_%H%M_report.html")

        output = open(file_name, "wb")

        loader = TestLoader()
        suite = TestSuite((
                           loader.loadTestsFromTestCase(TestMarketDepthTrader),
                           loader.loadTestsFromTestCase(TestWorkspace)
                          ))
        runner = HTMLTestRunner.HTMLTestRunner(stream = output, verbosity = 1, title="Debesys Regression Suite")
        runner.run(suite)