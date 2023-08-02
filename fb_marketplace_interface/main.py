from helpers.scraper import Scraper
from helpers.csv_helper import get_data_from_csv
from helpers.listing_helper import update_listings
import tkinter as tk
from tkinter import filedialog

scraper = Scraper('https://facebook.com')
# Add login functionality to the scraper
scraper.add_login_functionality('https://facebook.com', 'svg[aria-label="Your profile"]', 'facebook')
scraper.go_to_page('https://facebook.com/marketplace/you/selling')

# Get data for item type listings from csvs/items.csv
item_listings = get_data_from_csv('items')
# Publish all of the items into the facebook marketplace
#update_listings(item_listings, 'item', scraper)

# Get data for vechile type listings from csvs/vechiles.csv
vehicle_listings = get_data_from_csv('vehicles')
# Publish all of the vehicles into the facebook marketplace
#update_listings(vehicle_listings, 'vehicle', scraper)


# Create tkinter window
window = tk.Tk()
window.title("Facebook Marketplace Listing Bot")
window.geometry("400x350")

list_item_button = tk.Button(window, text="List Items", command=lambda:update_listings(vehicle_listings, 'item', scraper))
list_item_button.pack(pady=10)

list_vehicle_button = tk.Button(window, text="List Vehicle", command=lambda:update_listings(vehicle_listings, 'vehicle', scraper))
list_vehicle_button.pack(pady=10)

window.mainloop()













