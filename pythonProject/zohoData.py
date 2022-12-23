def process_data_string(data_string):
    print("Converting PDF data to CSV data...")

# This function is compatible with the OCR reader and not the pdf reader...
# Currently, this program should work for Single paged invoices...
# We will have one long text file, we should split it into individual lines
# Some of the data will be combined and will need some processing...
# We will list the data required
# datalist[4]: Ignore Bill To, Get Invoice#, XXXXXX
# datalist[5]: Recipient Name, Invoice Date: XX Nov 20XX
# datalist[6]: Recipient Loc.
# datalist[7]: Due Date
# datalist[9->n]: Each line corresponds to Item name + desc, Quantity, and Amount
# until the next line is subtotal
# dataline[x]: subtotal xxxx.xx
# dataline[x]: total xxxx.xx
# the rest will be ignored for now
def processDataString(dataString):
    try:
        print("Processing Zoho Data...");

        zohodatalist = dataString.split("\n")
        print(str(zohodatalist))


        output_datalist = []

        # We will directly extract from indexes for computational efficiency
        # As this will reduce number of conditions in for loop

        # Get the invoice number
        current_dataline = str(zohodatalist[4])
        current_dataline = current_dataline.replace("Bill To Invoice#", "")
        output_datalist.append(current_dataline)

        # Get recipient name and invoice date
        current_dataline = str(zohodatalist[5])
        current_dataline = current_dataline.replace("Invoice", "!Invoice")
        current_datalines = current_dataline.split("!")
        output_datalist.append(current_datalines[0])
        current_datalines[1] = current_datalines[1].replace("Invoice Date", "")
        output_datalist.append(current_datalines[1])

        # Get recipient loc.
        current_dataline = str(zohodatalist[6])
        output_datalist.append(current_dataline)

        # Get due date
        current_dataline = str(zohodatalist[7])
        current_dataline = current_dataline.replace("Due Date ", "")
        output_datalist.append(current_dataline)

        # Extracting the the other information, starting from 9th row
        for dataline in zohodatalist[9:]:

            if "Subtotal" in dataline: # Subtotal data indicator
                output_datalist.append(dataline)
            elif "TOTAL" in dataline: # Total data indicator
                output_datalist.append(dataline)
                break # We want to stop processing once total is obtained
            else: # It has to be product information...
                output_datalist.append("Product!"+dataline)

        print("Data extracted:"+str(output_datalist))
        print()
        return output_datalist
    except:
        print("Error processing Zoho data")
        print()
        return []