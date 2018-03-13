import sys, unittest, ADPQShell
'''
    ADPQ v1 - Sign In end point.
    
    Purpose - Logs in/signs in an existing user. 
    
    Method signature:
        sign_in(self, email='', emailExclude=False, return_status=False):
    
    Required:
        email

    Test cases
        Successfully sign in an existing user.
        
        Email missing from request call.
        Null email value. 
        Int email value.
        Float email value.
        String email value.
        Array email value.
'''
class TestSignIn(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.user = ADPQShell.ADPQ()
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])

    
    
    # Test successfully signing in an existing user.
    def test_success(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'])
    
           
        self.assertEqual(responseBody['token'], self.user.GetAuthKey(),
                          msg='test_Success assert#1 has failed.')
          
        self.assertEqual(responseBody['role'], self.user.GetRole(),
                            msg='test_Success assert#2 has failed.')
           
        self.assertEqual(responseBody['id'], self.user.GetUserId(),
                          msg='test_Success assert#3 has failed.')

         
         
         
         
    # *********************************************************************
    # *                        Email tests                                *
    # *********************************************************************
    
    
    # Missing email information from request call.
    def test_missingEmail(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'], 
                                         emailExclude = True)
              
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_missingEmail assert#1 has failed.')
        
        
        
    # Test a null email.
    def test_nullEmail(self):
        responseBody = self.user.sign_in(email = '')
         
        self.assertEqual(responseBody['error'], 'User not found',
                         msg='test_nullEmail assert#1 has failed.')
        
        
        
    # Test an int email.
    def test_intEmail(self):
        responseBody = self.user.sign_in(email = 666)
         
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_intEmail assert#1 has failed.')
         
         
         
    # Test a float email.
    def test_floatEmail(self):
        responseBody = self.user.sign_in(email = -.123)
         
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_floatEmail assert#1 has failed.')
     
        
        
    
    # Test a string email value call.
    def test_stringEmail(self):
        responseBody = self.user.sign_in(email = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
            
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_stringEmail assert#1 has failed.') 
        
        
           
    # Test an array email value call.
    def test_arrayEmail(self):
        responseBody = self.user.sign_in(email = ['hodl', 666, [.6, 0], {}])
            
        self.assertEqual(responseBody['name'], 'CastError',
                          msg='test_arrayEmail assert#1 has failed.') 
        
        
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestSignIn('test_success'))
            
    suite.addTest(TestSignIn('test_missingEmail'))
    suite.addTest(TestSignIn('test_nullEmail'))
    suite.addTest(TestSignIn('test_intEmail'))
    suite.addTest(TestSignIn('test_floatEmail'))
    suite.addTest(TestSignIn('test_stringEmail'))
    suite.addTest(TestSignIn('test_arrayEmail'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())