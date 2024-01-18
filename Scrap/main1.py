import os
#necessary to call modules of the file system
wk = "project_url/main_location"
os.chdir(wk)

from planning import *
from driv3r import *
from m0ng0 import *
from gmai1.quickstart import *

from datetime import datetime
import time
import numpy as np


#gmail
service = connect2gmail()
query = "is:unread (from:mail address 1 OR from:mail address 2 OR mail address 3)"
destination = 'mail address'
subject = 'Status'

###
schedule = robotUnion()  
print(schedule)
#morning_start = schedule[0]-current_time()
#sleep(morning_start)
#Start session
driver = Driver()   
#sub window to scroll in if exists in the page structure to scrap           
vignettes_window_XPATH = 'XPATH'
#group to pass the cursor in 
vignettes_selector = 'Selector:nth-child(n)' 
#######################################################

#listes
scrap_var_1 = []
scrap_var_i = []
scrap_var_n = []
numeroDEpage = []
indexDANSlaPage = []
position_dans_la_page = []
totalVignettesInPage = []
jourDuScrapping = []
heureDuScraping = []
capchat_occurrence_since_begening = [] 
sent = []
VignetteHeight = []
lastVignetteHeight = 0
#Initiat variables relatively to previous scrap
##connect to mongoDB
collection = connect2collection('DB_name', 'Collection_name')
#If collection empty
if collection.count_documents({}) == 0:
    print('h')
    #itérateurs
    page = 1
    i = 1
    driver.get('url to scrap')
    sleep(np.random.uniform(10,20))
    #frame                           
    init_v = get_window_and_vignettes(driver,vignettes_window_XPATH, vignettes_selector)
    vignettes_window = init_v[0]
    vignettes = init_v[1]
    current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", vignettes_window)
    last_capchat_occurrence_since_begening = 0
else:
    #If collection not empty
    last_i =  last_value(collection, 'indexDANSlaPage')
    last_page = last_value(collection, 'numeroDEpage')
    last_capchat_occurrence_since_begening = last_value(collection, 'capchat_occurrence_since_begening')
    tot_vignettes_in_page = last_value(collection, 'totalVignettesInPage')
    #If last inserted page completed
    if last_i == tot_vignettes_in_page:
        print('f')
        #itérateurs
        page = last_page + 1
        i = 1
        driver.get(f'url_to_scrap_page={last_page}')
        #frame
        init_v = get_window_and_vignettes(driver,vignettes_window_XPATH, vignettes_selector)
        vignettes_window = init_v[0]
        go2nextpage(driver, vignettes_window)
        sleep(np.random.uniform(10,20))
        #frame
        init_v = get_window_and_vignettes(driver,vignettes_window_XPATH, vignettes_selector)
        vignettes_window = init_v[0]
        vignettes = init_v[1]
        current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", vignettes_window)
    else:
        print('g')
        #If last inserted page not completed
        #itérateurs
        i = last_i + 1 
        page = last_page  
        driver.get(f'url_to scrap_page={page}')
        #frame 
        init_v = get_window_and_vignettes(driver,vignettes_window_XPATH, vignettes_selector)
        vignettes_window = init_v[0]
        vignettes = init_v[1]
        current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", vignettes_window)
        print(current_scroll_position)
        print(type(current_scroll_position))
        lastVignetteHeight = last_value(collection, 'VignetteHeight')
        last_scroll_position = last_value(collection, 'position_dans_la_page')
        current_scroll_position = scroll(driver, vignettes_window, current_scroll_position, lastVignetteHeight, 0, last_scroll_position)
L = [scrap_var_1, scrap_var_i, scrap_var_n, numeroDEpage, indexDANSlaPage , position_dans_la_page, totalVignettesInPage, jourDuScrapping, heureDuScraping, capchat_occurrence_since_begening, sent, VignetteHeight]
    
###################################################################################

