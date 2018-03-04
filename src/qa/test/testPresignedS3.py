import sys, unittest, QaAdpqShell

'''
    ADPQ v1 - Get Presigned S3 end point.
    
    Purpose - 
    
    Method signature:
        get_presignedS3(Authorization='', name='', AuthorizationExclude=False, 
                        nameExclude=False, return_status=False):
    
    Required:
        Authorization
        name

    Test cases
        Successfully 
        
        Authorization missing from request call.
        Null Authorization value. 
        Int Authorization value.    
        Float Authorization value.   
        String Authorization value.
        Array Authorization value.  
        
        Name missing from request call.
        Null Name value. 
        Int Name value.    
        Float Name value.   
        String Name value.
        Array Name value.  
'''
class TestPresignedS3(unittest.TestCase):
    name = 'file.txt'
    
    @classmethod
    def setUpClass(cls):
        try:
            # Create user object.
            cls.user = QaAdpqShell.QaADPQShell()
            # SignIn the user. 
            cls.user.sign_in(email = QaAdpqShell.QaADPQShell.testEmail)
            assert(cls.user != None)
        except:
            print("Unexpected error during setUpClass:", sys.exc_info()[0])
            raise

    
    
    # Test successfully commenting on an existing article.
    def test_success(self):
        # Comment article.
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = TestPresignedS3.name)

        self.assertNotEqual(responseBody['url'], "",
                          msg='test_Success assert#1 has failed.')

         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        # Missing Authorization value.
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = TestPresignedS3.name,
                                                 AuthorizationExclude=True)
         
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        # Null Authorization value.
        responseBody = self.user.get_presignedS3(Authorization = '', 
                                                 name = TestPresignedS3.name)
        
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        # Int Authorization value.
        responseBody = self.user.get_presignedS3(Authorization = 963, 
                                                 name = TestPresignedS3.name)
        
        self.assertEqual(responseBody['data'], [],
                          msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        # Float Authorization value.
        responseBody = self.user.get_presignedS3(Authorization = -.369, 
                                                 name = TestPresignedS3.name)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        # String Authorization value.
        responseBody = self.user.get_presignedS3(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                 name = TestPresignedS3.name)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        # Array Authorization value.
        responseBody = self.user.get_presignedS3(Authorization = ['hodl', 666, [.6, 0], {}], 
                                                 name = TestPresignedS3.name)
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                          Name tests                               *
    # *********************************************************************
    
    
        
    # Missing Name information from request call.
    def test_missingName(self):
        # Missing Name value.
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = TestPresignedS3.name,
                                                 nameExclude=True)
       
        self.assertNotEqual(responseBody['fileKey'], "",
                          msg='test_missingName assert#1 has failed.')
        
        
        
    # Test a null Name.
    def test_nullName(self):
        # Null Name value.
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = '')
        
        self.assertNotEqual(responseBody['fileKey'], "",
                          msg='test_nullName assert#1 has failed.')



    # Test a int Name.
    def test_intName(self):
        # Int Name value.
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = 123456789)
        
        self.assertNotEqual(responseBody['fileKey'], "",
                          msg='test_intName assert#1 has failed.')



    # Test a float Name.
    def test_floatName(self):
        # Float Name value.
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = 123.456789)
        
        self.assertNotEqual(responseBody['fileKey'], "",
                          msg='test_floatName assert#1 failed.')
        
        
        
    # Test a string Name value call.
    def test_stringName(self):
        # String Name value.
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")

        self.assertNotEqual(responseBody['fileKey'], "",
                          msg='test_stringName assert#1 failed.')



    # Test an array Name value call.
    def test_arrayName(self):
        # Array Name value.
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = ['hodl', 666, [.6, 0], {}])

        self.assertNotEqual(responseBody['fileKey'], "",
                          msg='test_arrayName assert#1 failed.')
        
        
   
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
    
    suite.addTest(TestPresignedS3('test_success'))
   
    suite.addTest(TestPresignedS3('test_missingAuthorization'))
    suite.addTest(TestPresignedS3('test_nullAuthorization'))
    suite.addTest(TestPresignedS3('test_intAuthorization'))
    suite.addTest(TestPresignedS3('test_floatAuthorization'))
    suite.addTest(TestPresignedS3('test_stringAuthorization'))
    suite.addTest(TestPresignedS3('test_arrayAuthorization'))
  
    suite.addTest(TestPresignedS3('test_missingName'))
    suite.addTest(TestPresignedS3('test_nullName'))
    suite.addTest(TestPresignedS3('test_intName'))
    suite.addTest(TestPresignedS3('test_floatName'))
    suite.addTest(TestPresignedS3('test_stringName'))
    suite.addTest(TestPresignedS3('test_arrayName'))

    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())