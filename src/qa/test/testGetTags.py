import sys, unittest, requests, ADPQShell

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
            cls.user = ADPQShell.ADPQ()
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])

    
    
    # Make sure the end point is live.
    def test_liveEndPoint(self):
        url = ADPQShell.ADPQ.setEnv + ADPQShell.data['GetTags']
        
        headers = {
            'Content-Type' : 'application/json',
            'Cache-Control': 'no-cache'
        }
            
        response = requests.request('GET', url, json={}, 
                                    headers=headers, verify=False)
        
        self.assertEqual(response.status_code, 200, msg='test_liveEndPoint assert#1 has failed.')
        
        
        
    # Test successfully getting a list of tags by hitting the end point.
    def test_success(self):
        responseBody = self.user.get_tags()
        
        self.assertNotEqual(responseBody['data'], [], msg='test_Success assert#1 has failed.')
    
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGetTags('test_liveEndPoint'))
    suite.addTest(TestGetTags('test_success'))
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())