import simple_colors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class AutoBot(webdriver.Edge):
    def __init__(self, driver_path=r"C:\SeleniumDriver\msedgedriver.exe", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        self.post_no = 1
        self.all_posts = [{0}]
        self.download = None

        super(AutoBot, self).__init__()
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            print("Quitting...")
            self.quit()

    def open_url(self, url):
        self.get(url)

    def select_state(self, state=None):
        self.implicitly_wait(5)
        self.find_element(by='xpath', value=f'//ul[@class="nav row"]/li/a[text()= "{state}"]').click()
        self.implicitly_wait(15)

    def select_county(self, county=None):
        self.implicitly_wait(5)
        self.find_element(by='xpath', value=f'//li[@ng-repeat="client in letterGroup.clients"]/a[text() = "{county}"]'
                          ).click()
        self.implicitly_wait(15)

    def search_bar(self, search=None):
        self.find_element(by='id', value='headerSearch').send_keys(search, Keys.ENTER)

    def search_per_page(self, posts):
        self.find_element(by='id', value='pageResultsSize').click()
        self.find_element(By.XPATH, f"//option[@label='{posts}']").click()

    def open_search(self, search=None):
        self.find_element(By.PARTIAL_LINK_TEXT, search).click()

    def all_headings(self, print_data=None):
        self.all_posts = self.find_elements(by='xpath', value='//div[@style="overflow: hidden;"]/div')
        if print_data:
            for post in self.all_posts:
                print(simple_colors.cyan(f'Result No.{self.all_posts.index(post) + 1}:', ['bold', 'underlined']))
                print(simple_colors.magenta(f'{post.text} \n'))

        # self.post_no = int(input("Enter the result no. you want to view in more detail:\n>"))
        # self.implicitly_wait(5)

    def download_pdf(self):
        self.find_element(by='xpath', value='//div[@class="col-md-9"]/button').click()
        self.find_element(By.CSS_SELECTOR, 'button[data-actionid="print"]').click()

    def download_sections(self, download):
        # download = (int(input('''
        # Press 0: Open section in webpage.
        # Press 1: Download section as Word file.
        # >''')))
        self.implicitly_wait(5)
        if not download:  # Open file
            self.find_element(by='xpath', value=f'//div[@style="overflow: hidden;"]/div[{self.post_no}]/div/div/div/h4'
                                                f'/a').click()
        else:  # Download file
            self.find_element(by='xpath', value=f'//div[@style="overflow: hidden;"]/div[{self.post_no}]/div/div/div/div'
                              ).click()
            self.find_element(By.CSS_SELECTOR, 'button[data-actionid="download"]').click()
            print(simple_colors.cyan("Download saved!"))

    def plant_pricing(self, plant=None):
        all_plants = self.find_elements(by='xpath', value=f"//div[@class='catalog-item']")
        print(len(all_plants))
        for item in all_plants:
            if plant in item.text:
                header_element = item.find_element(by='xpath', value="./article/header/h2")
                price_element = item.find_element(by='xpath', value="./article/div/div/div/a")
                print(f'Plant = {header_element.text}')
                print('Price =', price_element.text.replace("starting at", " ").strip())
