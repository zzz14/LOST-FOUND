from django.test import TestCase,Client
from selenium.webdriver.support.ui import WebDriverWait
from django.contrib.auth import models

# Create your tests here.
# 模拟一个简单的“哑”浏览器,
class adminPageWebVisitTests(TestCase):

    def setUp(self):
        super(adminPageWebVisitTests, self).setUp()

    # 测试登录登出网页的访问和返回状态是否正常
    def test_login_status(self):
        response_post = self.client.post('/a/login')
        self.assertEqual(response_post.status_code, 200)
        response_get = self.client.get('/a/login')
        self.assertEqual(response_get.status_code, 200)

    # 测试物品列表网页的访问
    def test_adminpage_list(self):
        response_post = self.client.post('/a/adminpage/list')
        self.assertEqual(response_post.status_code, 200)
        response_get = self.client.get('/a/adminpage/list')
        self.assertEqual(response_get.status_code, 200)
        #self.assertContains(response_get, "OK")

    # 测试新建发布网页的访问
    def test_adminpage_detail(self):
        response_post = self.client.post('/a/adminpage/detail?create=1')
        self.assertEqual(response_post.status_code, 200)
        response_get = self.client.get('/a/adminpage/detail?create=1')
        self.assertEqual(response_get.status_code, 200)


