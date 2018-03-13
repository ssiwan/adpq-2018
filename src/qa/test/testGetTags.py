import sys, unittest, ADPQShell

'''
    ADPQ v1 Get Tags end point.
    
    Purpose - Will get a list of all tags.
    
    Method signature:
        get_tags():
    
    Required:
        <none>

    Test cases
        Test end point status.
        Successfully get all tags.
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
        status = self.user.get_tags(return_status=True)
        self.assertEqual(status.status_code, 200, msg='test_liveEndPoint assert#1 failed.')
        
        
        
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