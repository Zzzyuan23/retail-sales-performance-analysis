Retail Sales Performance Analysis

A Python project that analyzes a retail (Superstore) sales dataset to uncover sales trends, top-performing products and regions, and shipping performance.

Dataset
Superstore sales data from Kaggle (rohitsahoo/sales-forecasting). It contains order dates, ship modes, customer segments, locations, product categories and sales amounts. The dataset has no profit column, so this analysis focuses on sales.

Tools Used
Python
pandas (data cleaning and analysis)
matplotlib (visualizations)

What the Script Does
1. Loads the sales data from a CSV file
2. Cleans it: parses day-first dates, removes duplicate rows, checks for missing values
3. Creates new fields such as year, month and shipping days
4. Groups and summarizes sales by year, month, category, sub-category, region, state, segment and ship mode
5. Saves 6 charts to a charts folder
6. Writes a text summary of the findings to summary.txt

Key Findings
- Total sales: $2,261,255 across 4,922 orders from 793 customers (average order value $459.42)
- Growth: sales dipped 4.2% in 2016, then grew 30.6% in 2017 and 20.3% in 2018
- Seasonality: November is the strongest month overall
- Top category: Technology (36.6% of sales), led by Phones ($327,782)
- Top region: West (31.4% of sales)
- Top states: California, New York and Texas together make up 40.7% of sales
- Top segment: Consumer (50.8% of sales)
- Shipping: average delivery takes 2.2 days (First Class), 3.2 days (Second Class) and 5.0 days (Standard Class)
  
Charts
	
<img width="1350" height="750" alt="6_top_states" src="https://github.com/user-attachments/assets/d2ccab84-6113-4c0f-9bf0-187e9491cbee" />
<img width="960" height="720" alt="5_sales_by_region" src="https://github.com/user-attachments/assets/34e91679-4f81-4806-be39-fd0163e95032" />
<img width="1350" height="750" alt="4_top_subcategories" src="https://github.com/user-attachments/assets/355fad87-69f8-4869-826c-b186d2dfcc15" />
<img width="960" height="720" alt="3_sales_by_category" src="https://github.com/user-attachments/assets/a0869d73-e927-4290-9ef2-0ec5d8cdfa3d" />
<img width="1500" height="675" alt="2_monthly_sales_trend" src="https://github.com/user-attachments/assets/1991490f-de8d-4e83-8a80-6d08004f4200" />
<img width="960" height="720" alt="1_sales_by_year" src="https://github.com/user-attachments/assets/66a331ed-7112-4edb-bd45-6c33fdf6161b" />

How to Run
1. Install the libraries:
   py -m pip install pandas matplotlib

2. Download the dataset from Kaggle and place train.csv in the same folder as the script.
Run:
   py retail_sales_analysis.py

3. The charts and summary.txt will be created in the same folder.
