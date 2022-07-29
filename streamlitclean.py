#all the imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as image
from pandas.core.frame import DataFrame

import requests
import json
from email_tester import send_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl 
from formulas import continue_calculation,formatter
import altair as alt


#top image
st.image("thin.png")
#link back to website
st.write("Return to the bayswatercapital [website](https://bayswatercapital.co.za/)")
    
#lists and dictionaries we need
conv_currency_list = ['USD','EUR','GBP', 'HKD', 'JPY','CAD','CHF','NZD','ZAR']
escalate_dict ={'No Increase':0.0,'2.5%':0.025, '5%':0.05, '7.5%':0.075, '10%':0.1, '15%':0.15, '20%':0.2}
frequency ={'Monthly':12,'Quarterly':4,'Annual':1}
# layout of the actual app, all in one form 
# with lots of columns on top of each other


#first row of  two columns
col1row1, col2row1 = st.columns(2)
with col1row1: 
    start_age = st.number_input('Enter your starting age: ',value = 0)
with col2row1: 
    retirement_age = st.number_input('Enter your retirement age: ', value = 0)
    years = retirement_age-start_age
    

#2nd row of two columns
col1row2, col2row2 = st.columns(2)
with col1row2:
    st.markdown('##')
    st.write("Your investment time horizon: ", years)

with col2row2:
    per_year = st.selectbox("How many times would you like to contribute per year?",['Monthly', 'Quarterly', 'Annually'])
    m= frequency[per_year]

#3rd row of two columns
col1row3,col2row3 = st.columns(2)

with col1row3:
    rate = st.slider('Select annual growth rate',min_value=0.0, max_value=15.0, value=0.0, step=0.1,format="%f %%") 
    rate_converted = rate/100 # is this correct ?? 
with col2row3: 
    inflation = st.slider('Select expected inflation over the period',min_value=0.0, max_value=15.0, value=0.0, step=0.1,format="%f %%") 
#writing under row 3
st.write(f"You expect your investment to grow at a rate of **{round(rate,2)}%** but taking inflation into account the real return will be **{round(rate-inflation,2)}%**")

#4th row of two columns
col1row4,col2row4 =st.columns(2)
with col1row4:
    deposit = st.number_input('Starting Deposit (R): ',value=0,step=100)
with col2row4:
    monthly = st.number_input(f'Your {per_year}  Contribution (R): ',value=0,step=100)


#5th row of two columns
col1row5,col2row5 =st.columns(2)
with col1row5:
    escalatep = st.selectbox("Select annual % increase of contribution",['No Increase','2.5%','5%','7.5%','10%','15%','20%'])
with col2row5:
    conv_currency_selector = st.selectbox('Select target currency to convert to', conv_currency_list)

#6th row of two columns
col1row6,col2row6 = st.columns(2)
with col1row6:
    cap_contribution = st.radio("Would you like to cap your contribution?",['No',f'Yes - set a {per_year} cap', 'Yes - set an Annual cap'])
    max_contribution= 0
with col2row6:
    if cap_contribution == f"Yes - set a {per_year} cap":
        max_contribution = st.number_input(f'Maximum {per_year} Contribution: ',value =0)
    elif cap_contribution == "Yes - set an annual cap":
        max_annual_contribution = st.number_input('Maximum Annual Contribution: ',value=0)
        max_contribution = max_annual_contribution/m  


#7th row of two columns
col1row7,col2row7 =st.columns(2)
with col1row7:
    email_choice = st.radio("Would you like to send info to your email address?",["No","Yes"])
    
with col2row7:
    if email_choice == "Yes":
        client_name = st.text_input("Name: ")
        email_address = st.text_input("email address to send to: ")
    
        

    

escalate = float(escalate_dict[escalatep]) # fetch the correct format from the dictionary
escalation=0 # set to zero for the for loop

  
if max_contribution == 0:
    max_contribution = 1000000000000
else:
    max_contribution = max_contribution

pressed = st.button("Calculate")
amounts=[]
growth_rate = rate_converted
rate =growth_rate # HEY ? 
accumulated_capital=[]
accumulated_interest=[]
capital = 0
monthlyesc = monthly

