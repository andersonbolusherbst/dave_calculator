import streamlit as st
import pandas as pd
st.image("bayswaterlogo.png")

start_age = int(st.number_input('Enter your age when your begin contributing to your investment'))
retirement_age = int(st.number_input('Enter your retirement age'))
years = retirement_age - start_age
st.write("Your investment time horizon: ", years)
rate = st.slider('Select annual interest rate. 1% = 0.01',min_val=0, max_val=0.2)
escalate = st.selectbox("Select annual % increase of contribution",[0,0.02,0.05,0.1,0.15])
deposit = st.number_input('Starting Deposit')
monthly = st.number_input('Your Monthly Contribution')
m = st.selectbox("payments per year",[12,4,1])
pressed = st.button("Calculate")
if pressed:
    amounts = []
    year_string = []
    def calculate(years,rate,escalate,deposit,monthly,m):
  
        for x in range(years+1):
            x += 1
            dep_fv = deposit*(1+(rate/m))**(x*m)
            ann_fv = monthly*(((1+rate/m)**(x*m)-1)/(rate/m))
            total_fv = dep_fv + ann_fv
            amounts.append(total_fv)
            escalation = escalate+1
                
            monthly = monthly*escalation
            year_string.append(f" Year {x}")
            
    calculate(years,rate,escalation,deposit,monthly,m)
    st.balloons()
    final_data = pd.DataFrame(amounts,year_string)
    st.write(f" If you invest {monthly}, {m} times a year with an annual escalatin of {escalation}, your investment with generate {amounts[-1]} in {years} years")
    #st.dataframe(final_data)
    st.bar_chart(amounts)
    
