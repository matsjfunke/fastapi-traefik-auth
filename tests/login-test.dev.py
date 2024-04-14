"""
Mats Funke
26.01.2024
"""
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.FirefoxOptions()
options.headless = True

driver = webdriver.Firefox(options=options)

# outside docker
port = 8011
driver.get(f"http://127.0.0.1:{port}/login")


username_field = driver.find_element(By.NAME, "username")
password_field = driver.find_element(By.NAME, "password")
time_frame_field = driver.find_element(By.NAME, "time_frame")
submit_button = driver.find_element(By.ID, "submit")

username_field.send_keys("user1")
password_field.send_keys("foo")

all = ""
year = "2023"
year_month = "2024-01"
full_date = "2023-12-07"
time_frame_field.send_keys(full_date)

submit_button.click()

print(driver.current_url)
if f"http://127.0.0.1:{port}/table" == driver.current_url:
    print("Login successful!")
elif "http://127.0.0.1/table" == driver.current_url:
    print("Login successful!")
else:
    print("Login failed.")

driver.implicitly_wait(5)
driver.quit()
