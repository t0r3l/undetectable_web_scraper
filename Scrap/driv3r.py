import undetected_chromedriver as uc
from webdriver_manager.core.os_manager import OperationSystemManager,ChromeType

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, WebDriverException 

from time import sleep
import numpy as np


#The project of lunching the bot on a debian server had been initialize however averted due to troubles to mask fingerprinting and lake of time
def DriverDeb():
    br_ver = OperationSystemManager().get_browser_version_from_os(ChromeType.GOOGLE)
    version_main=int(br_ver.split('.')[0])
    options = uc.ChromeOptions()
    options.add_argument("--user-data-dir=~/.config/google-chrome/")
    options.add_argument(r'--profile-directory=Default')
    driver_path = '/usr/bin/google-chrome'
    driver = uc.Chrome(executable_path=driver_path, version_main=version_main, options=options, service=Service(driver_path))
    return driver


def Driver():
    br_ver = OperationSystemManager().get_browser_version_from_os(ChromeType.GOOGLE)
    version_main=int(br_ver.split('.')[0])
    options = uc.ChromeOptions()
    #in order to don't have to pass by log page each time which might be considered as a suspicious behaviour by the social network create a chrome profile 
    #and log it once to then use it as the driver profile
    options.add_argument("--user-data-dir= path to chrome profile")
    options.add_argument(r'--profile-directory= profile name')
    driver_path = 'path to chrome.exe' 
    driver = uc.Chrome(executable_path=driver_path, version_main=version_main, options=options, service=Service(driver_path))
    return driver

def go2nextpage(driver, vignettes_window):
    current = driver.current_url
    # Scroll to the bottom of the subwindow using JavaScript
    c = driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", vignettes_window)
    print(c)
    # Switch to iframe by name or ID
    
    # Scroll to the bottom of the iframe
    # print(current_scroll_position)
    # driver.execute_script("arguments[0].scrollTop = arguments[1];", vignettes_window, current_scroll_position + int(np.random.uniform(57, 65)))
    # FeedbackButtonXPATH = '/html/body/main/div[1]/div[2]/div[2]/div/div[4]/div[2]/button[1]'
    # closeFeedbackXPATH = '/html/body/main/div[1]/div[2]/div[2]/div/div[4]/button'
    # suivantButtonXPATH = "//button[text()='Submit']"
    # sleep(np.random.uniform(5,10))
    # try:
    #     print(1)
    #     WebDriverWait(driver,120).until(
    #                         EC.element_to_be_clickable((By.XPATH, suivantButtonXPATH))
    #                         )
    #     suivantButton = driver.find_element_by_xpath("//button[text()='Suivant']")
    #     sleep(np.random.uniform(5,10))
    #     suivantButton.click()
    #     sleep(10)
    #     if current == driver.curent_url:
    #         print('2bis')
    #         suivantButtonXPATH = '/html/body/main/div[1]/div[2]/div[2]/div/div[5]/div/button[2]/span'
    #         WebDriverWait(driver,120).until(
    #                             EC.element_to_be_clickable((By.XPATH, suivantButtonXPATH))
    #                             )
    #         suivantButton = driver.find_element(By.XPATH, suivantButtonXPATH)
    #         sleep(np.random.uniform(5,10))
    #         suivantButton.click()
    #         sleep(np.random.uniform(3,5))
    # except (TimeoutException, StaleElementReferenceException, NoSuchElementException, WebDriverException):  
    #         try: 
    #             print(2)/html/body/main/div[1]/div[2]/div[2]/div/div[5]/div/button[2]/span
    suivantButtonXPATH = '/html/body/main/div[1]/div[2]/div[2]/div/div[5]/div/button[2]/span'
    WebDriverWait(driver,120).until(
                        EC.element_to_be_clickable((By.XPATH, suivantButtonXPATH))
                        )
    suivantButton = driver.find_element(By.XPATH, suivantButtonXPATH)
    sleep(np.random.uniform(5,10))
    suivantButton.click()
    sleep(np.random.uniform(3,5))
                # WebDriverWait(driver,600).until(
                #                     EC.element_to_be_clickable((By.XPATH, FeedbackButtonXPATH))
                #                     )
                # FeedbackButton = driver.find_element(By.XPATH, FeedbackButtonXPATH)
                # sleep(np.random.uniform(5,10))
                # FeedbackButton.click()
                # sleep(np.random.uniform(3,5))
                # WebDriverWait(driver,600).until(
                #                     EC.element_to_be_clickable((By.XPATH, closeFeedbackXPATH))
                #                     )  
                # closeFeedback = driver.find_element(By.XPATH, closeFeedbackXPATH)
                # sleep(np.random.uniform(5,10))
                # closeFeedback.click()
                # sleep(np.random.uniform(3,5))

            # except (TimeoutException, StaleElementReferenceException, NoSuchElementException, WebDriverException):
            #     print(3)              
            #     suivantButtonXPATH = '/html/body/main/div[1]/div[2]/div[2]/div/div[4]/div/button[2]' 
            #     WebDriverWait(driver,120).until(
            #                         EC.element_to_be_clickable((By.XPATH, suivantButtonXPATH))
            #                         )
            #     # Use JavaScript to scroll to the Suivant button
            #     suivantButton = driver.find_element(By.XPATH, suivantButtonXPATH)
            #     sleep(np.random.uniform(5,10))
            #     suivantButton.click()
            #     sleep(np.random.uniform(3,5))

        
