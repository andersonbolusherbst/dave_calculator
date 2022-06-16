import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
from currency_symbols import CurrencySymbols
import matplotlib.pyplot as plt
import matplotlib.image as image
from pandas.core.frame import DataFrame
import numpy as np
import pdfkit
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from streamlit.components.v1 import iframe

env = Environment(loader=FileSystemLoader("."), autoescape=select_autoescape())
template = env.get_template("template.html")

st.image("bayswaterlogo.png")

### Dont worry just currency work in progress
currency_list = {
    'ALL': 'Albania Lek',
    'AFN': 'Afghanistan Afghani',
    'ARS': 'Argentina Peso',
    'AWG': 'Aruba Guilder',
    'AUD': 'Australia Dollar',
    'AZN': 'Azerbaijan New Manat',
    'BSD': 'Bahamas Dollar',
    'BBD': 'Barbados Dollar',
    'BDT': 'Bangladeshi taka',
    'BYR': 'Belarus Ruble',
    'BZD': 'Belize Dollar',
    'BMD': 'Bermuda Dollar',
    'BOB': 'Bolivia Boliviano',
    'BAM': 'Bosnia and Herzegovina Convertible Marka',
    'BWP': 'Botswana Pula',
    'BGN': 'Bulgaria Lev',
    'BRL': 'Brazil Real',
    'BND': 'Brunei Darussalam Dollar',
    'KHR': 'Cambodia Riel',
    'CAD': 'Canada Dollar',
    'KYD': 'Cayman Islands Dollar',
    'CLP': 'Chile Peso',
    'CNY': 'China Yuan Renminbi',
    'COP': 'Colombia Peso',
    'CRC': 'Costa Rica Colon',
    'HRK': 'Croatia Kuna',
    'CUP': 'Cuba Peso',
    'CZK': 'Czech Republic Koruna',
    'DKK': 'Denmark Krone',
    'DOP': 'Dominican Republic Peso',
    'XCD': 'East Caribbean Dollar',
    'EGP': 'Egypt Pound',
    'SVC': 'El Salvador Colon',
    'EEK': 'Estonia Kroon',
    'EUR': 'Euro Member Countries',
    'FKP': 'Falkland Islands (Malvinas) Pound',
    'FJD': 'Fiji Dollar',
    'GHC': 'Ghana Cedis',
    'GIP': 'Gibraltar Pound',
    'GTQ': 'Guatemala Quetzal',
    'GGP': 'Guernsey Pound',
    'GYD': 'Guyana Dollar',
    'HNL': 'Honduras Lempira',
    'HKD': 'Hong Kong Dollar',
    'HUF': 'Hungary Forint',
    'ISK': 'Iceland Krona',
    'INR': 'India Rupee',
    'IDR': 'Indonesia Rupiah',
    'IRR': 'Iran Rial',
    'IMP': 'Isle of Man Pound',
    'ILS': 'Israel Shekel',
    'JMD': 'Jamaica Dollar',
    'JPY': 'Japan Yen',
    'JEP': 'Jersey Pound',
    'KZT': 'Kazakhstan Tenge',
    'KPW': 'Korea (North) Won',
    'KRW': 'Korea (South) Won',
    'KGS': 'Kyrgyzstan Som',
    'LAK': 'Laos Kip',
    'LVL': 'Latvia Lat',
    'LBP': 'Lebanon Pound',
    'LRD': 'Liberia Dollar',
    'LTL': 'Lithuania Litas',
    'MKD': 'Macedonia Denar',
    'MYR': 'Malaysia Ringgit',
    'MUR': 'Mauritius Rupee',
    'MXN': 'Mexico Peso',
    'MNT': 'Mongolia Tughrik',
    'MZN': 'Mozambique Metical',
    'NAD': 'Namibia Dollar',
    'NPR': 'Nepal Rupee',
    'ANG': 'Netherlands Antilles Guilder',
    'NZD': 'New Zealand Dollar',
    'NIO': 'Nicaragua Cordoba',
    'NGN': 'Nigeria Naira',
    'NOK': 'Norway Krone',
    'OMR': 'Oman Rial',
    'PKR': 'Pakistan Rupee',
    'PAB': 'Panama Balboa',
    'PYG': 'Paraguay Guarani',
    'PEN': 'Peru Nuevo Sol',
    'PHP': 'Philippines Peso',
    'PLN': 'Poland Zloty',
    'QAR': 'Qatar Riyal',
    'RON': 'Romania New Leu',
    'RUB': 'Russia Ruble',
    'SHP': 'Saint Helena Pound',
    'SAR': 'Saudi Arabia Riyal',
    'RSD': 'Serbia Dinar',
    'SCR': 'Seychelles Rupee',
    'SGD': 'Singapore Dollar',
    'SBD': 'Solomon Islands Dollar',
    'SOS': 'Somalia Shilling',
    'ZAR': 'South Africa Rand',
    'LKR': 'Sri Lanka Rupee',
    'SEK': 'Sweden Krona',
    'CHF': 'Switzerland Franc',
    'SRD': 'Suriname Dollar',
    'SYP': 'Syria Pound',
    'TWD': 'Taiwan New Dollar',
    'THB': 'Thailand Baht',
    'TTD': 'Trinidad and Tobago Dollar',
    'TRY': 'Turkey Lira',
    'TRL': 'Turkey Lira',
    'TVD': 'Tuvalu Dollar',
    'UAH': 'Ukraine Hryvna',
    'GBP': 'United Kingdom Pound',
    'USD': 'United States Dollar',
    'UYU': 'Uruguay Peso',
    'UZS': 'Uzbekistan Som',
    'VEF': 'Venezuela Bolivar',
    'VND': 'Viet Nam Dong',
    'YER': 'Yemen Rial',
    'ZWD': 'Zimbabwe Dollar'
}

