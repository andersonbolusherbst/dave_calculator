def continue_calculation(amounts,accumulated_capital,accumulated_interest,x,total_fv,years,rate,escalation,escalate,monthly,m, capital,monthlyesc,max_contribution):
    remaining_years = years - x
    new_deposit = total_fv 
    for y in range(remaining_years):
        y+=1 
        new_dep_fv = new_deposit*(1+(rate/m))**(y*m)
        new_ann_fv = max_contribution*(((1+rate/m)**(1*m)-1)/(rate/m))
        new_total_fv = new_ann_fv + new_dep_fv
        capital = capital + (max_contribution*m)
        interest = new_total_fv - capital
        new_total_fv = round(new_total_fv,2)
        amounts.append(new_total_fv)
        accumulated_capital.append(capital)
        accumulated_interest.append(interest)
