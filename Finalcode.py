#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import random
import json
from lxml.html import fromstring
import requests

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2",
    "Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; cs; rv:1.9.0.8) Gecko/2009032609 Firefox/3.0.8",
    "Mozilla/5.0 (X11; U; OpenBSD i386; en-US; rv:1.8.0.5) Gecko/20060819 Firefox/1.5.0.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3",
    "Mozilla/5.0 (Windows; U; WinNT4.0; en-US; rv:1.7.9) Gecko/20050711 Firefox/1.0.6",
    "Mozilla/5.0 (Windows; Windows NT 6.1; rv:2.0b2) Gecko/20100720 Firefox/4.0b2",
    "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b4) Gecko/20100818 Firefox/4.0b4",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2) Gecko/20100308 Ubuntu/10.04 (lucid) Firefox/3.6 GTB7.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b7) Gecko/20101111 Firefox/4.0b7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b8pre) Gecko/20101114 Firefox/4.0b8pre",
    "Mozilla/5.0 (X11; Linux x86_64; rv:2.0b9pre) Gecko/20110111 Firefox/4.0b9pre",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b9pre) Gecko/20101228 Firefox/4.0b9pre",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.2a1pre) Gecko/20110324 Firefox/4.2a1pre",
    "Mozilla/5.0 (X11; U; Linux amd64; rv:5.0) Gecko/20100101 Firefox/5.0 (Debian)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0a2) Gecko/20110613 Firefox/6.0a2",
    "Mozilla/5.0 (X11; Linux i686 on x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
    "Mozilla/5.0 (X11; Ubuntu; Linux armv7l; rv:17.0) Gecko/20100101 Firefox/17.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0",
    "Mozilla/5.0 (X11; Linux i686; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.36 Safari/525.19",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.4 (KHTML, like Gecko) Chrome/6.0.481.0 Safari/534.4",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US) AppleWebKit/533.4 (KHTML, like Gecko) Chrome/5.0.375.86 Safari/533.4",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.2 (KHTML, like Gecko) Chrome/4.0.223.3 Safari/532.2",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.201.1 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.27 Safari/532.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/530.5 (KHTML, like Gecko) Chrome/2.0.173.1 Safari/530.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.558.0 Safari/534.10",
    "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML,like Gecko) Chrome/9.1.0.0 Safari/540.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.600.0 Safari/534.14",
    "Mozilla/5.0 (X11; U; Windows NT 6; en-US) AppleWebKit/534.12 (KHTML, like Gecko) Chrome/9.0.587.0 Safari/534.12",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.792.0 Safari/535.1",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.45 Safari/535.19",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
]

n=0
#step 1/5 - change file path 
filepath='/Users/siyingsmac/Desktop/FinanceSpyder/Investing ticker pool.xlsx'
#step 2/5 - change sheet name
sheet = pd.read_excel(filepath, sheet_name='To Use')
#step 3/5 - change column name to list of id
idlist=list(sheet['pid'])

listprint=pd.DataFrame()