while 2 + 2 == 4:
    for index in range(0, len(vignettes[i-1:])):
        vignette = vignettes[i-1]
        if (current_time() < schedule[1] or (current_time() >= schedule[2] & current_time() < schedule[3])): 
            if 'sleep'.casefold() in read_last_command(service, query).casefold():
                send_message(service, destination, subject, 'Asleep')
                while 'run'.casefold() not in read_last_command(service, query).casefold():
                    time.sleep(5)
                    print('asleep')
                send_message(service, destination, subject, 'Runing')
                print('runing')
                send_message(service, destination, subject, 'Runing')
            #XPATH                          
            scrap_var_1_XPATH = f'XPATH1/tag[{i}]'
            scrap_var_i_XPATH = f'XPATHi/tag[{i}]'
            scrap_var_n_XPATH = f'XPATHn/tag[{i}]'
            VignetteSize = vignette.size['height']
            #if a previous session did not finish to scrap each vignette
            if lastVignetteHeight != 0:
                VignetteHeight.append(VignetteSize + lastVignetteHeight)
                lastVignetteHeight = 0
            elif VignetteHeight != [] and i != 1:
                VignetteHeight.append(VignetteSize + VignetteHeight[-1])
            else:
                VignetteHeight.append(VignetteSize)
            #X contains variables XPATH that we are reaching to scrap
            X = [scrap_var_1_XPATH, scrap_var_i_XPATH, scrap_var_n_XPATH]
            l_control = 0
            print(i)
            for elementList, elementXPATH in zip(L[0:n], X):
                Scrap = scrap(driver, elementList, l_control, elementXPATH, page, capchat_occurrence_since_begening, vignettes_window, current_scroll_position, last_capchat_occurrence_since_begening, vignettes_window_XPATH, vignettes_selector, VignetteHeight, VignetteSize)
                l_control = Scrap[0]
                last_capchat_occurrence_since_begening = Scrap[1]
                #means that DOM has changed due to refreshing
                if type(Scrap[2]) == list:
                    vignettes_window = Scrap[2][0]
                    vignettes = Scrap[2][1]
            capchat_occurrence_since_begening.append(last_capchat_occurrence_since_begening)
            jourDuScrapping.append(datetime.now().strftime("%Y-%m-%d"))
            heureDuScraping.append(datetime.now().strftime("%H-%M-%S"))
            indexDANSlaPage.append(i) 
            numeroDEpage.append(page)
            totalVignettesInPage.append(len(vignettes))
            sent.append('False')
            result = '###'.join(str(m[-1]) if len(m) > 0 else '' for m in L)
            print(result)
            sleep(np.random.uniform(20,40))
            #random nap (not advised while testing)
            # if int(np.random.uniform(1,100)) == 42:
            #     sleep(np.random.uniform(120,720))
            if i < number_of_vignettes_in_a_page:
                try:
                    #scroll()
                    # eg: current_scroll_position of vignette1 = start of vignette2 position
                    current_scroll_position = scroll(driver, vignettes_window, current_scroll_position, VignetteHeight[-1], VignetteSize)
                except StaleElementReferenceException:
                    print('?')
                    current_scroll_position = scroll(driver, vignettes_window, current_scroll_position, VignetteHeight[-1], VignetteSize)
            i += 1
            position_dans_la_page.append(current_scroll_position)
            print(f'{i} in {len(vignettes)}')
            if i > len(vignettes):
                print(f"{i} last in page {len(vignettes)}")
                export2atlas(L, collection)
                #reset
                scrap_var_1 = []
                scrap_var_i = []
                scrap_var_n = []
                numeroDEpage = []
                indexDANSlaPage = []
                position_dans_la_page = []
                totalVignettesInPage = []
                jourDuScrapping = []
                heureDuScraping = []
                last_capchat_occurrence_since_begening = capchat_occurrence_since_begening[-1]
                capchat_occurrence_since_begening = []
                sent = []
                VignetteHeight = []
                L = [scrap_var_1, scrap_var_i, scrap_var_n, numeroDEpage, indexDANSlaPage , position_dans_la_page, totalVignettesInPage, jourDuScrapping, heureDuScraping, capchat_occurrence_since_begening, sent, VignetteHeight]
                sleep(np.random.uniform(10,20))
                go2nextpage(driver, vignettes_window)
                i = 1
                page += 1
                sleep(np.random.uniform(300,500))
                reset_v = get_window_and_vignettes(driver,vignettes_window_XPATH, vignettes_selector)
                vignettes_window = reset_v[0]
                vignettes = reset_v[1]
                current_scroll_position = driver.execute_script("return arguments[0].scrollTop;", vignettes_window)

                 
        elif (current_time() < schedule[2]):
                    sleep(time2sec(schedule[2] - current_time()))
        else: 
            driver.quit()                   
            export2atlas(L, collection)
            # This code allows to send 500 extracted vignettes to reffered mail addresses
            # if not have been sent yet
            # if count_value('sent', 'False') >= 500:
            #      workbook = import_collection('DB name', 'Collection name')
            #      send_message(service, 'mail1', '500 leads', '', workbook)
            #      send_message(service, 'mail2', '500 leads', '', workbook)
            #sleep(time2sec(240000 + schedule[0] - schedule[3]))     
            break


