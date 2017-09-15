
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as bs
import pandas
from pandas import DataFrame
import datetime
from datetime import date, timedelta


# In[3]:


def homeshoppingmoaitems_crawler(url):
    
    res = requests.get(url)
    
    if res.status_code == 200:
        
        soup = bs(res.text,'html.parser')

        items = soup.select('div.식품·건강')

        table = []
        for item in items:
            row = []

            seller = item['class'][1]
            time = item.select('.font-12.c-midgray')
            time_live = item.select('.font-12.c-red')
            prod_name = item.select('.font-17')
            sub_prod_name = item.select('.font-14')
            live_prod_name = item.select('.font-18')
            a_price = item.select('s.c-gray ')
            live_a_price = item.select('s.c-gray.font-14')
            b_price = item.select('.strong.font-17.c-black')
            sub_b_price = item.select('.strong.font-14.c-black')
            live_b_price = item.select('.strong.font-18.c-black')
            url = item.select('.disblock')

            if len(time) > 0:
                row.append("".join(time[0].text.split()) if len(time) > 0 else "")
                row.append(seller.strip() if len(seller) > 0 else "")
                row.append(prod_name[0].text.strip() if len(prod_name) > 0 else "")
                row.append(a_price[0].text.strip() if len(a_price) > 0 else "")           
                row.append(b_price[0].text.strip() if len(b_price) > 0 else "")
                row.append("http://hsmoa.com"+url[0]['href'] if len(url) > 0 else "")
            
            elif url[0]['href'][:5] == "/live":
                row.append(time.live[0].text.strip() if len(time) > 0 else "")
                row.append(seller.strip() if len(seller) > 0 else "")
                row.append(live_prod_name[0].text.strip() if len(live_prod_name)>0 else "")
                row.append(live_a_price[0].text.strip() if len(live_a_price)>0 else "")
                row.append(live_b_price[0].text.strip() if len(live_b_price)>0 else "")
                row.append("http://hsmoa.com"+url[0]['href'] if len(url) > 0 else "")
                
            else:
                row.append("")
                row.append(seller.strip() if len(seller) > 0 else "")
                row.append(sub_prod_name[0].text.strip() if len(sub_prod_name) > 0 else "")
                row.append("")
                row.append(sub_b_price[0].text.strip() if len(sub_b_price) > 0 else "")
                row.append("http://hsmoa.com"+url[0]['href'] if len(url) > 0 else "")
                
            table.append(row)
            
    return table


# In[4]:


def select_date(url, n_date):
  
    n = datetime.date(int(n_date[:4]),int(n_date[4:6]), int(n_date[6:]))
    
    item_total = []
    
    for i in range(0, 7):
        d = n - timedelta(days=i)
        item_total += homeshoppingmoaitems_crawler(url.format(d.strftime('%Y%m%d')))
        
    return item_total


# In[5]:


def save_to_excel(url):
    n_date = input('원하는 날짜를 선택해주세요 yyyymmdd.(해당 날짜기준 과거 7일간의 판매상품 나열.)')    
    
    final_results = select_date(url, n_date)
    
    n2_date = datetime.date(int(n_date[:4]),int(n_date[4:6]), int(n_date[6:])) - timedelta(days=6)
    
    df_item_total = DataFrame(final_results)
    df_item_total.columns = ['판매시간','홈쇼핑채널','제품명','소비자가','판매가','url']
    df_item_total.to_excel('./'+n2_date.strftime('%Y%m%d')+'-'+n_date+'홈쇼핑모아리스트.xlsx')
    
    return df_item_total


# In[7]:


target_url = "http://hsmoa.com/schedule?date={0}&site=&cate=%EC%8B%9D%ED%92%88%C2%B7%EA%B1%B4%EA%B0%95"


save_to_excel(target_url)

