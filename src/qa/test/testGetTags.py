import sys, unittest, QaAdpqShell, requests

'''
    ADPQ v1 Get Tags end point.
    
    Purpose - Will get a list of all tags.
    
    Method signature:
        get_tags():
    
    Required:
        <none>

    Test cases
        Successfully get all tags.
        
        ApiKey missing from request call.
        Null ApiKey value. 
        Int ApiKey value.     # commented out
        Float ApiKey value.   # commented out
        String ApiKey value.
        Array ApiKey value.   # commented out
'''
class TestGetTags(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            # Create user object.
            cls.user = QaAdpqShell.QaADPQShell()
            assert(cls.user != None)
            
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])
            raise

    
    
    # Make sure the end point is live.
    def test_liveEndPoint(self):
        # URL end point.
        url = QaAdpqShell.QaADPQShell.setEnv + QaAdpqShell.QaADPQShell.GetTags

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
        
        
        
    # Test successfully getting a list of tags by hitting the end point.
    def test_success(self):
        # Hit the end point, should return a list of tags.
        responseBody = self.user.get_tags()
        
        # If successful, list will not be empty.
        self.assertNotEqual(responseBody['data'], [],
                          msg='test_Success assert#1 has failed.')
    
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGetTags('test_liveEndPoint'))
    suite.addTest(TestGetTags('test_success'))
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())