#This scrolling function has been devlopped to behave as a human user

def scroll(driver, vignettes_window, current_scroll_position, VignetteHeight, VignetteSize, last_scroll_position = 0):
    #if last_scroll_position == True meaning argument has been passed for it otherwise == 0 so False
    #the folowing block is meant to keep deviation in [-1, 1]; function resets deviation to 0 otherwise
    #Initiating variables
    up_or_down = np.random.uniform(0, 1.1)*(-1)**np.random.choice([1, 2])
    #if deviation exceeds setted value  (line 126) scrolling will opere to exact position of start of following vignette 
    deviation = 0
    scroll_position_to_compare = 0
    #scrolling is made from a vignette to the consecutive one (see line 166 & 171 mai1.py)
    if last_scroll_position == 0:
        print('a')
        #Sum of last_scroll_position and VignetteSize(length of vignette to scroll)
        scroll_position_to_compare = current_scroll_position + VignetteSize
        #VignetteHeight is the exact position of last scraped vignette??????????????????????????
        deviation = (VignetteHeight - scroll_position_to_compare)
        #If deviation outrange [-1:1] the scrolling is reset to to VignetteHeight
        if (deviation >= 1 or deviation <= -1):
            up_or_down = deviation
        scroll_distance = round(VignetteSize + up_or_down, 2)
    else:
        print('b')
        scroll_distance = last_scroll_position
    #random number between 1 and 2
    number_of_scrolls = int(np.random.uniform(1,3))
    if number_of_scrolls == 1:
        print('c')
        for i in range(int(scroll_distance)):
            driver.execute_script("arguments[0].scrollTop = arguments[1];", vignettes_window, current_scroll_position + 1)
            sleep(np.random.uniform(1/60000, 1/30000))
            current_scroll_position += 1
        #Add/subtract float part
        driver.execute_script("arguments[0].scrollTop = arguments[1];", vignettes_window, current_scroll_position + scroll_distance - int(scroll_distance))
        current_scroll_position += scroll_distance - int(scroll_distance)
    else: 
        print('d')
        #split scrolling in two sequences  
        distance_to_scroll_percentage = np.random.uniform(0.10,0.75)   
        distance1 = scroll_distance * distance_to_scroll_percentage  
        distance2 = scroll_distance - distance1
        #first sequence
        for i in range(int(distance1)):
            driver.execute_script("arguments[0].scrollTop = arguments[1];", vignettes_window, current_scroll_position + 1)
            sleep(np.random.uniform(1/600, 1/300))
            current_scroll_position += 1
        #Add/subtract float part 
        driver.execute_script("arguments[0].scrollTop = arguments[1];", vignettes_window, current_scroll_position + distance1 - int(distance1))
        current_scroll_position += distance1 - int(distance1)
        #pause
        sleep(np.random.uniform(1,3)) 
        #second sequence
        for i in range(int(distance2)):
            driver.execute_script("arguments[0].scrollTop = arguments[1];", vignettes_window, current_scroll_position + 1)  
            sleep(np.random.uniform(1/30000,1/10000))
            current_scroll_position += 1
        #Add/subtract float part 
        driver.execute_script("arguments[0].scrollTop = arguments[1];", vignettes_window, current_scroll_position + distance2 - int(distance2))
        current_scroll_position += distance2 - int(distance2)
    print(f'VignetteHeight: {VignetteHeight}')
    print(f'current_scroll_position: {current_scroll_position}')
    print(f'scroll_position_to_compare: {scroll_position_to_compare}')
    print(f'deviation: {deviation}')
    return current_scroll_position


#This function keeps track of capchats by recordig their url, source code and appearence to handle them. To make this function efficient a file system must be 
#created as the one provided in the repository
def capchat_recording(driver, last_capchat_witness):
    driver.save_screenshot(f"project_path/capchat_control/screenshots/capchatscreenshot{last_capchat_witness}.png")
    # Get the page source code
    page_source = driver.page_source
    # Specify the path where you want to save the page source code file
    file_path = f"project_path/capchat_control/codes_sources/capchat_source{last_capchat_witness}.html"
    # Save the page source code to the specified file path
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(page_source)
    # Get the current URL
    current_url = driver.current_url
    # Specify the path where you want to save the URL to a file
    url_path = f"project_path/capchat_control/url/capchat_url{last_capchat_witness}.txt"
    # Save the URL to the specified path
    with open(url_path, "w") as file:
        file.write(current_url)



