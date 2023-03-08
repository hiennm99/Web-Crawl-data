import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import requests
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine

def connect_MySQL():
    #MySQL connection information
    mysql_redshift={
        'driver':'mysql+pymysql',
        'username':'root',
        'password':'',
        'host':'localhost',
        'database':'tiki'
    }
    mysql_engine=create_engine(f"{mysql_redshift['driver']}://{mysql_redshift['username']}:{mysql_redshift['password']}@{mysql_redshift['host']}/{mysql_redshift['database']}")
    return mysql_engine

def connect_AWSRedshift():
    #AWSRedshift connection information
    redshift_config={
        'driver':'redshift+psycopg2',
        'username':'',
        'password':'',
        'host':'',
        'port':5439,
        'database':''
    }
    redshift_engine=create_engine(f"{redshift_config['driver']}://{redshift_config['username']}:{redshift_config['password']}@{redshift_config['host']}:{redshift_config['port']}/{redshift_config['database']}")
    return redshift_engine

def convert_to_str(lst=[]):
    res=''
    for val in lst:
        res=res+str(val)+'/'
    res=res[0:-1]
    return res

def Get_Champion_Information():
    data=response.json().get('data')
    champs=[]
    for i in range(len(data)):
        champ_information=[]  
        champ_name=data[i]['name']
        print(f'------Start to retrieve champion {i} : {champ_name} information')
        champ_image=data[i]['image_url']
        
        passive=data[i]['passive']['name']
        passive_des=data[i]['passive']['description']
        
        skill_1=data[i]['spells'][0]['name']
        skill_1_des=data[i]['spells'][0]['description']
        cooldown_1=convert_to_str(data[i]['spells'][0]['cooldown_burn'])
        cost_1=convert_to_str(data[i]['spells'][0]['cost_burn'])
        range_1=convert_to_str(data[i]['spells'][0]['range_burn'])
        skill_1_image=data[i]['spells'][0]['image_url']
        
        skill_2=data[i]['spells'][1]['name']
        skill_2_des=data[i]['spells'][1]['description']
        cooldown_2=convert_to_str(data[i]['spells'][1]['cooldown_burn'])
        cost_2=convert_to_str(data[i]['spells'][1]['cost_burn'])
        range_2=convert_to_str(data[i]['spells'][1]['range_burn'])
        skill_2_image=data[i]['spells'][1]['image_url']
        
        skill_3=data[i]['spells'][2]['name']
        skill_3_des=data[i]['spells'][2]['description']
        cooldown_3=convert_to_str(data[i]['spells'][2]['cooldown_burn'])
        cost_3=convert_to_str(data[i]['spells'][2]['cost_burn'])
        range_3=convert_to_str(data[i]['spells'][2]['range_burn'])
        skill_3_image=data[i]['spells'][2]['image_url']
        
        skill_4=data[i]['spells'][3]['name']
        skill_4_des=data[i]['spells'][3]['description']
        cooldown_4=convert_to_str(data[i]['spells'][3]['cooldown_burn'])
        cost_4=convert_to_str(data[i]['spells'][3]['cost_burn'])
        range_4=convert_to_str(data[i]['spells'][3]['range_burn'])
        skill_4_image=data[i]['spells'][3]['image_url']
        
        name_temp=champ_name.replace(" ","_").replace("'","%27") #Convert champion name to correct format
        url=f'https://leagueoflegends.fandom.com/wiki/{name_temp}/LoL'
        driver.get(url)
        sleep(5)
        try:  
            nickname_elem=driver.find_element(By.CSS_SELECTOR,'.pi-data-value.pi-font')
            nickname=nickname_elem.text
        except NoSuchElementException as e:
            nickname='N/A'
            
        try:
            health_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="health"]')
            health=health_elem.find_elements(By.TAG_NAME,'span')[1].text
        except NoSuchElementException as e:
            health='N/A'
            
        try:
            healthRegen_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="health regen"]')
            healthRegen=healthRegen_elem.find_elements(By.TAG_NAME,'span')[1].text
        except NoSuchElementException as e:
            healthRegen='N/A'
            
        try:
            armor_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="armor"]')
            armor=armor_elem.find_elements(By.TAG_NAME,'span')[1].text
        except NoSuchElementException as e:
            armor='N/A'
            
        try:
            magicResist_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="mr"]')
            magicResist=magicResist_elem.find_elements(By.TAG_NAME,'span')[1].text
        except NoSuchElementException as e:
            magicResist='N/A'
            
        try:
            moveSpeed_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="ms"]')
            moveSpeed=moveSpeed_elem.find_elements(By.TAG_NAME,'span')[0].text
        except NoSuchElementException as e:
            moveSpeed='N/A'
            
        try:
            mana_elems=driver.find_elements(By.CSS_SELECTOR,'div[data-source="resource"]')
        except NoSuchElementException as e:
            e
        if mana_elems[1].find_elements(By.TAG_NAME,'span')==[]:
            mana='N/A'
        else:
           mana=mana_elems[1].find_elements(By.TAG_NAME,'span')[1].text    
           
        try:
            manaRegen_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="resource regen"]')
            manaRegen_check=manaRegen_elem.find_elements(By.TAG_NAME,'span')
        except NoSuchElementException as e:
            e 
        if len(manaRegen_check)==1:
            manaRegen=manaRegen_check[0].text
        elif len(manaRegen_check)==2:
            manaRegen=manaRegen_check[1].text
            
        try:
            atkDamage_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="attack damage"]')
            atkDamage=atkDamage_elem.find_elements(By.TAG_NAME,"span")[1].text
        except NoSuchElementException as e:
            atkDamage='N/A'
            
        try:    
            atkRange_elem=driver.find_element(By.CSS_SELECTOR,'div[data-source="range"]')
            atkRange=atkRange_elem.find_element(By.TAG_NAME,"span").text
        except NoSuchElementException as e:
            atkRange='N/A'
        
        champ_information.append(champ_name)
        champ_information.append(nickname)
        champ_information.append(champ_image)
        champ_information.append(health)
        champ_information.append(healthRegen)
        champ_information.append(mana)
        champ_information.append(manaRegen)
        champ_information.append(atkDamage)
        champ_information.append(atkRange)
        champ_information.append(armor)
        champ_information.append(magicResist)
        champ_information.append(moveSpeed)
        
        champ_information.append(passive)
        
        champ_information.append(skill_1)
        champ_information.append(skill_1_des)
        champ_information.append(cooldown_1)
        champ_information.append(cost_1)
        champ_information.append(range_1)
        champ_information.append(skill_1_image)
        
        champ_information.append(skill_2)
        champ_information.append(skill_2_des)
        champ_information.append(cooldown_2)
        champ_information.append(cost_2)
        champ_information.append(range_2)
        champ_information.append(skill_2_image)
        
        champ_information.append(skill_3)
        champ_information.append(skill_3_des)
        champ_information.append(cooldown_3)
        champ_information.append(cost_3)
        champ_information.append(range_3)
        champ_information.append(skill_3_image)
        
        champ_information.append(skill_4)
        champ_information.append(skill_4_des)
        champ_information.append(cooldown_4)
        champ_information.append(cost_4)
        champ_information.append(range_4)
        champ_information.append(skill_4_image)
        
        champs.append(champ_information)
    
    print('-----Retrieve all champions information successfully!!!-----')
    return champs
    
