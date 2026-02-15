

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import random
import undetected_chromedriver as uc

from time import sleep
import pandas as pd



import os




class Request:
    selenium_retries = 0
    def __init__(self, url):
        self.url = url

    
    def create_driver(self):
        try:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value, 
                                OperatingSystem.LINUX.value]

            user_agent_rotator = UserAgent(software_names=software_names,
                                        operating_systems=operating_systems,
                                        limit=100)

            user_agent = user_agent_rotator.get_random_user_agent()

            chrome_options = Options()
            chrome_options.add_argument('--window-size=1420,1080')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(f'user-agent={user_agent}')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            profile_path = os.path.abspath("./auth")
            chrome_options.add_argument(f'--user-data-dir={profile_path}')



            #THIS IS THE PART THAT YOU SHOULD UNCOMMENT IF YOU WANT TO ADD PROXY
            #proxy_host = "X.X.X.X"
            #proxy_port = "X"
            #chrome_options.add_argument(f'--proxy-server={proxy_host}:{proxy_port}')


            driver = uc.Chrome(options=chrome_options, version_main=144)
            

            

            
            
            
            

        
            

            return driver
    
        except Exception as e:
            print(e)
            return None
        
    def proxy_test(self):
        try:
            driver = self.create_driver()
            driver.get("http://lumtest.com/myip.json")

            html_content = driver.page_source
            print("Page HTML:", html_content)
        except Exception as e:
            print("Exepction", e)
    
    def login(self, driver):
        url = "https://secure.indeed.com/auth"




        driver.get(url)

        sleep(1)

        if "Account settings" in driver.page_source:
            print("You are already connected, redirection to home page...")
            return


        print("\n" + "="*50)
        print("ACTION: Please log in manually in the browser window.")
        print("Once you are logged in and see your dashboard,")
        print("press ENTER here to continue.")
        print("="*50 + "\n")

        sleep(0.5)
        
        input("Press Enter to continue...")

        
    
    def export_csv(self, results, filename):

        if not results:
            return 
        
        df = pd.DataFrame(results)

        df.to_csv(filename, index=False, encoding='utf-8-sig')

        print(f"--- Succès ! {len(df)} jobs sauvegardés dans {filename} ---")


    
    def get_data(self, job):
        job_name = ""
        job_company = ""
        job_type = ""
        job_location = ""

        if job.is_displayed() and job.is_enabled():
            print("Hello")
            try:
                job_name = job.find_element(By.CLASS_NAME, "jcs-JobTitle").text
                print(job_name)
            except:
                pass
            try:
                job_company = job.find_element(By.CLASS_NAME, "css-19eicqx").text
            except:
                pass
            try:
                job_type = job.find_element(By.CLASS_NAME, "css-zydy3i").text
            except:
                pass
            try:
                job_location = job.find_element(By.CLASS_NAME, "css-1f06pz4").text
            except:
                pass
        else:
            print("Element exists in HTML but is hidden/off-screen.")
            return
        

        data = {
            "Job": job_name,
            "Company": job_company,
            "Type": job_type,
            "Location": job_location
        }

        return data



        
    def scraping(self, job, localisation):

        filename = f"{job.replace(' ', '_')}_{localisation.replace(' ', '_')}.csv"

        driver = self.create_driver()
        self.login(driver)
        driver.get(self.url)
        

        target_url = f"{self.url}/jobs?q={job}&l={localisation}"


        driver.get(target_url)
        count = 0
        results = []
        while True:
            

            url = driver.current_url
            
            sleep(random.uniform(0.5, 0.5))

            pop_up = driver.find_elements(By.CLASS_NAME, "css-14ii8a0")

            if len(pop_up) > 0 :
                pop_up = pop_up[0]
                pop_up.click()




            driver.set_page_load_timeout(30)
            jobs = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
            n_jobs = len(jobs)
            for job in jobs:
                data = self.get_data(job)
                if data:
                    results.append(data)

            

            try:
                pages = driver.find_elements(By.CSS_SELECTOR, "li.serp-page-8umzvb")

                arrow_next = pages[-1]

                current_page = driver.find_element(By.XPATH, '//a[@data-testid="pagination-page-current"]/ancestor::li')


                if(current_page == arrow_next):
                    break               

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", arrow_next)
                sleep(1)

                arrow_next.click()

            except Exception as e:
                print(e)
                break
        
        
        print(results)
        self.export_csv(results, filename)
    

    def get_data_with_description(self, driver):
        job_name = ""
        job_company = ""
        job_type = ""
        company_rating = ""
        job_location = ""
        job_description = ""
        try:
            job_name = driver.find_element(By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/h2/span').text
            job_name = job_name.split('\n')[0].strip()
        except:
            pass
        try:
            job_company = driver.find_element(By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div/span/a').text
        except:
            pass
        try:
            job_type = driver.find_element(By.XPATH, '//*[@id="jobDetailsSection"]/div/div[1]/div[2]/div/div/div/ul/li/button/div/div/div/span').text
        except:
            pass
        try:
            company_rating = driver.find_element(By.XPATH, '//*[@id="jobsearch-ViewjobPaneWrapper"]/div/div/div[2]/div[2]/div[1]/div/div[1]/div[2]/div/div/div/div[1]/div[2]/span[1]').text
        except:
            pass
        try:
            job_location = driver.find_element(By.XPATH, "//*[@id='jobLocationText']/div").text
        except:
            pass
        try:
            job_description = driver.find_element(By.XPATH, '//*[@id="jobDescriptionText"]').text
        except:
            pass


        data = {

            "Job": job_name,
            "Company": job_company,
            "Type": job_type,
            "Rating": company_rating,
            "Location": job_location,
            "Description": job_description

        }

        return data


    
    def scraping_with_description(self, job, localisation):

        filename = f"{job.replace(' ', '_')}_{localisation.replace(' ', '_')}.csv"

        driver = self.create_driver()
        driver.get(self.url)

        self.login(driver)

        target_url = f"{self.url}/jobs?q={job}&l={localisation}"


        sleep(random.uniform(3, 5))

        driver.get(target_url)

        count = 0

        results = []

        while True:

            sleep(random.uniform(3, 5))

            pop_up = driver.find_elements(By.CLASS_NAME, "css-14ii8a0")

            if len(pop_up) > 0 :
                pop_up = pop_up[0]
                pop_up.click()


            driver.set_page_load_timeout(30)

            jobs = driver.find_elements(By.CLASS_NAME, "jcs-JobTitle")

            for job in jobs:
                if job.is_displayed() and job.is_enabled():
                    driver.execute_script("arguments[0].click();", job)
                else:
                    print("Element exists in HTML but is hidden/off-screen.")
                    continue
                sleep(random.uniform(1, 6))

                data = self.get_data_with_description(driver)

                results.append(data)




            try:

                pages = driver.find_elements(By.CSS_SELECTOR, "li.serp-page-8umzvb")

                arrow_next = pages[-1]

                current_page = driver.find_element(By.XPATH, '//a[@data-testid="pagination-page-current"]/ancestor::li')

                if(current_page == arrow_next):
                    break              

                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", arrow_next)
                sleep(1)

                arrow_next.click()



            except Exception as e:

                print(e)

                break

        

        self.export_csv(results, filename)




request = Request("https://ma.indeed.com")

request.scraping("data scientist senior", "Maroc")

#uncomment to test the proxy
#request.proxy_test()
