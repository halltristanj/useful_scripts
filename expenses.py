import sys
import pandas as pd
import numpy as np
import datetime

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def to_date(df):
    df['date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', exact=True)
    dfb = df[df.date.isnull()]
    dfb['date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', exact=True)
    df.update(dfb)
    del dfb

    df['ym'] = pd.to_datetime(df['date']).map(lambda dt: dt.replace(day=1))

    df.to_csv('transactions_dated.csv', index=False)
    return df

def override(df):
    # These values override all others
    over = {
        'Student Loan': 524.6,
        'Internet': 54.99,
        'Mobile Phone': 45,
        'Bank Fee': 59,  # Captial One Membership
        'Payment': 125,
        'Tuition': 470,
    }

    for key, val in over.items():
        df.loc[key] = -val #,'transaction'] = -val

    return df


def etl(df):
    # These are okay:
    #   Auto Insurance
    #   Home Insurance
    #   Finance Charge
    #   Pharmacy

    # Drop some shit here
    df['drop'] = False
    df.loc[(df['Category'] == 'Credit Card Payment') & (df['Transaction Type'] == 'credit'), 'drop'] = True
    df.loc[(df['Category'] == 'Transfer'), 'drop'] = True

    # keep only Marquis
    df.loc[(df['Category'] == 'Mortgage & Rent') & (~df['Description'].str.contains('Marquis')), 'drop'] = True
    df.loc[(df['Category'] == 'Mortgage & Rent') & (df['Description'].str.contains('Marquis')) & (df['Amount'] == 280), 'drop'] = True

    # Remove Tall Utils
    df.loc[(df['Description'].str.match('Tall Util Des')), 'drop'] = True

    # Gas & Fuel < $10 is probably not gas and or fuel (snacks)
    df.loc[(df['Category'] == 'Gas & Fuel') & (df['Amount'] < 10), 'drop'] = True

    # Make sure just get tuition
    df.loc[(df['Category'] == 'Tuition') & (~df['Original Description'].str.contains('abc', case=False)), 'drop'] = True

    # Remove a one-time crazy cost
    # df.loc[(df['Category'] == 'Doctor') & (df['Description'] == 'asdf'), 'drop'] = True

    df = df[df['drop'] == False]
    del df['drop']
    return df

def etl_income(income):
    # These are okay:
    #   Gift
    #   Income
    #   Federal Tax
    #   Electronics & Software

    # Combine everything but Federal Tax and Paycheck.

    income['drop'] = False

    income.loc[(income['Category'] == 'Paycheck') & (income['Description'].str.contains('abc', case=False)), 'drop'] = True

    # Weird FSU Paycheck
    income.loc[(income['Category'] == 'Travel') & (income['Description'].str.contains('abc', case=False)), 'drop'] = True

    income = income[income['drop'] == False]
    del income['drop']
    return income

df = pd.read_csv('./transactions.csv')
df = to_date(df)

# Get since 
start_date_tjob = '2017-11-01'

# Get from a year ago
start_date_yago = datetime.datetime.now() - datetime.timedelta(days=365)

# Get the time frame
#df = df[df['date'] >= start_date_tjob]

# How many months
nmonths = diff_month(df['date'].max(), df['date'].min())

df = etl(df)

# convert amounts to +/- for credit/debit
df['transaction'] = df['Amount'] * df['Transaction Type'].map({'credit': 1, 'debit': -1})

# Combine income sources
income = {
        'Paycheck': 'Income',
        'Federal Tax': 'Income',
        'Rental Income': 'Income',
        'Credit Card Payment': 'cc_payment'
    }

#df['group_category'] = df['Category'].replace(income)

# Mandatory Expenses
mandatory_list = ['Mortgage & Rent', 'Utilities', 'cc_payment', 'Auto Insurance', 'Gas & Fuel',
        'Groceries', 'Home Insurance', 'Internet', 'Mobile Phone', 'Student Loan', 'Tuition',
        'Finance Charge', 'Bank Fee', 'Pharmacy', 'Matt Friend Fee', 'Doctor', 'Investments']

mand = {m: df[df['Category'] == m].groupby('ym').sum().mean()['transaction'] for m in mandatory_list}
mand = pd.Series(mand)
mand = override(mand)
mand = mand.round(2)

print('')
print(mand)

print('\nTotal Monthly Expenses: ${0:.2f}\n'.format(mand.sum()))

#income = etl_income(df[df['transaction'] >= 0].copy())
#del income['group_category']

# Income categories:
income_list = ['Paycheck', 'Income', 'Federal Tax', 'Interest Income']

inc = {m: df[df['Category'] == m].groupby('ym').sum().mean()['transaction'] for m in income_list}
inc = pd.Series(inc)
#inc = override(inc)
inc = inc.round(2)

print('\nIncome')
print(inc)
