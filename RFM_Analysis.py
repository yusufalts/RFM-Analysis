# BUSINESS PROBLEM

# An e-commerce company wants to divide its customers into segments and determine marketing strategies according to these segments

# Data Set Story

# Online Retail II, a dataset of an online retail store based in the UK It includes sales between 01/12/2009 - 09/12/2011.
# Data Set web address
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II
#
# Variables
#
# InvoiceNo: Invoice number. Unique number for each transaction, i.e. invoice. If it starts with C, the canceled transaction.
#
# StockCode: Product code. Unique number for each product.
# Description: Product name.
# Quantity: This is the quantity of the product. It expresses how many of the products in the invoices were sold.
# InvoiceDate: Invoice date and time.
# UnitPrice: Product price (in pounds sterling).
# CustomerID: Unique customer number.
# Country: Country name. The country where the customer lives.

# import Required Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import datetime as dt
import matplotlib.pyplot as plt
import plotly.express as px
import warnings

warnings.simplefilter(action="ignore")

# Adjusting Row Column Settings
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", lambda x: '%.2f' % x)

# Loading the Data Set
df_1 = pd.read_excel("/Users/yusufaltas/PycharmProjects/Item-Based Collaborative Filtering/datasets/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df_2 = pd.read_excel("/Users/yusufaltas/PycharmProjects/Item-Based Collaborative Filtering/datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")

df = pd.concat([df_1, df_2], ignore_index=True)

df.head()

df.shape

# Preliminary examination of the data set
def check_df(dataframe, head=5):
    print('##################### Shape #####################')
    print(dataframe.shape)
    print('##################### Types #####################')
    print(dataframe.dtypes)
    print('##################### Head #####################')
    print(dataframe.head(head))
    print('##################### Tail #####################')
    print(dataframe.tail(head))
    print('##################### NA #####################')
    print(dataframe.isnull().sum())
    print('##################### Quantiles #####################')
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# Examination of numerical and categorical variables

def grab_col_names(dataframe, cat_th=10, car_th=20):
    """
    Returns the names of categorical, numeric and categorical but cardinal variables in the data set.
    Note Categorical variables include categorical variables with numeric appearance.
    Parameters
    ------
         dataframe: dataframe
                Dataframe to get variable names
        cat_th: int, optional
                class threshold for numeric but categorical variables
        car_th: int, optinal
                    class threshold for categorical but cardinal variables
    Returns
    ------
        cat_cols: list
                Categorical variable list
                     num_cols: list
                Numeric variable list
        cat_but_car: list
                List of cardinal variables with categorical view
    Examples
    ------
        import seaborn as sns
        df = sns.load_dataset("iris")
        print(grab_col_names(df))
    Notes
    ------
        cat_cols + num_cols + cat_but_car = total number of variables
        num_but_cat is inside cat_cols.
        The sum of the 3 return lists equals the total number of variables: cat_cols + num_cols + cat_but_car = number of variables
    """

    # cat_cols, cat_but_car
    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == 'O']
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
                   dataframe[col].dtypes != 'O']
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
                   dataframe[col].dtypes == 'O']
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    # num_cols
    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != 'O']
    num_cols = [col for col in num_cols if col not in num_but_cat]

    print(f'Observations: {dataframe.shape[0]}')
    print(f'Variables: {dataframe.shape[1]}')
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')
    return cat_cols, num_cols, cat_but_car, num_but_cat


cat_cols, num_cols, cat_but_car, num_but_cat = grab_col_names(df)

# We selected the sales with a sales number greater than zero from df and reassigned it to the df variable.
#The reason for doing this is to remove the purchase returns from the data set.

df = df[(df['Quantity'] > 0)]


# We removed empty observations from the data set.
df.dropna(inplace=True)

df.shape


df.isnull().sum()

# From the observations in the dataset, we selected the observations that do not contain the C expression.
df = df[df["Invoice"].astype(str).str.contains("C")==False]

# Numerical variable analysis
def num_summary(dataframe, numerical_col, plot=False):
    quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
    print(dataframe[numerical_col].describe(quantiles).T)

    if plot:
        dataframe[numerical_col].hist(bins=20)
        plt.xlabel(numerical_col)
        plt.title(numerical_col)
        plt.show(block=True)

for col in num_cols:
    num_summary(df, col, plot=True)

# Correlation Analysis of the Variables

def df_corr(dataframe, annot=True):

    numeric_df = dataframe.select_dtypes(include=[np.number])


    corr_matrix = numeric_df.corr()


    sns.heatmap(corr_matrix, annot=annot, linewidths=.2, cmap='Reds', square=True)
    plt.show(block=True)


def high_correlated_cols(dataframe, head=10):
    numeric_df = dataframe.select_dtypes(include=[np.number])

    corr_matrix = numeric_df.corr().abs()
    corr_cols = (corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1)
                                   .astype(bool)).stack().sort_values(ascending=False)).head(head)
    return corr_cols


df_corr(df, annot=False)

high_correlated_cols(df, 15)

# Calculating RFM Metrics (Recency, Frequency, Monetary)

# Present Date (date of analysis)
today_date = dt.datetime(2011, 12, 11)

# InvoiceDate => Recency
# Invoice => Frequency
# TotalPrice => Monetary

# Creation of TotalPrice
df["TotalPrice"] = df["Quantity"] * df["Price"]

df.head()

df["InvoiceDate"].max()

today_date

# Calculating RFM Metrics
rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda InvoiceDate: (today_date - InvoiceDate.max()).days,
                                     'Invoice': lambda Invoice: Invoice.nunique(),
                                     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

rfm.head()

# Changing column names
rfm.columns = ['recency', 'frequency', 'monetary']

