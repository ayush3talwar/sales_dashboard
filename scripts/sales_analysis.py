import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Connect to MySQL and Fetch Data
db_connection = mysql.connector.connect(
    host="127.0.0.1",    # Change this to your MySQL host
    user="root",         # Your MySQL username
    password="root@123", # Your MySQL password
    database="sales_data" # The database name you created
)

# Create a cursor object to execute SQL queries
cursor = db_connection.cursor()

# Step 2: SQL Query to Extract Data
query = """
SELECT OrderID, OrderDate, ShipDate, ShipMode, CustomerID, CustomerName, Segment, 
       Country, City, State, PostalCode, Region, ProductID, Category, SubCategory, 
       ProductName, Sales, Quantity, Discount, Profit 
FROM Sales;
"""

cursor.execute(query)

# Fetch all results into a Pandas DataFrame
data = cursor.fetchall()
columns = [
    'OrderID', 'OrderDate', 'ShipDate', 'ShipMode', 'CustomerID', 'CustomerName', 
    'Segment', 'Country', 'City', 'State', 'PostalCode', 'Region', 'ProductID', 
    'Category', 'SubCategory', 'ProductName', 'Sales', 'Quantity', 'Discount', 'Profit'
]
df = pd.DataFrame(data, columns=columns)

# Close the MySQL connection
cursor.close()
db_connection.close()

# Step 3: Data Analysis in Pandas
# Convert dates to datetime format
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['ShipDate'] = pd.to_datetime(df['ShipDate'])

# Example Analysis 1: Total Sales by Year
df['Year'] = df['OrderDate'].dt.year
sales_by_year = df.groupby('Year')['Sales'].sum()

# Example Analysis 2: Top 5 Products by Profit
top_products = df.groupby('ProductName')['Profit'].sum().sort_values(ascending=False).head(5)

# Example Analysis 3: Sales by Region
sales_by_region = df.groupby('Region')['Sales'].sum()

# Step 4: Create Simple Plot for Visualization
# Total Sales by Year Plot
plt.figure(figsize=(10, 6))
sns.lineplot(data=sales_by_year)
plt.title("Total Sales by Year")
plt.xlabel("Year")
plt.ylabel("Sales")
plt.savefig('sales_by_year.png')  # Save plot as image

# Step 5: Export Data to Excel for Analysis or Tableau
# Save dataframes to Excel
with pd.ExcelWriter('sales_analysis.xlsx', engine='openpyxl') as writer:
    sales_by_year.to_excel(writer, sheet_name='Sales_by_Year')
    top_products.to_excel(writer, sheet_name='Top_Products')
    sales_by_region.to_excel(writer, sheet_name='Sales_by_Region')

# Step 6: Prepare Data for Tableau
# Export the cleaned dataframe to CSV for Tableau
df.to_csv('sales_data_for_tableau.csv', index=False)

print("Data analysis completed and saved to 'sales_analysis.xlsx' and 'sales_data_for_tableau.csv'.")