def scrap(driver, elementList, l_control, scrap_var_i, elementXPATH, page, vignettes_window, current_scroll_position, last_capchat_witness,vignettes_window_XPATH, vignettes_selector, VignetteHeight, VignetteSize, refreshing = 0):
    reset_v2 = 0
    #A: Retrieve vignette's information
    try: 
        WebDriverWait(driver,600).until(
                        EC.presence_of_all_elements_located((By.XPATH, elementXPATH))
                        )
        sleep(2)
        #A1: Normal retrieving
        if l_control != iplus:                                     
            elementList.append(driver.find_element(By.XPATH, elementXPATH).text)
        #A2: Two informations are contained in the same XPATH see Readme scrap_var_i in part IV Scraping a page
        else:
            scrap_var_i_and_iplus_HTML= driver.find_element(By.XPATH, elementXPATH)
            scrap_var_i = scrap_var_i[-1]
            elementList.append(scrap_var_i_and_iplus_HTML.text.lstrip(scrap_var_i))  
        #Iterator of vignette's variables is incremented by 1    
        l_control += 1
    #B: XPATH not found
    except (TimeoutException, StaleElementReferenceException, NoSuchElementException, WebDriverException):   
        #B1: Capchat occured
        if driver.current_url not in ['possible_url_1', f'possible_url_page={page}']:
            last_capchat_witness += 1
                print('CAPCHAT?')
            #save informations about capchat
            capchat_recording(driver, last_capchat_witness)   
            #try: 
                #WebDriverWait(driver,10).until(
                            # EC.presence_of_all_elements_located((By.XPATH, capchatXPATH))
                            # ) 
                            # solve Capchat then return to point where program stoped
                            #retry to same point
                            # except (TimeoutException, StaleElementReferenceException, NoSuchElementException, WebDriverException):
                                #refresh page and retry to same point
        #B2: We are dealing with a variable of index z which often misses
        elif l_control == z:
            elementList.append('Na')
            l_control += 1
        #B3: None of the above cases => try to get results by refreshing page one time
        else:
            if refreshing == 0:
                #Might be sent through gmail api
                print('charging?')
                #incrementing 
                refreshing = 1
                driver.refresh()
                sleep(np.random.uniform(300,500))
                #reseting vignette window selector
                reset_v2 = get_window_and_vignettes(driver,vignettes_window_XPATH, vignettes_selector)
                vignettes_window = reset_v2[0]
                last_scroll_position = current_scroll_position
                #get back to previous scroll position
                current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", vignettes_window)
                current_scroll_position = scroll(driver, vignettes_window, current_scroll_position, VignetteHeight, VignetteSize, last_scroll_position)
                #Retry retrieving
                Scrap = scrap(driver, elementList, l_control, scrap_var_i, elementXPATH, page, vignettes_window, current_scroll_position, last_capchat_witness, vignettes_window_XPATH, vignettes_selector, VignetteHeight, VignetteSize, refreshing)
                l_control = Scrap[0]
                last_capchat_witness = Scrap[1]
            #B4: Failure of the program
            else:
                print('refreshing failed')
                #Keep session open to see the problem 
                #gmail API might be used here to warn technician
                while 2 + 2 == 4:
                    sleep(1)
    list2return =  [l_control, last_capchat_witness, reset_v2]
    return list2return
   

def lastIndex(collection, variable):
    pipeline = [
        {
            "$group": {
                "_id": None,
                "max_value": {"$max": variable}
            }
        }
    ]
    result = list(collection.aggregate(pipeline))

    lastIndex = result[0]["max_value"]
    return lastIndex

#vignette index must be compared with lenVignettes

#In the case of vignettes to scrap being in a sub window; this code allows to select it to scroll it.

def get_window_and_vignettes(driver,vignettes_window_XPATH, vignettes_selector):
    #charge page
    sleep(np.random.uniform(60, 120))
    #window
    WebDriverWait(driver, 600).until(
                    EC.presence_of_all_elements_located((By.XPATH, vignettes_window_XPATH))
                    )
    vignettes_window = driver.find_element(By.XPATH, vignettes_window_XPATH)  
    #vignettes
    WebDriverWait(driver,600).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, vignettes_selector))
                        )
    vignettes = driver.find_elements(By.CSS_SELECTOR, vignettes_selector)
    list2return = [vignettes_window, vignettes]
    return list2return


