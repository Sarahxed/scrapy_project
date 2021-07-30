import time
from logging import getLogger

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


option = ChromeOptions()
option.add_argument('disable-infobars')
option.add_argument("disable-blink-features=AutomationControlled")
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"')


class SeleniumMiddleware:
    login_url = 'https://login.taobao.com/member/login.jhtml'

    def __init__(self, timeout=None, username=None, password=None):
        self.logger = getLogger()
        self.timeout = timeout
        self.browser = webdriver.Chrome("chromedriver", 0, options=option)
        # 淘宝对selenium + chromedriver做了反爬
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.username = username
        self.password = password
        self.login()


    def __del__(self):
        self.browser.close()

    def login(self):
        self.browser.get(self.login_url)
        time.sleep(1)
        self.write_username()
        self.logger.debug('Input Username!')
        time.sleep(1)
        self.write_password()
        self.logger.debug('Input Password!')
        time.sleep(1)
        if self.lock_exist() is True:
            self.logger.debug('Lock Exist!')
            self.check_stock()
        time.sleep(1)
        self.submit()
        self.logger.debug('Login Success!')

    def write_username(self):
        """输入用户名"""
        username_input = self.browser.find_element_by_name('fm-login-id')
        username_input.clear()
        username_input.send_keys(self.username)

    def write_password(self):
        """
        输入密码
        :param password:
        :return:
        """
        password_input = self.browser.find_element_by_id("fm-login-password")
        password_input.clear()
        password_input.send_keys(self.password)

    def lock_exist(self):
        """
        判断是否存在滑动验证
        :return:
        """
        nc_1_n1z = self.browser.find_element_by_id('nc_1_n1z')
        if nc_1_n1z.is_displayed():
            return True
        else:
            return False

    def get_track(self, distance):  # distance为传入的总距离
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 1

        while current < distance:
            if current < mid:
                # 加速度为2
                a = 4
            else:
                # 加速度为-2
                a = -3
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, slider, tracks):
        """
        滑块解锁破解
        :param slider: 移动的滑块
        :param tracks: 移动轨迹
        :return: None
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            time.sleep(0.1)
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def check_stock(self):
        slider = self.browser.find_element_by_xpath("//span[contains(@class, 'btn_slide')])]")
        if slider.is_displayed():
            ActionChains(self.browser).click_and_hold(on_element=slider).perform()
            ActionChains(self.browser).move_by_offset(xoffset=258, yoffset=0).perform()
            ActionChains(self.browser).pause(0.5).release().perform()


    def submit(self):
        """
        提交登录
        :return:
        """
        self.browser.find_element_by_css_selector('.password-login').click()
        time.sleep(0.5)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   username=crawler.settings.get('USERNAME'),
                   password=crawler.settings.get('PASSWORD')
                   )

    def process_request(self, request, spider):
        """使用PhantomJS抓取页面"""
        self.logger.debug('PhantomJS is Starting!')
        page = request.meta.get('page', 1)
        try:
            self.browser.get(request.url)
            print(request.url)
            time.sleep(2)
            # 等待滑动拖动控件出现
            swipe_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#nc_1_n1z")))
            self.move_to_gap(swipe_button, self.get_track(3600))
            html_slider = self.browser.page_source
            while '哎呀，出错了，点击' in html_slider:
                print('滑块破解失败~')
                print('即将重新模拟~')
                time.sleep(60)
                self.browser.switch_to.frame("sufei-dialog-content")
                swipe_button = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#nc_1_n1z")))  # 等待滑动拖动控件出现
                self.browser.find_element_by_css_selector('#nocaptcha > div > span > a').click()
                self.move_to_gap(swipe_button, self.get_track(3600))
            if page > 1:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
                input.clear()
                submit.send_keys(page)
                # 等待页面跳转
            self.wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding='utf-8',
                                status=200)

        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
