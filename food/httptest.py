import unittest
import requests as req
from requests.auth import HTTPBasicAuth

class foo(unittest.TestCase):
    hostname = "http://localhost:8000/"
    passwd = 'asdfghjkl'

    def setUp(self):
        pass

    def test_login(self):
        x=req.get(self.hostname+"admin/login/",{'username':'ak', 'password':self.passwd})
 #       print('----------------')
        csrf = x.cookies['csrftoken']
 #       print(dir(x.content))
        print('--------------')
#        print(csrf)
        x=req.post(self.hostname+"admin/login/",{'username':'ak', 'password':self.passwd,'csrfmiddlewaretoken':csrf},
                auth= HTTPBasicAuth('ak',self.passwd))
        print(x)

    def xtest_userlogin_plain_http(self):
        x = req.get(self.hostname+"api/order/",)
        print(x.content)


if __name__=="__main__":
    unittest.main()
