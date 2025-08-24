
balance = 5_000
interest = 0.24
monthly_payment = 120 + 50

count = 0
while balance > 0:
    monthly_interest = (interest/12) * balance
    principal = monthly_payment - monthly_interest
    balance -= principal
    count += 1
    print(f"Month {count} -- Payment ${monthly_payment:,.2f} -- Interest ${monthly_interest:,.2f} -- Principal ${principal:,.2f} -- Balance ${balance:,.2f}")
