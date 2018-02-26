import sys, unittest, QaAdpqShell, requests

'''
    ADPQ v1 Get Agencies end point.
    
    Purpose - Will retrieve a list of CA agencies.
    
    Method signature:
        agencies():
    
    Required:
        <none>

    Test cases
        Ensure the end point is live.
        Successfully retrieve a list of all CA agencies.
'''
class TestGetAgencies(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            # Create shell class object.
            cls.user = QaAdpqShell.QaADPQShell()
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            raise

    
    
    # Make sure the end point is live.
    def test_liveEndPoint(self):
        # URL end point.
        url = QaAdpqShell.QaADPQShell.BaseURL + QaAdpqShell.QaADPQShell.GetAgencies

        # HTTP Action.
        HTTP_action = 'GET'
        
        # Header Parameters.
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
        
        # Dynamically set key/value body pairs. Add all body parameters.
        body = {}
            
        # Make HTTPS Request.
        response = requests.request(HTTP_action, url, json=body, 
                                    headers=headers, verify=False)
        
        # Ensure end point is live.
        self.assertEqual(response.status_code, 200, msg='test_liveEndPoint assert#1 has failed.')
        
        
    
    # Successfully get back a list of agencies.
    def test_success(self):
        
        # Attempt to get a list of all CA agencies. 
        responseBody = self.user.get_agencies()
           
        # If successful, list will not be empty.
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_Success assert#1 has failed.')
    
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGetAgencies('test_liveEndPoint'))
    suite.addTest(TestGetAgencies('test_success'))
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())