for i in idlist:
    try:
        pid=str(int(i))
        n=n+1
        headers = {"User-Agent": random.choice(USER_AGENTS),
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "text/html",
                    "Accept-Encoding": "gzip, deflate",
                    "Connection": "keep-alive",
                    }
        params1 = {
            "action": "change_report_type",
            "pair_ID": pid,
            "report_type": 'BAL',
            "period_type": "Annual"
        }

        params2 = {
            "action": "change_report_type",
            "pair_ID": pid,
            "report_type": 'INC',
            "period_type": "Annual"
        }
        params3 = {

            "pair_ID": pid,

        }

        data = {
            'Company id':list(),
            'Cash and Short Term Investments':list(),
            'Total Receivables, Net':list(),
            'Total Inventory':list(),
            'Total Current Assets':list(),
            'Goodwill, Net':list(),
            'Intangibles, Net':list(),
            'Total Assets':list(),
            'Notes Payable/Short Term Debt':list(),
            'Current Port. of LT Debt/Capital Leases':list(),
            'Total Current Liabilities':list(),
            'Total Liabilities':list(),
            'Total Long Term Debt':list(),
            'Minority Interest':list(),
            'Redeemable Preferred Stock, Total':list(),
            'Preferred Stock - Non Redeemable, Net':list(),
            'Total Equity':list(),
            'Total Revenue':list(),
            'Gross Profit':list(),
            'Operating Income':list(),
            'Net Income':list(),
            'Share Price':list(),     
            'Shares Outstanding':list(),
            }
        url = 'https://www.investing.com/instruments/Financials/changereporttypeajax'


        try:
            #balence Sheet
            req1 = requests.get(url, params=params1, headers=headers)
            root1 = fromstring(req1.text)
            tables1 = root1.xpath(".//div/table[contains(@class, 'genTbl reportTbl')]") #breakdown row 
            tables2= root1.xpath(".//tr[contains(@class, 'openTr pointer')]")  #summary row

            data['Company id'].append(pid)

            Cash_and_Short_Term_Investments=tables1[0].xpath(".//tbody")[0].xpath(".//tr")[0].text_content().splitlines()[2]
            data['Cash and Short Term Investments'].append(Cash_and_Short_Term_Investments)

            Total_Receivables_Net=tables1[0].xpath(".//tbody")[0].xpath(".//tr")[4].text_content().splitlines()[2]
            data['Total Receivables, Net'].append(Total_Receivables_Net)

            Total_Inventory=tables1[0].xpath(".//tbody")[0].xpath(".//tr")[6].text_content().splitlines()[2]
            data['Total Inventory'].append(Total_Inventory)

            Total_Current_Asset=tables2[0].text_content().splitlines()[2]
            data['Total Current Assets'].append(Total_Current_Asset)

            total_assets=tables2[1].text_content().splitlines()[2]
            data['Total Assets'].append(total_assets)

            Total_Current_Liabilities=tables2[2].text_content().splitlines()[2]
            data['Total Current Liabilities'].append(Total_Current_Liabilities)

            Total_Liabilities=tables2[3].text_content().splitlines()[2]
            data['Total Liabilities'].append(Total_Liabilities)

            Total_Equity=tables2[4].text_content().splitlines()[2]
            data['Total Equity'].append(Total_Equity)

            Goodwill_Net=tables1[1].xpath(".//tbody")[0].xpath(".//tr")[3].text_content().splitlines()[2]
            data['Goodwill, Net'].append(Goodwill_Net)

            Intangibles_Net=tables1[1].xpath(".//tbody")[0].xpath(".//tr")[4].text_content().splitlines()[2]
            data['Intangibles, Net'].append(Intangibles_Net)

            Notes_Payable_Short_Term_Debt=tables1[2].xpath(".//tbody")[0].xpath(".//tr")[3].text_content().splitlines()[2]
            data['Notes Payable/Short Term Debt'].append(Notes_Payable_Short_Term_Debt)

            Current_Port=tables1[2].xpath(".//tbody")[0].xpath(".//tr")[4].text_content().splitlines()[2]
            data['Current Port. of LT Debt/Capital Leases'].append(Current_Port)

            Total_Long_Term_debt=tables1[3].xpath(".//tbody")[0].xpath(".//tr")[0].text_content().splitlines()[2]
            data['Total Long Term Debt'].append(Total_Long_Term_debt)

            Minority_Interest=tables1[3].xpath(".//tbody")[0].xpath(".//tr")[4].text_content().splitlines()[2]
            data['Minority Interest'].append(Minority_Interest)

            Redeemable_Preferred_Stock_Total=tables1[4].xpath(".//tbody")[0].xpath(".//tr")[0].text_content().splitlines()[2]
            data['Redeemable Preferred Stock, Total'].append(Redeemable_Preferred_Stock_Total)

            Preferred_Stock=tables1[4].xpath(".//tbody")[0].xpath(".//tr")[1].text_content().splitlines()[2]
            data['Preferred Stock - Non Redeemable, Net'].append(Preferred_Stock)

        except: 
            print (n,pid,"BAL Error")
            pass


        try:
            #Income Statement
            req2 = requests.get(url, params=params2, headers=headers)
            root2 = fromstring(req2.text)
            tables3 = root2.xpath(".//tr[contains(@class, 'openTr pointer')]") #summary row 
            tables4 = root2.xpath(".//tr/td") #breakdown row 

            Total_Revenue=tables3[0].text_content().splitlines()[2]
            data['Total Revenue'].append(Total_Revenue)

            Gross_Profit=tables4[22].text_content()
            data['Gross Profit'].append(Gross_Profit)

            Operating_Income=tables4[63].text_content()
            data['Operating Income'].append(Operating_Income)

            Net_Income=tables4[123].text_content()
            data['Net Income'].append(Net_Income)

        except: 
            print (n,pid,"INC Error")
            pass

        try:
#step 4/5- change the column name for tags
            tag=sheet.loc[(sheet['pid'] == i).idxmax(), 'tag']
            url1='https://www.investing.com/equities/'+str(tag)   

            req3 = requests.get(url1,headers=headers)
            root3 = fromstring(req3.text)
            tables5 = root3.xpath(".//div/span[contains(@class, 'instrument-price_last__KQzyA')]")
        except: 
            print (n,pid,"Summury link Error")
            pass
        
        try:
            Share_Price=tables5[0].text_content()
            data['Share Price'].append(Share_Price)
        except: 
            print (n,pid,"Shareprice Error")
            pass
        
        
        try:
            tables6 = root3.xpath(".//div[contains(@class, 'flex justify-between border-b py-2 desktop:py-0.5')]")

            Shares_Outstanding=tables6[13].text_content()[18:] 
            data['Shares Outstanding'].append(Shares_Outstanding)


        except: 
            print (n,pid,"shares outstanding Error")
            pass


        try:
            dataset = pd.DataFrame(data)
            listprint=pd.concat([listprint,dataset])
            print(n,'done')

        except:
            pass
    except:
        print (n,"ID Missing")
        pass

#step 5/5 - change target path
listprint.to_excel("/Users/siyingsmac/Desktop/output.xlsx")

