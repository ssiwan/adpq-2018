import sys, unittest, ADPQShell

'''
    ADPQ v1 - Dashboard analytics, trending, published articles, & workflow end point.
    
    Purpose - Will return a list of articles pertaining to the end point.
    
    Method signature:
        dashboard_analytics(self, Authorization='', AuthorizationExclude=False, return_status=False): 
        dashboard_trending(self, Authorization='', AuthorizationExclude=False, return_status=False): 
        dashboard_pubArticles(self, Authorization='', AuthorizationExclude=False, return_status=False):
        dashboard_workflow(self, Authorization='', AuthorizationExclude=False, return_status=False):
    
    Required:
        Authorization

    Test cases
        Successfully get users dashboard analytics.
        Successfully get the users dashboard trending articles.
        Successfully get users published articles.
        Successfully get users dashboard workflow.
        
        Authorization missing from request call.
        Null Authorization value. 
        Int Authorization value.    
        Float Authorization value.   
        String Authorization value.
        Array Authorization value.  
'''
class TestGetArticlesDetails(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.user = ADPQShell.ADPQ()
            cls.user.sign_in(email = ADPQShell.data['testEmail'])
            assert(cls.user != None)
        except:
            print("Unexpected error during setUpClass:", sys.exc_info()[0])

    
    
    # Test successfully getting the users dashboard analytics.
    def test_successAnalytics(self):
        status = self.user.dashboard_analytics(self.user.GetAuthKey(), return_status=True)

        self.assertEqual(status.status_code, 200, msg='test_successAnalytics assert#1 failed.')
        
    
    
    # Test successfully getting the users dashboard trending articles.
    def test_successTrendings(self):
        status = self.user.dashboard_trending(self.user.GetAuthKey(), return_status=True)

        self.assertEqual(status.status_code, 200, msg='test_successTrendings assert#1 failed.')
        
        
        
    # Test successfully getting the users published articles.
    def test_successPublishedArticles(self):
        status = self.user.dashboard_pubArticles(self.user.GetAuthKey(), return_status=True)

        self.assertEqual(status.status_code, 200, msg='test_successPublishedArticles assert#1 failed.')
        
        
        
    # Test successfully getting the users dashboard workflow.
    def test_successWorkflow(self):
        status = self.user.dashboard_workflow(self.user.GetAuthKey(), return_status=True)

        self.assertEqual(status.status_code, 200, msg='test_successWorkflow assert#1 failed.')
         
         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        # Missing Authorization value.
        responseBody = self.user.dashboard_analytics(self.user.GetAuthKey(),
                                                     AuthorizationExclude=True)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        responseBody = self.user.dashboard_trending(self.user.GetAuthKey(),
                                                     AuthorizationExclude=True)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#2 has failed.')
        
        
        responseBody = self.user.dashboard_pubArticles(self.user.GetAuthKey(),
                                                     AuthorizationExclude=True)
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#3 has failed.')
        
        
        responseBody = self.user.dashboard_workflow(self.user.GetAuthKey(),
                                                     AuthorizationExclude=True)
        

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#4 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        # Null Authorization value.
        responseBody = self.user.dashboard_analytics(Authorization='')

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#1 has failed.')
        
        
        responseBody = self.user.dashboard_trending(Authorization='')

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#2 has failed.')
        
        
        responseBody = self.user.dashboard_pubArticles(Authorization='')
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#3 has failed.')
        
        
        responseBody = self.user.dashboard_workflow(Authorization='')
        

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#4 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        # Int Authorization value.
        responseBody = self.user.dashboard_analytics(Authorization=1)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_intAuthorization assert#1 has failed.')
        
        
        responseBody = self.user.dashboard_trending(Authorization=2)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_intAuthorization assert#2 has failed.')
        
        
        responseBody = self.user.dashboard_pubArticles(Authorization=3)
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_intAuthorization assert#3 has failed.')
        
        
        responseBody = self.user.dashboard_workflow(Authorization=4)
        

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_intAuthorization assert#4 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        # Float Authorization value.
        responseBody = self.user.dashboard_analytics(Authorization=.78)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_floatAuthorization assert#1 has failed.')
        
        
        responseBody = self.user.dashboard_trending(Authorization=7.8)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_floatAuthorization assert#2 has failed.')
        
        
        responseBody = self.user.dashboard_pubArticles(Authorization=.8787)
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_floatAuthorization assert#3 has failed.')
        
        
        responseBody = self.user.dashboard_workflow(Authorization=7878.78)
        

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_floatAuthorization assert#4 has failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        # String Authorization value.
        responseBody = self.user.dashboard_analytics(Authorization="';:.>,</?]}[{!@#$%^&*()-_=+|\"")

        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 has failed.')
        
        
        responseBody = self.user.dashboard_trending(Authorization="';:.>,</?]}[{!@#$%^&*()-_=+|\"")

        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#2 has failed.')
        
        
        responseBody = self.user.dashboard_pubArticles(Authorization="';:.>,</?]}[{!@#$%^&*()-_=+|\"")
  
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#3 has failed.')
        
        
        responseBody = self.user.dashboard_workflow(Authorization="';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        

        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#4 has failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        # Array Authorization value.
        responseBody = self.user.dashboard_analytics(Authorization=['hodl', 666, [.6, 0], {}])

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_arrayAuthorization assert#1 has failed.')
        
        
        responseBody = self.user.dashboard_trending(Authorization=['hodl', 666, [.6, 0], {}])

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_arrayAuthorization assert#2 has failed.')
        
        
        responseBody = self.user.dashboard_pubArticles(Authorization=['hodl', 666, [.6, 0], {}])
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_arrayAuthorization assert#3 has failed.')
        
        
        responseBody = self.user.dashboard_workflow(Authorization=['hodl', 666, [.6, 0], {}])
        

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_arrayAuthorization assert#4 has failed.')
        
        
        
        
        
    @classmethod
    def tearDownClass(cls):
        try:
            pass
        except:
            print("Unexpected error during tearDownClass:", sys.exc_info()[0])
    
    
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestGetArticlesDetails('test_successAnalytics'))
    suite.addTest(TestGetArticlesDetails('test_successTrendings'))
    suite.addTest(TestGetArticlesDetails('test_successPublishedArticles'))
    suite.addTest(TestGetArticlesDetails('test_successWorkflow'))

    suite.addTest(TestGetArticlesDetails('test_missingAuthorization'))
    suite.addTest(TestGetArticlesDetails('test_nullAuthorization'))
    suite.addTest(TestGetArticlesDetails('test_intAuthorization'))
    suite.addTest(TestGetArticlesDetails('test_floatAuthorization'))
    suite.addTest(TestGetArticlesDetails('test_stringAuthorization'))
    suite.addTest(TestGetArticlesDetails('test_arrayAuthorization'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())