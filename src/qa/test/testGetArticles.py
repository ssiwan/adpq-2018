import sys, unittest, QaAdpqShell

'''
    ADPQ v1 - Get Articles end point.
    
    Purpose - Will return a list of all articles.
    
    Method signature:
        get_articles(api_key='', apiKeyExclude=False):
    
    Required:
        api_key

    Test cases
        Successfully get all articles.
        
        ApiKey missing from request call.
        Null ApiKey value. 
        Int ApiKey value.     # commented out
        Float ApiKey value.   # commented out
        String ApiKey value.
        Array ApiKey value.   # commented out
'''
class TestGetArticles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            # Create user object.
            cls.user = QaAdpqShell.QaADPQShell()
            assert(cls.user != None)
            
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            raise

    
    
    # Test successfully getting a list of tags by hitting the end point.
    def test_success(self):
        # Hit the end point, should return a list of articles.
        responseBody = self.user.get_articles(api_key = self.user.GetApiKey())
        
        # If successful, list will not be empty.
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_Success assert#1 has failed.')
         
         
         
         
    # *********************************************************************
    # *                          ApiKey tests                             *
    # *********************************************************************
    
    
        
    # Missing ApiKey information from request call.
    def test_missingApiKey(self):
        # Missing ApiKey value.
        responseBody = self.user.get_articles(api_key = self.user.GetApiKey(),
                                              apiKeyExclude=True)
        
        self.assertEqual(responseBody['error'], False,
                          msg='test_missingApiKey assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Missing Authorization Key]',
#                           msg='test_missingApiKey assert#1 has failed.')
        
        
        
    # Test a null ApiKey.
    def test_nullApiKey(self):
        # Null ApiKey value.
        responseBody = self.user.get_articles(api_key = '')
        
        self.assertEqual(responseBody['error'], False,
                          msg='test_nullApiKey assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Missing Authorization Key]',
#                           msg='test_nullApiKey assert#1 has failed.')



    # Test a int ApiKey.
    def test_intApiKey(self):
        # Int ApiKey value.
        responseBody = self.user.get_articles(api_key = 8523154687)
        
        self.assertEqual(responseBody['error'], False,
                          msg='test_intApiKey assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Missing Authorization Key]',
#                           msg='test_nullApiKey assert#1 has failed.')



    # Test a float ApiKey.
    def test_floatApiKey(self):
        # Float ApiKey value.
        responseBody = self.user.get_articles(api_key = -852315.4687)
        
        self.assertEqual(responseBody['error'], False,
                          msg='test_floatApiKey assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Missing Authorization Key]',
#                           msg='test_floatApiKey assert#1 has failed.')
        
        
        
    # Test a string ApiKey value call.
    def test_stringApiKey(self):
        # String ApiKey value.
        responseBody = self.user.get_articles(api_key = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
        
        self.assertEqual(responseBody['error'], False,
                          msg='test_stringApiKey assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Incorrect Authorization Key]',
#                           msg='test_stringApiKey assert#1 has failed.')



    # Test an array ApiKey value call.
    def test_arrayApiKey(self):
        # Array ApiKey value.
        responseBody = self.user.get_articles(api_key = ['hodl', 666, [.6, 0], {}])
        
        self.assertEqual(responseBody['error'], False,
                          msg='test_arrayApiKey assert#1 failed.')
        
#         self.assertEqual(responseBody['err']['err'], 'Not authorized [Incorrect Authorization Key]',
#                           msg='test_arrayApiKey assert#1 has failed.')
        
        
        
        
        
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

    suite.addTest(TestGetArticles('test_missingApiKey'))
    suite.addTest(TestGetArticles('test_nullApiKey'))
#     suite.addTest(TestGetArticles('test_intApiKey'))
#     suite.addTest(TestGetArticles('test_floatApiKey'))
    suite.addTest(TestGetArticles('test_stringApiKey'))
#     suite.addTest(TestGetArticles('test_arrayApiKey'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())