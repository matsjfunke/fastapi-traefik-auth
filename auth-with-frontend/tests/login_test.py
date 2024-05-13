"""
matsjfunke
07.05.2024
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

# options = webdriver.FirefoxOptions()
# options.headless = True

driver = webdriver.Firefox()  # options=options

port = 8000
driver.get(f"http://127.0.0.1:{port}/login")


username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")
submit_button = driver.find_element(By.ID, "submit")

username_field.send_keys("user1")
password_field.send_keys("foo")

submit_button.click()

print(driver.current_url)
if f"http://127.0.0.1:{port}/hello?username=user1" == driver.current_url:
    print("Login successful!")
elif "http://127.0.0.1/hello?username=user1" == driver.current_url:
    print("Login successful!")
else:
    print("Login failed.")

driver.implicitly_wait(5)
driver.quit()
