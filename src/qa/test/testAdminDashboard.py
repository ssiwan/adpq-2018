import sys, unittest, ADPQShell

'''
    ADPQ v1 - Admin Dashboard Pending/Approved/Decline end point.
    
    Purpose - Will return a list of articles pertaining to the end point.
    
    Notes - Only role 2 users can access these end points.
    
    Method signature:
        admin_dashboard_decline(self, Authorization='', AuthorizationExclude=False, return_status=False): 
        admin_dashboard_approved(self, Authorization='', AuthorizationExclude=False, return_status=False): 
        admin_dashboard_pending(self, Authorization='', AuthorizationExclude=False, return_status=False):
    
    Required:
        Authorization

    Test cases
        Successfully get admins declined articles.
        Successfully get admins approved articles.
        Successfully get admins pending articles.
        
        Attempt to get admin page with users of type 0 & 1. WE ARE HERE FIGURE OUT ROLES
        
        Authorization missing from request call.
        Null Authorization value. 
        Int Authorization value.    
        Float Authorization value.   
        String Authorization value.
        Array Authorization value.  
'''
class TestAdminDashboard(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.role2 = ADPQShell.ADPQ()
            cls.role2.sign_in(email = ADPQShell.data['testEmail'])   # Role 2.
            
            cls.role1 = ADPQShell.ADPQ()
            cls.role1.sign_in(email = 'pmccartney@hotbsoftware.com') # Role 1.
            
            cls.role0 = ADPQShell.ADPQ()
            cls.role0.sign_in(email = 'jlennon@hotbsoftware.com')    # Role 0.
            
        except:
            print("Unexpected error during setUpClass:", sys.exc_info()[0])

    
    
    # Test successfully getting the admin dashboard declined articles.
    def test_successDeclined(self):
        status = self.role2.admin_dashboard_decline(self.role2.GetAuthKey(),
                                                         return_status=True)

        self.assertEqual(status.status_code, 200, msg='test_successDeclined assert#1 has failed.')
        
    
    
    # Test successfully getting the admin dashboard approved articles.
    def test_successApproved(self):
        status = self.role2.admin_dashboard_approved(self.role2.GetAuthKey(),
                                                         return_status=True)

        self.assertEqual(status.status_code, 200, msg='test_successApproved assert#1 has failed.')
        
        
        
    # Test successfully getting the admin dashboard pending articles.
    def test_successPending(self):
        status = self.role2.admin_dashboard_pending(self.role2.GetAuthKey(),
                                                         return_status=True)

        self.assertEqual(status.status_code, 200, msg='test_successPending assert#1 has failed.')
         
         
        
    # Test whether user of role 0 & 1 can access admin dashboards.
    def test_invalidUserRole(self):
        responseBody = self.role1.admin_dashboard_pending(self.role1.GetAuthKey())

        self.assertEqual(responseBody['error'], 'User not permitted', 
                         msg='test_invalidUserRole assert#1 has failed.')
        
        responseBody = self.role0.admin_dashboard_pending(self.role0.GetAuthKey())

        self.assertEqual(responseBody['error'], 'User not permitted', 
                         msg='test_invalidUserRole assert#1 has failed.') 
        
        
        
    # *********************************************************************
    # *                       Authorization tests                         *
    # *********************************************************************
    
    
        
    # Missing Authorization information from request call.
    def test_missingAuthorization(self):
        # Missing Authorization value.
        responseBody = self.role2.admin_dashboard_decline(self.role2.GetAuthKey(),
                                                     AuthorizationExclude=True)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#1 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_approved(self.role2.GetAuthKey(),
                                                     AuthorizationExclude=True)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#2 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_pending(self.role2.GetAuthKey(),
                                                     AuthorizationExclude=True)
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_missingAuthorization assert#3 has failed.')
        
        
        
    # Test a null Authorization.
    def test_nullAuthorization(self):
        # Null Authorization value.
        responseBody = self.role2.admin_dashboard_decline(Authorization='')

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#1 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_approved(Authorization='')

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#2 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_pending(Authorization='')
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_nullAuthorization assert#3 has failed.')



    # Test a int Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_intAuthorization(self):
        # Int Authorization value.
        responseBody = self.role2.admin_dashboard_decline(Authorization=1)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_intAuthorization assert#1 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_approved(Authorization=2)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_intAuthorization assert#2 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_pending(Authorization=3)
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_intAuthorization assert#3 has failed.')



    # Test a float Authorization.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_floatAuthorization(self):
        # Float Authorization value.
        responseBody = self.role2.admin_dashboard_decline(Authorization=.78)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_floatAuthorization assert#1 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_approved(Authorization=7.8)

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_floatAuthorization assert#2 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_pending(Authorization=.8787)
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_floatAuthorization assert#3 has failed.')
        
        
        
    # Test a string Authorization value call.
    def test_stringAuthorization(self):
        # String Authorization value.
        responseBody = self.role2.admin_dashboard_decline(Authorization="';:.>,</?]}[{!@#$%^&*()-_=+|\"")

        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#1 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_approved(Authorization="';:.>,</?]}[{!@#$%^&*()-_=+|\"")

        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#2 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_pending(Authorization="';:.>,</?]}[{!@#$%^&*()-_=+|\"")
  
        self.assertEqual(responseBody['error'], 'Failed to authenticate token',
                          msg='test_stringAuthorization assert#3 has failed.')



    # Test an array Authorization value call.
    @unittest.skip("requests.exceptions - must be of type str or bytes")
    def test_arrayAuthorization(self):
        # Array Authorization value.
        responseBody = self.role2.admin_dashboard_decline(Authorization=['hodl', 666, [.6, 0], {}])

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_arrayAuthorization assert#1 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_approved(Authorization=['hodl', 666, [.6, 0], {}])

        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_arrayAuthorization assert#2 has failed.')
        
        
        responseBody = self.role2.admin_dashboard_pending(Authorization=['hodl', 666, [.6, 0], {}])
  
        self.assertEqual(responseBody['error'], 'Please provide an authentication token',
                          msg='test_arrayAuthorization assert#3 has failed.')
        
        
        
        
        
    @classmethod
    def tearDownClass(cls):
        try:
            pass
        except:
            print("Unexpected error during tearDownClass:", sys.exc_info()[0])
    
    
    
def suite():
    suite = unittest.TestSuite()
    
    suite.addTest(TestAdminDashboard('test_successDeclined'))
    suite.addTest(TestAdminDashboard('test_successApproved'))
    suite.addTest(TestAdminDashboard('test_successPending'))
     
    suite.addTest(TestAdminDashboard('test_invalidUserRole'))

    suite.addTest(TestAdminDashboard('test_missingAuthorization'))
    suite.addTest(TestAdminDashboard('test_nullAuthorization'))
    suite.addTest(TestAdminDashboard('test_intAuthorization'))
    suite.addTest(TestAdminDashboard('test_floatAuthorization'))
    suite.addTest(TestAdminDashboard('test_stringAuthorization'))
    suite.addTest(TestAdminDashboard('test_arrayAuthorization'))
    
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())