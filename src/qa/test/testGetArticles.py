import sys, unittest, ADPQShell

'''
    ADPQ v1 - Get Articles end point.
    
    Purpose - Will return a list of all articles according to user permission.
    
    Method signature:
        get_articles(Authorization='', AuthorizationExclude=False, sortUrl=False,
                     limitUrl=False, dateStartURL=False, dateEndUrl=False,
                     agencyIdUrl=False, tagIdUrl=False, return_status=False,
                     return_status=False):
                     
    Notes: Url boolean in method signature indicates URL appending optional
           search parameters. Authorization key is optional.
    
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
class TestGetArticles(unittest.TestCase):

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
        responseBody = self.user.get_articles(Authorization = self.user.GetAuthKey(),
                                              sortUrl=True, limitUrl=True, tagIdUrl=True)

        self.assertNotEqual(responseBody['data'], [], msg='test_Success assert#1 has failed.')
         
         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        responseBody = self.user.get_articles(Authorization = self.user.GetAuthKey(),
                                              AuthorizationExclude=True)
        
        self.assertNotEqual(responseBody['data'], [], 
                            msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        responseBody = self.user.get_articles(Authorization = '')
        
        self.assertNotEqual(responseBody['data'], [], 
                            msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        responseBody = self.user.get_articles(Authorization = 8523154687)
        
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        responseBody = self.user.get_articles(Authorization = -852315.4687)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        responseBody = self.user.get_articles(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        responseBody = self.user.get_articles(Authorization = ['hodl', 666, [.6, 0], {}])
        
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
    
    suite.addTest(TestGetArticles('test_success'))

    suite.addTest(TestGetArticles('test_missingAuthorization'))
    suite.addTest(TestGetArticles('test_nullAuthorization'))
    suite.addTest(TestGetArticles('test_intAuthorization'))
    suite.addTest(TestGetArticles('test_floatAuthorization'))
    suite.addTest(TestGetArticles('test_stringAuthorization'))
    suite.addTest(TestGetArticles('test_arrayAuthorization'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())