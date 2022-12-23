import csv
import calendar
import os

import numpy as np
from numpy import genfromtxt

import Configs


# Returns the path to the csv file...
# Also initialises a CSV file with some headers if not detected
def initialise_csv(csv_folder_path, csv_name):
    file_title = csv_folder_path + "\\" + csv_name + ".csv"
    if not (os.path.exists(file_title)):
        print("No CSV detected. Creating new CSV...");
        # This will be in accordance to our zohoData.processData
        f = open(file_title, 'w', newline='')
        # product, total and subtotal printing...
        # add headers - Customer Name, Invoice Number, Invoice Date
        # item name, quantity, unit price, description, sales taxes, messages
        writer = csv.writer(f)
        headers = ["Customer Name", "Invoice Number", "Invoice Date", "Item Name",
                   "Quantity", "Unit Price", "Description", "Sales Taxes", "Messages"]
        writer.writerow(headers)
        f.close()
    else:
        print("CSV File detected.")
    return file_title


def get_shipment_numbers(target_csv_path):
    try:
        my_data = np.genfromtxt(target_csv_path, delimiter=',', dtype=None, encoding=None)
        shipment_number_list = my_data[:, 1].tolist()
        del shipment_number_list[0] # Getting rid of the header
    except Exception: # It must mean its a new CSV file...
        shipment_number_list = []

    return shipment_number_list




# Data should be in form:
# Customer Name, Invoice Number, Invoice Date, Item Name, Quantity
# Unit Price, Description, Sales Taxes, Messages
def data_list_to_csv(data_list, target_csv_path):
    print("Writing to CSV...")
    try:

        # This will be in accordance to our zohoData.processData
        f = open(target_csv_path, 'a', newline='')

        # create the csv writer
        writer = csv.writer(f)

        # product, total and subtotal printing...
        # add headers - Customer Name, Invoice Number, Invoice Date
        # item name, quantity, unit price, description, sales taxes, messages

        customer_name = data_list[1]
        invoice_number = format_invoice_num(data_list[0])
        invoice_date = format_date(data_list[2])
        item_name = "SALE - VINTAGE"  # Default value for item name
        quantity = 1
        unit_price = 1
        sales_taxes = ""
        messages = "SUCCESS: Invoice created."

        # if it contains a Product!, add it to the total string list...
        total_products_data_string = ""
        for data_string in data_list:
            if "Product!" in data_string:
                product_data_string = format_product_data_to_string(data_string)
                total_products_data_string = total_products_data_string + product_data_string
            elif "TOTAL" in data_string:
                data_string = data_string.replace("TOTAL ", "")
                total = (["Total", data_string])  # unused for now

        writer.writerow([customer_name, invoice_number, invoice_date, item_name,
                         quantity, unit_price, total_products_data_string, sales_taxes, messages])
        print("CSV Writing successful")
        print("Invoice extracted for :"+ str(target_csv_path))

        f.close()
    except Exception:
        print("Problem writing to CSV - Likely due to incorrect format")


def product_data_to_list(data_string):  # rsplit partitions from right
    data_list = data_string.rsplit(" ", 3)
    return data_list


def format_product_data_to_string(data_string):  # Extract relevant information for CSV file...
    data_string = data_string.replace("Product!", "")  # Remove product identifier
    product_data_list = data_string.rsplit(" ", 3)  # Split into constituents
    product_data_list[1] = "x" + product_data_list[1]  # add xN for quantities
    product_data_list[2] = "RM" + product_data_list[2]  # add currency for our rate
    product_data_list.remove(product_data_list[3])  # We don't care about product total
    product_string = ' '.join(product_data_list) + " "  # add a " " to seperate products later
    return product_string;


# Our OCR has a bad habit or reading italic S as a $
def format_invoice_num(invoice_num):
    invoice_num = invoice_num.replace("$", "S")
    return invoice_num


# We need to convert Short form month names to number
def format_date(date):
    date_list = date.split()
    month_string = date_list[1]
    month_num = str(list(calendar.month_abbr).index(month_string))
    return str(date_list[0]) + "/" + month_string + "/" + str(date_list[2])
