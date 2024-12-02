from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    # Configure your credentials and the URL
    email = "agrestjj@dukes.jmu.edu"
    password = "Disney$&k362003J"
    duo_username = "agrestjj@dukes.jmu.edu"  # If different from your email

    # Start Chrome and navigate to the email login page
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://dukes.jmu.edu/")  # Replace with the actual login URL

    # Wait for the page to load
    time.sleep(2)

    # Log in to the email service
    usernameField = driver.find_element(By.NAME, "loginfmt")
    usernameField.send_keys(email)
    usernameField.submit()  # Email Submit

    passwordField = driver.find_element(By.NAME, "i0118")
    passwordField.send_keys(password)
    passwordField.submit()  # Password Submit

    # Wait for the Duo prompt
    time.sleep(5)

    # Handle Duo Authentication
    # Choose the appropriate method: push, call, or enter a passcode
    # Example for sending a push notification
    driver.find_element(By.LINK_TEXT, "Send Me a Push").click()

    # Wait for the authentication to complete
    time.sleep(10)  # Adjust this if necessary

    # Now you are logged in, and you can perform any actions
    print("Logged in successfully!")

    # Don't forget to close the driver
    # driver.quit()


if __name__ == "__main__":
    main()