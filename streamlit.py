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
from email_tester import send_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl 

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")

st.image("bayswaterlogo.png")

currency_list=currency_list = ['ZAR','USD','EUR','GBP', 'HKD', 'JPY','CAD','CHF','NZD']

conv_currency_list = ['USD','EUR','GBP', 'HKD', 'JPY','CAD','CHF','NZD','ZAR']

rates = {'1%':0.01,'2%':0.02,'3%':0.03,'4%':0.04,'5%':0.05,'6%':0.06,'7%':0.07,'8%':0.08,'9%':0.09,'10%':0.1}
escalates ={'0%':0.0,'2.5%':0.025, '5%':0.05, '7.5%':0.075, '10%':0.1, '15%':0.15, '20%':0.2}




col1, col2 = st.columns(2)

with col1:
    currency_selector = st.selectbox(
     'Which currency will you be investing with?',
     ('ZAR','USD','GBP','EUR','VND'))

    
    
with col2:
    conv_currency_selector = st.selectbox('Select target currency to convert to', conv_currency_list)
st.write("You're investing with:", currency_selector)  
rate = st.selectbox('Select annual growth rate', ['1%','2%','3%','4%','5%','6%','7%','8%','9%','10%'])

col4,col5 = st.columns(2)   
with col4:
    start_age = st.number_input('Enter your starting age: ',value = 0)
    
    
with col5:
    retirement_age = st.number_input('Enter your retirement age: ', value = 0)
    
   
years = retirement_age - start_age
st.write("Your investment time horizon: ", years)


#rate = st.slider('Select annual growth rate',min_value=0.01, max_value=0.15)

#percentage = f"{rate:.0%}"

col3, col4 = st.columns(2)
with col3:
    deposit = st.number_input('Starting Deposit')
    max_contribution = st.number_input('Maximum Monthly Contribution:')
    
    
with col4:
    monthly = st.number_input('Your Contribution')
    escalatep = st.selectbox("Select annual % increase of contribution",['0%','2.5%','5%','7.5%','10%','15%','20%'])
escalate = float(escalates[escalatep])

m = st.selectbox("How many times would you like to contribute per year?",[12, 4, 1])
                                                                          
                                                                          
escalation=0

if max_contribution == 0:
    max_contribution = monthly
pressed = st.button("Calculate")
amounts=[]
rate =rates[rate]
accumulated_capital=[]
accumulated_interest=[]
capital = 0

def calculate(years,rate,escalation,escalate,deposit,monthly,m, capital):
    for x in range(years+1):
            x += 1
            dep_fv = deposit*(1+(rate/m))**(x*m)
            ann_fv = monthly*(((1+rate/m)**(x*m)-1)/(rate/m))
            if x == 1:
                capital = deposit + (monthly*m)
            else:
                capital = (monthly*m)+capital
            total_fv = dep_fv + ann_fv
            interest = total_fv - capital
            total_fv = round(total_fv,2)
            amounts.append(total_fv)
            accumulated_capital.append(capital)
            accumulated_interest.append(interest)
            escalation = escalate+1
            monthly = monthly*escalation
            if monthly >= max_contribution:
                monthly = max_contribution
            else:
                monthly = monthly*escalation
            year_string.append(f" Year {x}")
            
    return amounts,accumulated_capital,accumulated_interest


if pressed:
    #@st.cache
    year_string = []
    if monthly == 0:
        st.error("please input in your contribution amount")
    else:
        calculate(years,rate,escalation,escalate,deposit,monthly,m,capital)
        st.balloons()
        
        st.header("Annuity Table")

        amounts_rounded = [round(num, 2) for num in amounts]
        acc_cap = [round(num, 2) for num in accumulated_capital]
        acc_int = [round(num, 2) for num in accumulated_interest]

        final_data = pd.DataFrame(list(zip(acc_cap, acc_int,amounts_rounded)),columns=['Capital','Interest','Total'])
        #final_data = final_data.T
        st.dataframe(final_data)
        # Retrieving currency data from ratesapi.io
        # https://api.ratesapi.io/api/latest?base=AUD&symbols=AUD
        base_price_unit = currency_selector   
        #@st.cache
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
        ireturn = (acc_int[-1]/acc_cap[-1])*100
        #ireturn = f"{ireturn:%}"

        st.header('Your Investment Value')
        st.write(f" If you invest **{monthly}** **{currency_selector}** at an annual return of **{rate}**, **{m}** times a year with an annual escalation of **{escalatep}**, your investment will generate **{amounts[-1]}** **{currency_selector}** in **{years}** years.")
        st.write(f"The converted value of your investment is: **{converted}** **{conv_currency_selector}** at a rate of **{df['info']['rate']}** in **{years}** years.")
        st.write(f" You will earn earn **{acc_int[-1]}** on your capital contribution of **{acc_cap[-1]}** which is a return of **{ireturn}**")


        stacked_bar = final_data[['Capital','Interest',]]
        st.bar_chart(stacked_bar)
        
#         html = template.render(
#             monthly=monthly,
#             currency_selector=currency_selector,
#             escalation=escalation,
#             m=m,
#             years=years,
#             escalate=escalate,
#             rate=rate,
#             deposit=deposit,
#             amounts=amounts,
#             year_string=year_string,
#             date=date.today().strftime("%B %d, %Y"),
#             )

#         pdf = pdfkit.from_string(html, False)
#         st.balloons()

#         st.download_button(
#             "⬇️ Download PDF",
#             data=pdf,
#             file_name="calculation.pdf",
#             mime="application/octet-stream",
#          )
        


        #decimal_data = final_data.iloc[:, 0]
        #decimal_data = np.round(decimal_data, decimals = 2)
                   

            
    
    
        



