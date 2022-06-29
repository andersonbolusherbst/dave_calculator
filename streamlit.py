import streamlit as st
import pandas as pd
from datetime import date
from currency_symbols import CurrencySymbols
import matplotlib.pyplot as plt
import matplotlib.image as image
from pandas.core.frame import DataFrame
import numpy as np
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from streamlit.components.v1 import iframe
import requests
import json

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")

st.image("bayswaterlogo.png")

currency_list=currency_list = ['ZAR','USD','EUR','GBP', 'HKD', 'JPY','CAD','CHF','NZD']

conv_currency_list = ['USD','EUR','GBP', 'HKD', 'JPY','CAD','CHF','NZD','ZAR']






col1, col2 = st.columns(2)

with col1:
    currency_selector = st.selectbox(
     'Which currency will you be investing with?',
     ('ZAR','USD','GBP','EUR','VND'))

    
    
with col2:
    conv_currency_selector = st.selectbox('Select target currency to convert to', conv_currency_list)
st.write("You're investing with:", currency_selector)    

col4,col5 = st.columns(2)   
with col4:
    start_age = st.number_input('Enter your starting age: ',value = 0)
    
with col5:
    retirement_age = st.number_input('Enter your retirement age: ', value = 0)
   
years = retirement_age - start_age
st.write("Your investment time horizon: ", years)

mnp= 0.01
mxp = 0.15
minp = f"{mnp:.0%}
maxp = f"{mxp:.0%}

rate = st.slider('Select annual interest rate',min_value=minp, max_value=maxp)
percentage = f"{rate:.0%}"
st.write("Your interest rate: ", percentage)
col3, col4 = st.columns(2)
with col3:
    deposit = st.number_input('Starting Deposit')
    m = st.selectbox("Payments per year",[12,4,1])
with col4:
    monthly = st.number_input('Your Monthly Contribution')
    escalate = float(st.selectbox("Select annual % increase of contribution",[0,0.02,0.05,0.1,0.15]))
escalation=0
max_contribution = st.number_input('Maximum Monthly Contribution:')
if max_contribution == 0:
    max_contribution = monthly
pressed = st.button("Calculate")
amounts=[]  

def calculate(years,rate,escalation,escalate,deposit,monthly,m):
    for x in range(years+1):
            x += 1
            dep_fv = deposit*(1+(rate/m))**(x*m)
            ann_fv = monthly*(((1+rate/m)**(x*m)-1)/(rate/m))
            total_fv = dep_fv + ann_fv
            total_fv = round(total_fv,2)
            amounts.append(total_fv)
            escalation = escalate+1
            if monthly >= max_contribution:
                monthly = max_contribution
            else:
                monthly = monthly*escalation
            year_string.append(f" Year {x}")
            
    return amounts

if pressed:
    
    year_string = []        
    calculate(years,rate,escalation,escalate,deposit,monthly,m)
    st.balloons()
   

    final_data = pd.DataFrame(amounts,year_string)
    final_data = final_data.T
    
   # st.header("Annuity Table")
    
    amounts_rounded = [round(num, 2) for num in amounts]
   # final_data = pd.DataFrame(amounts_rounded,year_string)
    #final_data = final_data.T
   # st.dataframe(final_data)
    
   # html = template.render(
    #   monthly=monthly,
       # currency_selector=currency_selector,
      #  escalation=escalation,
      #  m=m,
      #  years=years,
      #  escalate=escalate,
      #  rate=rate,
      #  deposit=deposit,
       # amounts=amounts,
      #  table=final_data,
      #  year_string=year_string,
      #  date=date.today().strftime("%B %d, %Y"),
      #  )

   # pdf = pdfkit.from_string(html, False)
   # st.balloons()

    #st.download_button(
   #     "⬇️ Download PDF",
   #     data=pdf,
   #     file_name="calculation.pdf",
   #     mime="application/octet-stream",
   #  )
   # st.download_button('Download file', st.bar_chart(amounts))
    
    
    #decimal_data = final_data.iloc[:, 0]
    #decimal_data = np.round(decimal_data, decimals = 2)
    
    
   

    # Retrieving currency data from ratesapi.io
    # https://api.ratesapi.io/api/latest?base=AUD&symbols=AUD
    base_price_unit = currency_selector   
    @st.cache
    def load_data():
        url = f'https://api.apilayer.com/exchangerates_data/convert?to={conv_currency_selector}&from={base_price_unit}&amount={amounts[-1]}'
        #url = 'https://api.apilayer.com/exchangerates_data/symbols'
        payload = {}
        headers= {
            "apikey": "WcqtBq92HnXahaiGoCV22XcgA8oY15pj"
          }
        
        response = requests.request("GET", url, headers=headers, data = payload)
       # status_code = response.status_code
        data = response.json()
        return data

    df = load_data()
    converted = df['result']
    converted= round(converted,2)

    st.header('Your Investment Value')
    st.write(f" If you invest **{monthly}** **{currency_selector}**, **{m}** times a year with an annual escalation of **{escalate}**, your investment will generate **{amounts[-1]}** **{currency_selector}** in **{years}** years.")
    st.write(f"The converted value of your investment is: **{converted}** **{conv_currency_selector}** at a rate of **{df['info']['rate']}** in **{years}** years.")

  
    st.bar_chart(amounts)

   



#url = "https://api.apilayer.com/exchangerates_data/convert?to={to}&from={from}&amount={amount}"



