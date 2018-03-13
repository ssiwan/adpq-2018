import sys, unittest, ADPQShell

'''
    ADPQ v1 - Get Article Details end point.
    
    Purpose - Will return a list of all articles according to user permission. 
              If a user passes in a particular article ID which exists, then
              the details returns will pretain to that article.
    
    Method signature:
        get_articles_details(Authorization='', AuthorizationExclude=False,
                             articleId=[], return_status=False):
    
    Optional:
        Authorization

    Test cases
        Successfully get all articles.
        
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
            print("Unexpected error during setUp:", sys.exc_info()[0])

    
    
    # Test successfully getting a list of tags by hitting the end point.
    def test_success(self):
        responseBody = self.user.get_articles_details(self.user.GetAuthKey())

        self.assertNotEqual(responseBody['data'], [], msg='test_Success assert#1 has failed.')
         
         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        responseBody = self.user.get_articles_details(Authorization = self.user.GetAuthKey(),
                                                      AuthorizationExclude=True)
        

        self.assertNotIn( 'Error', responseBody.keys(),
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        responseBody = self.user.get_articles_details(Authorization = '')
        

        self.assertNotIn('Error', responseBody.keys(), msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        responseBody = self.user.get_articles_details(Authorization = 8523154687)
        
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        responseBody = self.user.get_articles_details(Authorization = -852315.4687)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        responseBody = self.user.get_articles_details(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        responseBody = self.user.get_articles_details(Authorization = ['hodl', 666, [.6, 0], {}])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
        
        
        
        
    @classmethod
    def tearDownClass(cls):
        try:
            pass
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
    
    
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestGetArticlesDetails('test_success'))

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