def calculate(years,rate,escalation,escalate,deposit,monthly,m, capital,monthlyesc):
    for x in range(years):
        x += 1
        if rate == escalate:
            ann_fv = monthly*(m*x)*(1+(rate/m))**((x*m)-1)
            dep_fv = deposit*(1+(rate/m))**(x*m)
        else:
            ann_fv = monthly *(((1+(rate/m))**(x*m)-(1+(escalate/m))**(x*m))/((rate/m)-(escalate/m)))
            dep_fv = deposit*(1+(rate/m))**(x*m)
            
        total_fv = dep_fv + ann_fv
        escalation = escalate+1
        
        
        if monthlyesc > max_contribution:
            monthlyesc = max_contribution
            continue_calculation(amounts,accumulated_capital,accumulated_interest,x,total_fv,years,rate,escalation,escalate,monthly,m, capital,monthlyesc,max_contribution)
            break
        else:
            monthlyesc = monthlyesc
            
        if x == 1:
            capital = deposit + (monthly*m)
            monthlyesc = monthlyesc * escalation
        else:
            capital = capital + (monthlyesc*m)
            monthlyesc = monthlyesc * escalation
            
        interest = total_fv - capital
        total_fv = round(total_fv,2)
        amounts.append(total_fv)
        accumulated_capital.append(capital)
        accumulated_interest.append(interest)
        
            
    return amounts,accumulated_capital,accumulated_interest


if pressed:
    
    if monthly == 0:
        st.error("please input in your contribution amount")
    elif retirement_age == 0 or years < 1:
        st.error("please input correct retirement and starting age")
    else:
        calculate(years,rate,escalation,escalate,deposit,monthly,m,capital,monthlyesc)
        st.balloons()
        
        

        amounts_rounded = [round(num, 2) for num in amounts]
        acc_cap = [round(num, 2) for num in accumulated_capital]
        acc_int = [round(num, 2) for num in accumulated_interest]

        final_data = pd.DataFrame(list(zip(acc_cap, acc_int,amounts_rounded,range(1,len(amounts_rounded)))),columns=['Capital Contribution','Investment Growth','Total','year_index'])
        
        base_price_unit = "ZAR"   
        
        def load_data():
            url = f'https://api.apilayer.com/exchangerates_data/convert?to={conv_currency_selector}&from={base_price_unit}&amount={amounts[-1]}'
            
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
        converted = formatter(converted)
        ireturn = (acc_int[-1]/acc_cap[-1])
        ireturn = f"{ireturn:.0%}"
        
        # convert all of them to nice looking numbers e.g 1000000 => 100,000
        monthly = formatter(monthly)
        deposit = formatter(deposit)
        final_amount = formatter(amounts[-1])
        final_interest = formatter(acc_int[-1])
        final_cap = formatter(acc_cap[-1])
        
        # make growth rate nicer to read
        display_rate = round(growth_rate*100,1)

        st.header('Your Investment Value')
        st.write(f" If you desposit **R{deposit}** and contribute **R{monthly}**,  **{m}** times a year with an annual escalation of **{escalatep}**,  at a growth rate of **{display_rate}%**, your investment will generate **R{final_amount}**  in **{years}** years.")
        st.write(f"The converted value of your investment is:  **{conv_currency_selector}** **{converted}** at a rate of **{df['info']['rate']}** ")
        st.write(f" You will earn earn **R{final_interest}**  on your capital contribution of **R{final_cap}**  which is a return of **{ireturn}**")


        stacked_bar = final_data[['Investment Growth','Capital Contribution','year_index']]
        new_stacked = stacked_bar.melt('year_index', var_name='Key', value_name='Amount')
        
        # write the new bar chart here
        
        Key_dict = {
                'Capital Contribution': "#DDC385", 
                'Investment Growth': "#0D1A34", 
    
                            }

        new_stacked['Color'] = new_stacked['Key'].map(Key_dict)

        domain = ['Capital Contribution','Investment Growth']
        range_ = ["#DDC385","#0D1A34"]
        
        c = alt.Chart(new_stacked).mark_bar().encode(
            x='year_index:O',
            y='Amount',
            tooltip= ["Key","Amount"],
            color=alt.Color('Key',scale=alt.Scale(domain=domain,range=range_),sort = 'ascending')
            )
        st.altair_chart(c,use_container_width=True)
        
        
        ##Test
        #c.save("chart.json")
        
        
        if email_choice =="Yes":
            send_email(st.secrets["email_secret"]["password"][0],monthly,m,escalation,final_amount,years,escalatep,deposit,final_interest,final_cap,ireturn,converted,df,conv_currency_selector,display_rate,email_address,client_name,max_contribution)
            # 