currency_selector = st.selectbox(
     'Which currency will you be investing with?',
     ('ZAR','USD','GBP','EUR','VND'))
    
st.write('You selected:', currency_selector)

### Brad Playground

dollarSymbol = CurrencySymbols.get_symbol('USD')
euroSymbol = CurrencySymbols.get_symbol('EUR')
britishPoundSymbol = CurrencySymbols.get_symbol('GBP')
#randSymbol = CurrencySymbols.get_symbol('ZAR')
#randSymbol = CurrencySymbols.get_symbol('ZAR')





start_age = st.number_input('Enter your age when your begin contributing to your investment',value = 0)
retirement_age = st.number_input('Enter your retirement age', value = 0)
years = retirement_age - start_age
st.write("Your investment time horizon: ", years)
rate = st.slider('Select annual interest rate',min_value=0.00, max_value=0.15)
escalate = float(st.selectbox("Select annual % increase of contribution",[0,0.02,0.05,0.1,0.15]))
escalation=0
deposit = st.number_input('Starting Deposit')
monthly = st.number_input('Your Monthly Contribution')
m = st.selectbox("payments per year",[12,4,1])
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
            monthly = monthly*escalation
            year_string.append(f" Year {x}")
            
    return amounts

if pressed:
    
    year_string = []        
    calculate(years,rate,escalation,escalate,deposit,monthly,m)
    st.balloons()
   
#if currency_selector == "USD":
   #currency_selector = dollarSymbol
#elif currency_selector == "GBP":
   #currency_selector = britishPoundSymbol
#elif currency_selector == "EUR":
   #currency_selector = euroSymbol
#else: 
   #pass

    final_data = pd.DataFrame(amounts,year_string)
    final_data = final_data.T
    st.write(f" If you invest **{monthly}** {currency_selector}, **{m}** times a year with an annual escalation of **{escalation}**, your investment will generate **{amounts[-1]}** **{currency_selector}** in **{years}** years")

    #col1, col2 = st.columns([1, 3])

    #with col1:
    st.header("Yearly Projections")
    plt.rcParams["figure.figsize"] = (len(year_string), len(amounts))
    #plt.rcParams["figure.figsize"] = (20,3)
    #plt.rcParams["figure.autolayout"] = True

    #im = image.imread("bayswaterlogo.png")
    #imS = cv2.resize(im, (960, 540))
    
    fig, ax = plt.subplots()
    plotdata = pd.DataFrame(list(zip(year_string, amounts)), columns =["Year", "Amount"])
    
    font = {'family': 'serif',
        'color':  'darkblue',
        'weight': 'normal',
        'size': 40,
        }

    #fig.figimage(im, xo = 90, yo = 690, zorder=2, alpha=1)

    ax.bar(plotdata["Year"], plotdata["Amount"], color='lightblue')
    ax.plot(plotdata["Year"], plotdata["Amount"], color='darkblue', ms=10)
    
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax.get_yticklabels(), visible=False)
    ax.tick_params(axis='both', which='both', length=0)

    
    #plt.tick_params(
    #axis='x',          
    #which='both',      
    #bottom=False,      
    #top=False,         
    #labelbottom=False)
    
    #plt.tick_params(
    #axis='y',          
    #which='both',      
    #bottom=False,      
    #top=False,         
    #labelbottom=False)
    
    ax.set_xlabel('Years in Plan', fontdict = font)
    ax.set_ylabel('Annuity Amount', fontdict = font)

    st.pyplot(fig,ax)
    
    #st.line_chart(amounts)

    #with col2:
    st.header("Annuity Table")
    
    amounts_rounded = [round(num, 2) for num in amounts]
    final_data = pd.DataFrame(amounts_rounded,year_string)
    final_data = final_data.T
    st.dataframe(final_data)
    
    html = template.render(
        monthly=monthly,
        currency_selector=currency_selector,
        escalation=escalation,
        m=m,
        years=years,
        escalate=escalate,
        rate=rate,
        deposit=deposit,
        amounts=amounts,
        table=final_data,
        year_string=year_string,
        date=date.today().strftime("%B %d, %Y"),
        )

    pdf = pdfkit.from_string(html, False)
    st.balloons()

    st.download_button(
        "⬇️ Download PDF",
        data=pdf,
        file_name="calculation.pdf",
        mime="application/octet-stream",
     )
    
    
    
    #decimal_data = final_data.iloc[:, 0]
    #decimal_data = np.round(decimal_data, decimals = 2)
    
   

