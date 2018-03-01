import sys, unittest, QaAdpqShell

'''
    ADPQ v1 - Get Articles end point.
    
    Purpose - Will return a list of all articles according to user permission.
    
    Method signature:
        get_articles(Authorization='', AuthorizationExclude=False, sortUrl=False,
                     limitUrl=False, dateStartURL=False, dateEndUrl=False,
                     agencyIdUrl=False, tagIdUrl=False):
                     
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
            # Create user object.
            cls.user = QaAdpqShell.QaADPQShell()
            
            # SignIn the user. 
            cls.user.sign_in(email = QaAdpqShell.QaADPQShell.testEmail)
            
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            raise

    
    
    # Test successfully getting a list of tags by hitting the end point.
    def test_success(self):
        # Hit the end point, should return a list of articles.
        responseBody = self.user.get_articles(Authorization = self.user.GetAuthKey(),
                                              sortUrl=True, limitUrl=True, tagIdUrl=True)

        # If successful, list will not be empty.
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_Success assert#1 has failed.')
         
         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        # Missing Authorization value.
        responseBody = self.user.get_articles(Authorization = self.user.GetAuthKey(),
                                              AuthorizationExclude=True)
        
        # Currently passing. 
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_missingAuthorization assert#1 has failed.')
        
#         self.assertEqual(responseBody['error'], 'Failed to authenticate token',
#                           msg='test_missingAuthorization assert#2 failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        # Null Authorization value.
        responseBody = self.user.get_articles(Authorization = '')
        
        # Currently passing. 
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_nullAuthorization assert#1 has failed.')
        
#         self.assertEqual(responseBody['error'], 'Failed to authenticate token',
#                           msg='test_nullAuthorization assert#2 failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        # Int Authorization value.
        responseBody = self.user.get_articles(Authorization = 8523154687)
        
        # Currently passing. 
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_intAuthorization assert#1 has failed.')
        
#         self.assertEqual(responseBody['error'], 'Failed to authenticate token',
#                           msg='test_intAuthorization assert#2 failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        # Float Authorization value.
        responseBody = self.user.get_articles(Authorization = -852315.4687)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Missing Authorization Key]',
#                           msg='test_floatAuthorization assert#1 has failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        # String Authorization value.
        responseBody = self.user.get_articles(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Incorrect Authorization Key]',
#                           msg='test_stringAuthorization assert#1 has failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        # Array Authorization value.
        responseBody = self.user.get_articles(Authorization = ['hodl', 666, [.6, 0], {}])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Incorrect Authorization Key]',
#                           msg='test_arrayAuthorization assert#1 has failed.')
        
        
        
        
        
    @classmethod
    def tearDownClass(cls):
        try:
            pass
#             cls.user.remove_user(cls.user.testEmail)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            #raise
        #cls.user.remove_user(cls.user.testEmail)
    
    
    
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