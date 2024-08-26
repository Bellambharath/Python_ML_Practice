from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# # Deprecated - no longer needed
# chrome_driver_path = "/Users/philippmuellauer/Development/chromedriver"
#
# # keeps chrome open
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("detach", True)
#
# # driver = webdriver.Chrome(executable_path=chrome_driver_path)
# # driver = webdriver.Chrome()
# driver = webdriver.Chrome(options=chrome_options)
#
# def test_eight_components():
#     driver.get("https://www.selenium.dev/selenium/web/web-form.html")
#     title = driver.title
#     assert title == "Web form"
#     driver.implicitly_wait(0.5)
#     text_box = driver.find_element(by=By.NAME, value="my-text")
#     submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")
#     text_box.send_keys("Selenium")
#     submit_button.click()
#     message = driver.find_element(by=By.ID, value="message")
#     value = message.text
#     assert value == "Received!"
#
#     # Closes Chrome
#     # driver.quit()
#     driver.close()
#
#
# test_eight_components()


options_ch = webdriver.ChromeOptions()
options_ch.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options_ch)
driver.get("http://secure-retreat-92358.herokuapp.com/")

FirstName = driver.find_element(By.NAME, value="fName")
FirstName.send_keys("Bharath")
LastName = driver.find_element(By.NAME, value="lName")
LastName.send_keys("Bharath")
Email = driver.find_element(By.NAME, value="email")
Email.send_keys("Bharath@gmail.com")


Button = driver.find_element(By.TAG_NAME, value="button")
Button.click()

print(FirstName.text)
# driver.quit()
