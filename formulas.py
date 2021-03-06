def continue_calculation(amounts,accumulated_capital,accumulated_interest,x,total_fv,years,rate,escalation,escalate,monthly,m, capital,monthlyesc,max_contribution):
    remaining_years = years - x
    new_deposit = amounts[-1]
    for y in range(remaining_years + 1):
        y+=1 
        new_dep_fv = new_deposit*(1+(rate/m))**(y*m)
        new_ann_fv = max_contribution*(((1+rate/m)**(y*m)-1)/(rate/m))
        new_total_fv = new_ann_fv + new_dep_fv
        capital = capital + (max_contribution*m)
        interest = new_total_fv - capital
        new_total_fv = round(new_total_fv,2)
        amounts.append(new_total_fv)
        accumulated_capital.append(capital)
        accumulated_interest.append(interest)

def formatter(raw_number):
            return "{:,}".format(raw_number)