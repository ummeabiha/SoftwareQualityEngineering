from webDriverSetup import get_chrome_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logging.basicConfig(level=logging.INFO)

driver = get_chrome_driver()
driver.get('http://localhost:5173/bytebazaar/reset-password')

error_messages = [
'400: "password" should contain at least 1 lower-cased letter',
'400: "password" should contain at least 1 upper-cased letter',
'400: "password" should contain at least 1 number',
'400: "password" should contain at least 1 symbol',
'400: "password" should be at least 8 characters long',
'400: Passwords do not match',
'400: "email" must be a valid email',
'404: undefined',
'Password have been changed successfully',
]

print("Title: ", driver.title)

def check_toast_message(test_num, expected_message, toast_message):
    if expected_message in toast_message:
        logging.info(f"Test case '{test_num}' passed: Expected toast message '{expected_message}' received")
    else:
        logging.error(f"Test case '{test_num}' failed: Expected toast message '{expected_message}' not received. Actual: {toast_message}")

def clear_and_send_keys(element, keys):
    element.clear()
    element.send_keys(keys)
    time.sleep(0.5)

def test_form_submission(email, password, confirmPassword):
    email_input = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
    confirmPassword_input = driver.find_element(By.CSS_SELECTOR, "input[name='confirmPassword']")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    clear_and_send_keys(email_input, email)
    clear_and_send_keys(password_input, password)
    clear_and_send_keys(confirmPassword_input, confirmPassword)

    submit_button.click()

    toast_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@role='alert']")))

    toast_message = toast_element.text

    if toast_element.is_displayed():
        close_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='Toastify']//button[@aria-label='close']")))
        close_button.click()

    return toast_message

# Testing Navigation Links on Login Form
def navigation_test_status(expected_url):
    current_url = driver.current_url

    if (expected_url == current_url) or (expected_url in current_url):
        logging.info(f"Test case passed: URL navigation occurred to {expected_url}.")
    else:
        logging.error("Test case failed: URL navigation did not occur.")

    time.sleep(1)
    driver.get("http://localhost:5173/bytebazaar/reset-password")

def test_navigation_links():
    print("\nRunning Tests for Reset Password Link")
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Do not have an account? Signup!']"))).click()
    navigation_test_status('http://localhost:5173/bytebazaar/signup')

# RUN TEST CASES
def run_test_cases():
    with open('./TestDataFiles/testResetPswdData.txt', 'r') as file:
        print("\nRunning Tests for Forgot Password Form")
        lines = file.readlines()
        for line in lines:
            data = line.strip().split(',')
            email, password, confirmPassword = data
            toast_message = test_form_submission(email, password, confirmPassword)
            logging.info(f"Submitting form with data: {data}")
            logging.info(f"Toast message: {toast_message}")
            check_toast_message(lines.index(line) + 1, error_messages[lines.index(line)], toast_message)
            print("\n")

    time.sleep(1)
    driver.back()
    time.sleep(2)
    test_navigation_links()

run_test_cases()

time.sleep(1)
driver.quit()
