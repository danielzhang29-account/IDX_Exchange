import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

#listings

listing1 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202401.csv')
listing2 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202402.csv')
listing3 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202403.csv')
listing4 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202404.csv')
listing5 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202405.csv')
listing6 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202406.csv')
listing7 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202407.csv')
listing8 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202408.csv')
listing9 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202409.csv')
listing10 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202410.csv')
listing11 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202411.csv')
listing12 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202412.csv')
listing13 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202501.csv')
listing14 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202502.csv')
listing15 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202503.csv')
listing16 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202504.csv')
listing17 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202505.csv')
listing18 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202506.csv')
listing19 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202507.csv')
listing20 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202508.csv')
listing21 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202509.csv')
listing22 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202510.csv')
listing23 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202511.csv')
listing24 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202512.csv')
listing25 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSListing202601.csv')
listing26 = pd.read_csv('/Users/Kyle/Documents/IDXWork/Week0/CRMLSListing202602.csv')
listing27 = pd.read_csv('/Users/Kyle/Documents/IDXWork/Week0/CRMLSListing202603.csv')

total_1 = len(listing1) + len(listing2) + len(listing3) + len(listing4) + len(listing5) + len(listing6) + len(listing7) + len(listing8) + len(listing9) + len(listing10) + len(listing11) + len(listing12) + len(listing13) + len(listing14) + len(listing15) + len(listing16) + len(listing17) + len(listing18) + len(listing19) + len(listing20) + len(listing21) + len(listing22) + len(listing23) + len(listing24) + len(listing25) + len(listing26) + len(listing27) 

print(total_1)

total_listings = pd.concat([listing1, listing2, listing3, listing4, listing5, listing6, listing7, listing8, listing9, listing10, listing11, listing12, listing13, listing14, listing15, listing16, listing17, listing18, listing19, listing20, listing21, listing22, listing23, listing24, listing25, listing26, listing27], ignore_index=True)

print(len(total_listings))

filtered_listings = total_listings[total_listings].PropertyType == 'Residential']
len(filtered)_listings)

filtered_listings.to_csv('/Users/Kyle/Documents/IDXWork/Week1/listing.csv', index=False)

#sold

sold1 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202401.csv')
sold2 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202402.csv')
sold3 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202403.csv')
sold4 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202404.csv')
sold5 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202405.csv')
sold6 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202406.csv')
sold7 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202407.csv')
sold8 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202408.csv')
sold9 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202409.csv')
sold10 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202410.csv')
sold11 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202411.csv')
sold12 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202412.csv')
sold13 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202501.csv')
sold14 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202502.csv')
sold15 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202503.csv')
sold16 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202504.csv')
sold17 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202505.csv')
sold18 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202506.csv')
sold19 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202507.csv')
sold20 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202508.csv')
sold21 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202509.csv')
sold22 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202510.csv')
sold23 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202511.csv')
sold24 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202512.csv')
sold25 = pd.read_csv('/Users/Kyle/Documents/IDXWork/raw/CRMLSSold202601.csv')
sold26 = pd.read_csv('/Users/Kyle/Documents/IDXWork/Week0/CRMLSSold202602.csv')
sold27 = pd.read_csv('/Users/Kyle/Documents/IDXWork/Week0/CRMLSSold202603.csv')

total_2 = len(sold1) + len(sold2) + len(sold3) + len(sold4) + len(sold5) + len(sold6) + len(sold7) + len(sold8) + len(sold9) + len(sold10) + len(sold11) + len(sold12) + len(sold13) + len(sold14) + len(sold15) + len(sold16) + len(sold17) + len(sold18) + len(sold19) + len(sold20) + len(sold21) + len(sold22) + len(sold23) + len(sold24) + len(sold25) + len(sold26) + len(sold27) 

print(total_2)

total_sold = pd.concat([sold1, sold2, sold3, sold4, sold5, sold6, sold7, sold8, sold9, sold10, sold11, sold12, sold13, sold14, sold15, sold16, sold17, sold18, sold19, sold20, sold21, sold22, sold23, sold24, sold25, sold26, sold27], ignore_index=True)
print(len(total_sold))

filtered_sales = total_sold[total_sold.PropertyType == 'Residential']
len(filtered_sales)