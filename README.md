# job-search-model

# Purpose

This project uses undetected_chromedriver with Selenium to scrape job listings from Indeed.
undetected_chromedriver helps reduce bot detection, making it more suitable for scraping websites with advanced security mechanisms.

# Requirements

Before running the project, make sure you have:
 - Python 3.x installed
 - All required Python dependencies (see requirements.txt).
 - Google Chrome installed.
 - ChromeDriver version 144 (must match your Chrome version for Selenium compatibility)
# Functionalities
there are two main functions in the Request Class that are used to scrap, the first one without description, way faster than the second version with description, because selenium needs to simulate clicking on every job in the page to have their description displayed, and there is a random delay (1 to 6 seconds) between each click used to avoid triggering the robot detection and the "verify that you are not a robot" page.
there is a function Login that is triggered the first time you run the algorithm, its purpose is to manually sign in, after that, the user data is stored in the auth folder, and the next times you run the algorithm, you wont have to login again.
You can also incorporate proxy usage in your scraping to avoid having your IP adress black listed because of too much requests. There is a test_proxy function used to make sure that your requests are send through your proxy. 

# Disclaimer
This project is for educational and personal use only. Users are responsible for complying with Indeed's Terms of Service. The author assumes no liability for misuse of this tool.
