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

The Request class provides two main scraping methods:

## Fast Mode (Without Description)

This method extracts job listings without retrieving their full descriptions.
It is significantly faster because it does not simulate interaction with each individual job post.

## Full Mode (With Description)

This method retrieves complete job descriptions.
To access the description content, Selenium simulates clicking on each job listing displayed on the page.

To reduce the risk of triggering bot detection mechanisms (such as the "Verify you are not a robot" page), a randomized delay of 1 to 6 seconds is introduced between each click.
This makes the scraping behavior more human-like, but increases overall execution time.

## Authentication Handling

The Login() function is automatically triggered the first time the program is executed.
It allows the user to manually sign in to their Indeed account.

Once authenticated:

- Session data is stored in the auth/ directory.
- Future executions reuse the stored session.
- The user does not need to log in again unless the session expires.

## Proxy Support

Proxy usage can be integrated to reduce the risk of IP blacklisting due to a high number of requests.

Proxies can be configured within the scraper.

The proxy_test function ensures that requests are properly routed through the configured proxy.

## User-agent

A user-agent rotator is implemented to reduce the likelihood of bot detection.
It randomly changes the User-Agent header for each session, making the traffic appear as if it originates from different browsers or devices.

By rotating User-Agent strings, the scraper avoids repeatedly sending requests with the same browser signature, which helps lower the risk of being flagged by anti-bot systems.

## Headless-mode

This project does not use headless mode, and so the browser window is visibly opened during the execution, it is impossible to use during the sign in phase, but you can add it afterward, when the user data are saved, but not having the headless mode on is generally better as it makes it harder for the anti-bot detection flag to trigger.

# Disclaimer
This project is for educational and personal use only. Users are responsible for complying with Indeed's Terms of Service. The author assumes no liability for misuse of this tool.
