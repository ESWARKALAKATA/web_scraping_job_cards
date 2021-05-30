"""
@author: eswar
"""
#scaraping job desciptions from monister.com 
#same impletion can be done for sourcing candidates
#for sourcing candidates details we need employeer cridentials



from time import *
from selenium import webdriver
import pymongo
from pymongo.results import InsertManyResult


client = pymongo.MongoClient()
mydb =  client['jobs']
collection  = mydb['cards']

client = pymongo.MongoClient()

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.monsterindia.com/")

driver.implicitly_wait(9)
driver.find_element_by_id("SE_home_autocomplete").send_keys("java ,spring ,sql ,hibernate")


#for normal search use this 
driver.find_element_by_xpath("//body/div[@id='themeDefault']/section[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/form[1]/div[1]/div[2]/input[1]").click()
driver.implicitly_wait(20)
temp = 1
while(True):
    if temp == 5:
        break
    all_jobs =  driver.find_elements_by_class_name("card-apply-content")
    link_list = []
    for job in all_jobs:
        try:
            company = ""
            com_name = job.find_elements_by_class_name("job-tittle")
            driver.implicitly_wait(1)
            for ele in com_name:
                company = ele.find_element_by_class_name('company-name').text
            
            location = job.find_element_by_class_name("loc").text

            driver.implicitly_wait(1)
            lnks= job.find_elements_by_tag_name("a")
            for lnk in lnks:
                link_list.append(lnk.get_attribute('href'))
                break
            driver.implicitly_wait(1)
            desc = job.find_element_by_class_name("job-descrip").text
            driver.implicitly_wait(1)
            skills = job.find_element_by_class_name("descrip-skills").text

        except:
            desc =  'desc Not Specified'
            skills =  'skills Not Specified'  
            location = ' location Not Specified'
            company = 'company  Not Specified'
        
        s = skills.split(' ')
        for i in s:
            if i == ',':
                s.remove(',')
        data = {"comapany_name": company,"job_location": location,"job_desc":desc,"skills":s[2::],"card_link":link_list[0]}
        link_list.clear()
        y =  collection.insert_one(data)
        print(y.inserted_id)
    driver.find_element_by_xpath("//button[contains(text(),'Next')]").click()
    sleep(25)
    temp = temp +1







#driver.quit()
