"""
Mats Funke
26.01.2024
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get('https://www.google.com/')


# outside docker
port = 8011
driver.get(f"http://localhost:{port}/login")

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
time_frame_field.send_keys(all)

submit_button.click()

print(driver.current_url)
if f"http://localhost:{port}/table?time_frame=all" == driver.current_url:
    print("Login successful!")

elif f"http://localhost:{port}/table?time_frame=2023-12-07" == driver.current_url:
    print("Login successful!")

elif f"http://localhost:{port}/table?time_frame=2024-01" == driver.current_url:
    print("Login successful!")

elif f"http://localhost:{port}/table?time_frame=2023" == driver.current_url:
    print("Login successful!")

else:
    print("Login failed.")

driver.implicitly_wait(5)
driver.quit()
