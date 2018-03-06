import sys, unittest, ADPQShell
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
            cls.user = ADPQShell.ADPQ()
            cls.user.sign_in(email = ADPQShell.data['testEmail'])
            assert(cls.user != None)
        except:
            print("Unexpected error during setUpClass:", sys.exc_info()[0])

    
    
    # Test successfully commenting on an existing article.
    def test_success(self):
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = ADPQShell.data['testName'])

        self.assertNotEqual(responseBody['url'], "", msg='test_Success assert#1 has failed.')

         
         
         
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = ADPQShell.data['testName'],
                                                 AuthorizationExclude=True)
         
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        responseBody = self.user.get_presignedS3(Authorization = '', 
                                                 name = ADPQShell.data['testName'])
        
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#1 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        responseBody = self.user.get_presignedS3(Authorization = 963, 
                                                 name = ADPQShell.data['testName'])
        
        self.assertEqual(responseBody['data'], [],
                          msg='test_intAuthorization assert#1 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        responseBody = self.user.get_presignedS3(Authorization = -.369, 
                                                 name = ADPQShell.data['testName'])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_floatAuthorization assert#1 failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        responseBody = self.user.get_presignedS3(Authorization = "';:.>,</?]}[{!@#$%^&*()-_=+|\"", 
                                                 name = ADPQShell.data['testName'])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        responseBody = self.user.get_presignedS3(Authorization = ['hodl', 666, [.6, 0], {}], 
                                                 name = ADPQShell.data['testName'])
        
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_arrayAuthorization assert#1 failed.')
        
        
        
    # *********************************************************************
    # *                          Name tests                               *
    # *********************************************************************
    
    
        
    # Missing Name information from request call.
    def test_missingName(self):
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = ADPQShell.data['testName'],
                                                 nameExclude=True)
       
        self.assertNotEqual(responseBody['fileKey'], "", msg='test_missingName assert#1 has failed.')
        
        
        
    # Test a null Name.
    def test_nullName(self):
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = '')
        
        self.assertNotEqual(responseBody['fileKey'], "", msg='test_nullName assert#1 has failed.')



    # Test a int Name.
    def test_intName(self):
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = 123456789)
        
        self.assertNotEqual(responseBody['fileKey'], "", msg='test_intName assert#1 has failed.')



    # Test a float Name.
    def test_floatName(self):
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = 123.456789)
        
        self.assertNotEqual(responseBody['fileKey'], "", msg='test_floatName assert#1 failed.')
        
        
        
    # Test a string Name value call.
    def test_stringName(self):
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")

        self.assertNotEqual(responseBody['fileKey'], "", msg='test_stringName assert#1 failed.')



    # Test an array Name value call.
    def test_arrayName(self):
        responseBody = self.user.get_presignedS3(Authorization = self. user.GetAuthKey(), 
                                                 name = ['hodl', 666, [.6, 0], {}])

        self.assertNotEqual(responseBody['fileKey'], "", msg='test_arrayName assert#1 failed.')
        
        
   
    @classmethod
    def tearDownClass(cls):
        try:
            pass
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
    
    
    
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