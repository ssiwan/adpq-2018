import sys, unittest, ADPQShell
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
            cls.user = ADPQShell.ADPQ()
            assert(cls.user != None)
        except:
            print("Unexpected error during setUp:", sys.exc_info()[0])

    
    
    # Make sure the end point is live.
    def test_liveEndPoint(self):
        status = self.user.get_agencies(return_status=True)
        
        self.assertEqual(status.status_code, 200, msg='test_Success assert#1 has failed.')
        
        
    
    # Successfully get back a list of agencies.
    def test_successData(self):
        responseBody = self.user.get_agencies()
           
        self.assertNotEqual(responseBody['data'], [], msg='test_Success assert#1 has failed.')
    
    
    
def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestGetAgencies('test_liveEndPoint'))
    suite.addTest(TestGetAgencies('test_successData'))
    return suite
    
    
    
if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())