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
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'],
                                         password = ADPQShell.data['testPassword'])
    
           
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
    @unittest.skip("Checked on the front end.")
    def test_missingEmail(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'], 
                                         password = ADPQShell.data['testPassword'],
                                         emailExclude = True)
              
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_missingEmail assert#1 has failed.')
        
        
        
    # Test a null email.
    @unittest.skip("Checked on the front end.")
    def test_nullEmail(self):
        responseBody = self.user.sign_in(email = '', password = ADPQShell.data['testPassword'])
         
        self.assertEqual(responseBody['error'], 'User not found',
                         msg='test_nullEmail assert#1 has failed.')
        
        
        
    # Test an int email.
    @unittest.skip("Checked on the front end.")
    def test_intEmail(self):
        responseBody = self.user.sign_in(email = 666, password = ADPQShell.data['testPassword'])
         
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_intEmail assert#1 has failed.')
         
         
         
    # Test a float email.
    @unittest.skip("Checked on the front end.")
    def test_floatEmail(self):
        responseBody = self.user.sign_in(email = -.123)
         
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_floatEmail assert#1 has failed.')
     
        
        
    
    # Test a string email value call.
    @unittest.skip("Checked on the front end.")
    def test_stringEmail(self):
        responseBody = self.user.sign_in(email = "';:.>,</?]}[{!@#$%^&*()-_=+|\"",
                                         password = ADPQShell.data['testPassword'])
            
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_stringEmail assert#1 has failed.') 
        
        
           
    # Test an array email value call.
    @unittest.skip("Checked on the front end.")
    def test_arrayEmail(self):
        responseBody = self.user.sign_in(email = ['hodl', 666, [.6, 0], {}],
                                         password = ADPQShell.data['testPassword'])
            
        self.assertEqual(responseBody['name'], 'CastError',
                          msg='test_arrayEmail assert#1 has failed.') 
        
        
        
    # *********************************************************************
    # *                        Password tests                             *
    # *********************************************************************
    
    
    # Missing Password information from request call.
    @unittest.skip("Checked on the front end.")
    def test_missingPassword(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'], 
                                         password = ADPQShell.data['testPassword'],
                                         passwordExclude = True)
              
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_missingPassword assert#1 has failed.')
        
        
        
    # Test a null Password.
    @unittest.skip("Checked on the front end.")
    def test_nullPassword(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'], 
                                         password = '')
         
        self.assertEqual(responseBody['error'], 'User not found',
                         msg='test_nullPassword assert#1 has failed.')
        
        
        
    # Test an int Password.
    @unittest.skip("Checked on the front end.")
    def test_intPassword(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'], 
                                         password = 66)
         
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_intPassword assert#1 has failed.')
         
         
         
    # Test a float Password.
    @unittest.skip("Checked on the front end.")
    def test_floatPassword(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'],
                                         password = -.1235)
         
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_floatPassword assert#1 has failed.')
     
        
        
    
    # Test a string Password value call.
    @unittest.skip("Checked on the front end.")
    def test_stringPassword(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'],
                                         password = "';:.>,</?]}[{!@#$%^&*()-_=+|\"")
            
        self.assertEqual(responseBody['error'], 'User not found',
                          msg='test_stringPassword assert#1 has failed.') 
        
        
           
    # Test an array Password value call.
    @unittest.skip("Checked on the front end.")
    def test_arrayPassword(self):
        responseBody = self.user.sign_in(email = ADPQShell.data['testEmail'],
                                         password = ['hodl', 666, [.6, 0], {}])
            
        self.assertEqual(responseBody['name'], 'CastError',
                          msg='test_arrayPassword assert#1 has failed.') 
        
        
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestSignIn('test_success'))
            
    suite.addTest(TestSignIn('test_missingEmail'))
    suite.addTest(TestSignIn('test_nullEmail'))
    suite.addTest(TestSignIn('test_intEmail'))
    suite.addTest(TestSignIn('test_floatEmail'))
    suite.addTest(TestSignIn('test_stringEmail'))
    suite.addTest(TestSignIn('test_arrayEmail'))
    
    suite.addTest(TestSignIn('test_missingPassword'))
    suite.addTest(TestSignIn('test_nullPassword'))
    suite.addTest(TestSignIn('test_intPassword'))
    suite.addTest(TestSignIn('test_floatPassword'))
    suite.addTest(TestSignIn('test_stringPassword'))
    suite.addTest(TestSignIn('test_arrayPassword'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())