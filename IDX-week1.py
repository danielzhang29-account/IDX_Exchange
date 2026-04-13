import pandas as pd

#listings

february_listings = pd.read_csv("/Users/Kyle/IDX-Exchange/CRMLSListing202602.csv")
march_listings = pd.read_csv("/Users/Kyle/IDX-Exchange/CRMLSListing202603.csv")

print("February Total Listings: ", len(february_listings))
print("March Total Listings: ", len(march_listings))

listings = pd.concat([february_listings, march_listings], ignore_index=True)
print("After Concat Listings Total:", len(listings))

print("Before Filtering Listings Total: ", len(listings))
filtered_listings = listings[listings["PropertyType"] == "Residential"]
print("After Filtering Listings Total:", len(filtered_listings))

filtered_listings.to_csv("filtered_listings.csv", index=False)

# Sales

february_sales = pd.read_csv("/Users/Kyle/IDX-Exchange/CRMLSSold202602.csv")
march_sales = pd.read_csv("/Users/Kyle/IDX-Exchange/CRMLSSold202603.csv")

print("February Total Sold:", len(february_sales))
print("March Total Sold:", len(march_sales))

sold = pd.concat([february_sales, march_sales], ignore_index=True)
print("After Concat Sold Total:", len(sold))

print("Before Filtering Sold Total:", len(sold))
filtered_sold = sold[sold["PropertyType"] == "Residential"]
print("After Filtering Sold Total:", len(filtered_sold))

filtered_sold.to_csv("filtered_sold.csv", index=False)
