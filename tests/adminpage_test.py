# coding=utf-8
from django.test import LiveServerTestCase
from wechat.models import User, AdminLost
from django.contrib.auth.models import User
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

class LoginLogoutTest(LiveServerTestCase):
    browser = None

    # 对比url是否一致
    def assertUrl(self, url):
        self.assertEqual(self.browser.current_url, self.live_server_url + url)

    @classmethod
    def setUpClass(self):
        super(LoginLogoutTest, self).setUpClass()
        self.browser = webdriver.PhantomJS()
        self.wait = WebDriverWait(self.browser, 6)
        self.browser.set_window_size(1920, 1080)
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    @classmethod
    def tearDownClass(self):
        self.browser.quit()
        super(LoginLogoutTest, self).tearDownClass()

    @classmethod
    def fillTheBox(self, selector, value):
        name_box = self.browser.find_element_by_css_selector(selector)
        name_box.clear()
        sleep(0.6)
        name_box.send_keys(value)
        sleep(0.2)

    # 用户登录函数
    def login(self, username='john', password='johnpassword'):
        self.browser.get(self.live_server_url + '/a/login')
        self.wait = WebDriverWait(self.browser, 5)
        self.wait.until(EC.presence_of_element_located((By.ID, 'inputUsername')))
        self.fillTheBox('#inputUsername', username)
        self.fillTheBox('#inputPassword', password)
        submit_button = self.browser.find_element_by_css_selector('#loginnow')
        submit_button.click()
        sleep(0.1)

    '''
    # 非注册用户
    def test_guest_tour(self):
        self.browser.get(self.live_server_url + '/a')
        self.wait.until(EC.title_contains('失物招领'))
        self.assertUrl('/a/login?next=%2Fa')
        self.login('john233', 'johnpassword')
        alert = self.browser.find_element_by_id('alert')
        self.wait.until(EC.visibility_of((alert)))
        self.assertIn('login error', alert.text)
        self.browser.get(self.live_server_url + '/a/adminpage/list')
        self.wait.until(EC.title_contains('登录'))
        self.assertUrl('/a/login?next=%2Fa%2Fadminpage%2Flist')


    # 密码正确
    def test_admin_login_with_right_pass(self):
        self.login('john', 'johnpassword')
        sleep(3)
        self.browser.get_screenshot_as_file('tests/pic/11_login.png')
        self.assertUrl('/a/adminpage/list')
        self.browser.get(self.live_server_url + '/a/adminpage/list')
        self.browser.get_screenshot_as_file('tests/pic/12_list.png')

    # 密码错误
    def test_admin_login_with_wrong_pass(self):
        self.login('john', 'johnpassword233')
        self.browser.get_screenshot_as_file('tests/pic/21_login.png')
        alert = self.browser.find_element_by_id('alert')
        self.wait.until(EC.visibility_of((alert)))
        self.assertIn('login error', alert.text)
        self.browser.get(self.live_server_url + '/a/adminpage/list')
        self.browser.get_screenshot_as_file('tests/pic/22_list.png')
        self.wait.until(EC.title_contains('登录'))
        self.assertUrl('/a/login?next=%2Fa%2Fadminpage%2Flist')
    '''

    # 注销
    def test_logout(self):
        self.login('john', 'johnpassword')
        sleep(4)
        self.browser.get(self.live_server_url + '/a/adminpage/list')
        self.browser.get_screenshot_as_file('tests/pic/31_login.png')
        self.wait.until(EC.presence_of_element_located((By.ID, 'my-upload-list')))
        submit_button1 = self.browser.find_element_by_id('logout-button')
        submit_button1.click()
        sleep(1)
        self.wait.until(EC.title_contains('登录'))
        self.assertUrl('/a/login')

    def test_newAdminLost(self):
        self.login('john', 'johnpassword')
        sleep(2)
        self.browser.get(self.live_server_url + '/a/adminpage/list')
        self.wait.until(EC.presence_of_elements_located((By.ID, 'fileUploadBtn')))
        submit_button1 = self.browser.find_element_by_id('new-admin')
        submit_button1.click()
        self.browser.get_screenshot_as_file('tests/pic/41_login.png')
        sleep(1)





