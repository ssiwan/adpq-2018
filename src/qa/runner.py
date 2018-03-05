'''
Created on Feb 14, 2018

@author: Luis.Escobar-Driver
'''

import unittest, xmlrunner

# Import test modules   
from test import smokeTest
from test import testGetAgencies
from test import testGetTags
from test import testGetArticles
from test import testSearchArticles
from test import testSignIn
from test import testGetArticleDetails
from test import testCreateArticle
from test import testDashboard
from test import testEditArticle
from test import testCommentArticle
from test import testPresignedS3

# Initialize a test loader & test suite package.
loader = unittest.TestLoader()
suite  = unittest.TestSuite()
 
# Add test suites to the runners suite package.
suite.addTests(loader.suiteClass(smokeTest.suite()))
suite.addTests(loader.suiteClass(testGetAgencies.suite()))
suite.addTests(loader.suiteClass(testGetTags.suite()))
suite.addTests(loader.suiteClass(testGetArticles.suite()))
suite.addTests(loader.suiteClass(testSearchArticles.suite()))
suite.addTests(loader.suiteClass(testSignIn.suite()))
suite.addTests(loader.suiteClass(testGetArticleDetails.suite()))
suite.addTests(loader.suiteClass(testCreateArticle.suite()))
suite.addTests(loader.suiteClass(testDashboard.suite()))
suite.addTests(loader.suiteClass(testEditArticle.suite()))
suite.addTests(loader.suiteClass(testCommentArticle.suite()))
suite.addTests(loader.suiteClass(testPresignedS3.suite()))

# Initialize an xml runner.
testRunner=xmlrunner.XMLTestRunner(output='data/testReports', verbosity=2)
 
# Run the suite & save the results.
results = testRunner.run(suite)
  
print(results)