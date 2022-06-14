import streamlit as st
import pandas as pd
st.image("bayswaterlogo.png")

start_age = st.number_input('Enter your age when your begin contributing to your investment')
retirement_age = st.number_input('Enter your retirement age')
years = retirement_age - start_age
rate = st.number_input('Annual interest rate. Use Decimals e.g 10% = 0.1')
escalation = st.number_input("Annual % increase of contribution")
deposit = st.number_input('Starting Deposit')
monthly = st.number_input('Your Monthly Contribution')
m = st.selectbox("payments per year",[12,4,1])
pressed = st.button("Calculate")
if pressed:
    amounts = []
    year_string = []
    def calculate(years,rate,escalation,deposit,monthly,m):
  
        for x in range(years+1):
            x += 1
            dep_fv = deposit*(1+(rate/m))**(x*m)
            ann_fv = monthly*(((1+rate/m)**(x*m)-1)/(rate/m))
            total_fv = dep_fv + ann_fv
            amounts.append(total_fv)
            if escalation == 0:
                escalation = 1
            else:
                escalation = escalation
                
            monthly = monthly*escalation
            year_string.append(f" Year {x}")
            
    calculate(years,rate,escalation,deposit,monthly,m)
    st.balloons()
    final_data = pd.DataFrame(amounts,year_string)
    st.dataframe(final_data)
    st.bar_chart(amounts)