def Load_Champion_Information(champs):
    df=pd.DataFrame(data=champs,columns=['Champion name','Champion nickname','Champion image',
                                     'Health','Health regen (per 5s)','Mana','Mana regen (per 5s)','Attack damage','Attack range','Armor','Magic resist','Move speed',
                                     'Passive skill',
                                     'Skill 1','Description','Cooldown','Cost','Range','Skill 1 image',
                                     'Skill 2','Description','Cooldown','Cost','Range','Skill 2 image',
                                     'Skill 3','Description','Cooldown','Cost','Range','Skill 3 image',
                                     'Skill 4','Description','Cooldown','Cost','Range','Skill 4 image'])
    
    #DataFrame to MySQL
    df.to_excel('Champions information.xlsx')
    print('-----Insert all champions information to excel file successfully!!!-----')
    
    #DataFrame to MySQL
    mysql_engine=connect_MySQL()
    df.to_sql('lol_champions',con=mysql_engine,if_exists='append',index=False)
    print('-----Insert all champions information to MySQL successfully!!!-----')
    #DataFrame to AWS Redshift
    redshift_engine=connect_AWSRedshift()
    df.to_sql('lol_champions',con=redshift_engine,if_exists='append',index=False)
    print('-----Insert all champions information to AWS Redshift successfully!!!-----')
    
if __name__ == "__main__":
    start=time.time()
    url = "https://op.gg/api/v1.0/internal/bypass/meta/champions?hl=en_US"
    payload={ 
            
    }
    headers = {
    'authority': 'op.gg',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    'if-none-match': 'W/"1a7688-4EXDwhv77MGYD9umSmmUAy9rhgU"',
    'origin': 'https://www.op.gg',
    'referer': 'https://www.op.gg/',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-logging')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)

    champs=Get_Champion_Information()
    Load_Champion_Information(champs)
    end=time.time()-start
    print(f'Execute time: {end}')