rfm.head()

# Avoiding negative values due to refunds
rfm = rfm[rfm["monetary"] > 0]

# Calculating RFM Scores (Recency_Score, Frequency_Score, Monetary_Score)

# Calculating Recency_Score
rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])

rfm.head()

# Calculating Frequency_Score
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])

rfm.head()

# Calculating Monetary_Score
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()

# Creating RFM_SSCORE VARIABLE
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))

rfm.head()

# Creating & Analysing RFM Segments

#Champions are the best customers, who bought most recently, most often, and are heavy spenders. Reward these customers. They can be the first to buy new products

#Potential Loyalists are the recent customers with average frequency and who spent a good amount. You can make them your Loyalists or Champions by offering membership or loyalty programs or recommending related products to them.

#New Customers are the customers who have a high overall RFM score but are not frequent shoppers. Special offers can be provided to increase their visits

#At Risk Customers are the customers who purchased often and spent big amounts, but haven’t purchased recently. Personalized deals and product/service recommendations can help reactivate them

#Can’t Lose Them are the customers who used to visit and purchase quite often, but haven’t been visiting recently. Get them to revisit with relevant promotions and conduct surveys to find out what went wrong and not lose them to a competitor.

# Creation of a segment map
seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

# creating segment variable
rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)

rfm.head()

rfm.shape

# Segment Distribution
segment_counts = rfm['segment'].value_counts()
plt.figure(figsize=(16, 8))
sns.barplot(x=segment_counts.index, y=segment_counts.values)
plt.title('Segment Distribution')
plt.xlabel('Segment')
plt.ylabel('Customer Count')
plt.xticks(rotation=45)
plt.show()

# Segment Analysis
fig = px.scatter(rfm, x='recency', y='frequency', color='segment', title='RFM Segments')
fig.show()

rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])

new_df = pd.DataFrame()

new_df["new_customer_id"] = rfm[rfm["segment"] == "new_customers"].index

new_df.head()

new_df["new_customer_id"] = new_df["new_customer_id"].astype(int)

new_df.head()

# new_df.to_csv("new_customers.csv")

# rfm.to_csv("rfm.csv")

df.head()

# Convert InvoiceDate to a datetime object

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Extract day, year, time and hour
df['Day'] = df['InvoiceDate'].dt.day
df['Month'] = df['InvoiceDate'].dt.month
df['Year'] = df['InvoiceDate'].dt.year
df['Time'] = df['InvoiceDate'].dt.time
df['Hour'] = df['InvoiceDate'].dt.hour

df.head()

# Top 10 Customers
top_customers = df.groupby('Customer ID')['TotalPrice'].sum().sort_values(ascending=False).head(10)

# Create a bar chart
plt.figure(figsize=(15,8))
sns.barplot(x=top_customers.index, y=top_customers.values)
plt.title('Top 10 Customers by Purchase Amount')
plt.xlabel('Customer ID')
plt.xticks(rotation = 90)
plt.ylabel('Total Purchase Amount')
plt.show()


# Top 10 Most Selling Items
top_item = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)

# Create a bar chart
plt.figure(figsize=(15,8))
sns.barplot(x=top_item.index, y=top_item.values)
plt.title('Top 10 Most Selling item.')
plt.xticks(rotation = 90)
plt.ylabel('Total Sales Amount')
plt.xlabel('Item name')
plt.show()

# Top 5 Purchasing Country

# Calculate total sales by country
sales_by_country = df.groupby('Country')['TotalPrice'].sum().reset_index()

# Sort the sales by descending order
sales_by_country = sales_by_country.sort_values(by='TotalPrice', ascending=False).head(5)

# Create the bar chart
plt.figure(figsize=(15,8))
plt.bar(sales_by_country['Country'], sales_by_country['TotalPrice'])
plt.xlabel('Country')
plt.ylabel('Total Sales')
plt.title('Total Sales by Country')
plt.ticklabel_format(style='plain', axis='y')
plt.show()


# Sales By Years

# Group by year and sum TotalPrice
sales_by_year = df.groupby('Year')['TotalPrice'].sum().reset_index()

# Create bar chart using Seaborn
plt.figure(figsize=(15,8))
sns.set_style('darkgrid')
sns.barplot(x='Year', y='TotalPrice', data=sales_by_year)
plt.ticklabel_format(style='plain', axis='y')
plt.show()

# Sales By Month
# Group by months and sum TotalPrice
sales_by_months = df.groupby('Month')['TotalPrice'].sum().reset_index()
month=['Jan', 'Feb','Mar','Apr', 'May', 'June', 'July', "Aug", "Sep", 'Oct', 'Nov', 'Dec']
# Create bar chart using Seaborn
plt.figure(figsize=(15,8))
sns.set_style('darkgrid')
sns.barplot(x=month, y=sales_by_months['TotalPrice'], data=sales_by_year)
plt.ticklabel_format(style='plain', axis='y')
plt.show()

# Sales By Day

# Group by day and sum TotalPrice
sales_by_months = df.groupby('Day')['TotalPrice'].sum().reset_index()

# Create bar chart using Seaborn
plt.figure(figsize=(15,8))
sns.set_style('darkgrid')
sns.lineplot(x=sales_by_months.Day, y=sales_by_months.TotalPrice, data=sales_by_year)
plt.show()

# Sales By Hour

c=df.groupby('Hour').count()
hours=[hour for hour , df in df.groupby('Hour')]
plt.figure(figsize=(15,8))
plt.plot(hours,c['Quantity'])
plt.xticks(hours)
plt.title('Number of Orders Per Hour')
plt.xlabel('Hours 24')
plt.ylabel('Numbers of Oder')
plt.grid()
plt.show()