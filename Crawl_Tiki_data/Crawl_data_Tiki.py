import pandas as pd
import requests
import json
import threading
from time import sleep
import time
from sqlalchemy import create_engine
import concurrent.futures

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

def Get_List_ID(url):     
    response=requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        print(f'-------Crawl page successfully!!!--------')
    for record in response.json().get('data'):
        product_list.append(record.get('id'))

def Get_Multi_Page():   
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(Get_List_ID,urls)

def Get_Product_Information(id):
    response=requests.get(f'https://tiki.vn/api/v2/products/{id}',headers=headers,params=params)
    text=response.content
    data=json.loads(text)

    master_=[]
    master_.append(data['id'])
    master_.append(data['name'])
    master_.append(data['categories']['name'])
    master_.append(data['brand']['name'])
    master_.append(data['current_seller']['id'])
    master_.append(data['current_seller']['name'])
    masterProduct.append(master_)
    
    for i in range(0,len(data['configurable_products'])):
        detail_=[]
        detail_.append(data['id'])
        detail_.append(int(data['configurable_products'][i]['sku']))
        detail_.append(data['configurable_products'][i]['option1'])
        detail_.append(data['configurable_products'][i]['price'])
        productDetail.append(detail_)

    try: 
        sold_item=data['all_time_quantity_sold']
    except Exception as e:
        sold_item=''
        
    marketing_=[]
    marketing_.append(data['id'])
    marketing_.append(data['review_count'])
    marketing_.append(data['rating_average'])
    marketing_.append(sold_item)
    Marketing.append(marketing_)

def Get_Multi_Product():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(Get_Product_Information,product_list)

def Create_DataFrame():
    if masterProduct is not None:
        if productDetail is not None and Marketing is not None:
            print('------Data is available-------')
            
    df_MasterProduct=pd.DataFrame(data=masterProduct,columns=['ID','Name','Category','Brand','Shop ID','Shop name'])
    df_ProductDetail=pd.DataFrame(data=productDetail,columns=['Product ID','SKU','Option','Price'])
    df_Marketing=pd.DataFrame(data=Marketing,columns=['Product ID','Count review','Average score','Sold items'])
    
    print('-------Crawl data successfully-------')
    # Dataframe to Excel 
    df_MasterProduct.to_excel('Master Product.xlsx')
    df_ProductDetail.to_excel('Product Detail.xlsx')
    df_Marketing.to_excel('Marketing.xlsx')
    
    #DataFrame to MySQL
    mysql_engine=connect_MySQL()
    df_MasterProduct.to_sql('master product',con=mysql_engine,if_exists='append',index=False)
    df_ProductDetail.to_sql('product detail',con=mysql_engine,if_exists='append',index=False)
    df_Marketing.to_sql('marketing',con=mysql_engine,if_exists='append',index=False)
    print('-------Insert data to MySQL successfully-------')
    
    #DataFrame to AWS Redshift
    redshift_engine=connect_AWSRedshift()
    df_MasterProduct.to_sql('master product',con=redshift_engine,if_exists='append',index=False)
    df_ProductDetail.to_sql('product detail',con=redshift_engine,if_exists='append',index=False)
    df_Marketing.to_sql('marketing',con=redshift_engine,if_exists='append',index=False)
    print('-------Insert data to AWS Redshift successfully-------')
    
    
if __name__ == "__main__":
    
    headers={
    'user-agent':'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,vi;q=0.8',
    }

    params={
        'limit': '40',
        'include': 'advertisement',
        'is_mweb': '1',
        'aggregations': '2',
        'q': 'điện thoại samsung',
    }
    urls=[]
    temp_url=f'https://tiki.vn/api/v2/products?limit=40&include=advertisement&aggregations=2&q=%C4%91i%E1%BB%87n+tho%E1%BA%A1i+samsung&page='
    for i in range(1,4):
        url=temp_url+str(i)
        urls.append(url)
        
    product_list=[]
    masterProduct=[]
    productDetail=[]
    Marketing=[]
    t1=time.time()
    Get_Multi_Page()
    Get_Multi_Product()
    Create_DataFrame()
    print('Executive time:',time.time()-t1)

    