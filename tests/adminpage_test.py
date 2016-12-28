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
        self.wait = WebDriverWait(self.browser, 5)
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

    def test_admin_login_with_right_pass(self):
        self.login('john', 'johnpassword')
        self.browser.get_screenshot_as_file('tests/1_login.png')
        self.browser.get(self.live_server_url + '/a/adminpage/list')
        self.browser.get_screenshot_as_file('tests/2_list.png')

