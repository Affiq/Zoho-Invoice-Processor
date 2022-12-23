import PyPDF2


def read_pdf(target_pdf_path):
    try:
        print("Using PDF reader for: "+target_pdf_path)

        # create pdfreader object and page object to extract string
        pdf_file_obj = open(target_pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        page_obj = pdf_reader.pages[0]
        extracted_string = page_obj.extract_text()

        print("Extracted PDF String...")
        return parse_extracted_string(extracted_string)
    except Exception as e:
        print("PDF reader function error")


# Function used to extract the relevant information from the string.
def parse_extracted_string(extracted_string):
    try:
        extracted_string_list = extracted_string.split("\n")
        print(extracted_string_list)

        # Main block that extracts Strings according to previous line - 'identifiers' in a sense
        for i, current_string in enumerate(extracted_string_list):
            if current_string == "Invoice#":
                invoice_num = extracted_string_list[i+1]
            elif current_string == "Invoice Date":
                invoice_date = extracted_string_list[i+1]
            elif current_string == "Due Date":
                due_date = extracted_string_list[i+1]
            elif current_string == "Subtotal":
                subtotal = "Subtotal " + extracted_string_list[i+1]
            elif current_string == "TOTAL":
                total = "TOTAL " + extracted_string_list[i+1]
            elif current_string == "Bill To":
                recipient_name = extracted_string_list[i+1]
                recipient_loc = extracted_string_list[i+2]
        product_list = get_product_list(extracted_string)

        # Needs to be in a CSVManager compatible form
        final_list = [invoice_num, recipient_name, invoice_date, recipient_loc, due_date]
        final_list = final_list + product_list + [subtotal, total]
        return final_list
    except Exception as e:
        print("Problem parsing pdf string: " + e)


# We will get a list of products through here...
# Takes in the entire array and looks for 'Amount' and 'Notes' identifier
# Which signals start and end of product information
def get_product_list(data_string):
    try:
        data_string_list = data_string.split("\n")
        start_index = data_string_list.index("Amount") + 1
        end_index = data_string_list.index("Notes")

        # Create sublist containing product information, and remove empty lines...
        data_string_list = data_string_list[start_index:end_index]
        data_string_list = list(filter(is_not_empty, data_string_list))

        psl_length = len(data_string_list)
        product_sub_list = []
        print("Product sublist: " + str(data_string_list))

        # Attempt to join fractured product names
        last_string_index = None
        product_name = ""
        new_product_list = []
        for i in range(0, psl_length):
            if not(try_parse_to_float(data_string_list[i])): # If you can't parse to float, it's a product name
                if last_string_index is None: # First occurrence of a name indicator
                    last_string_index = i;
                    product_name = product_name + data_string_list[i]
                else: # The previous index was also a product
                    last_string_index = i;
                    product_name = product_name + data_string_list[i]
            else:
                if last_string_index is not None: # Add product name, reset the name and pointer, and add current element
                    new_product_list.extend([product_name, data_string_list[i]])
                    last_string_index = None
                    product_name = ""
                else: # We are just moving from float to another float
                    new_product_list.append(data_string_list[i])

        data_string_list = new_product_list
        # Put it in form 'Product![NameIdentifier] [Quantity] [Rate] [Amount]'
        # and add it to product sublist
        product_sub_list = []
        print("Product list: " + str(data_string_list))
        for i in range(0, psl_length-1, 4):
            product_string = "Product!"+data_string_list[i] + " " + data_string_list[i+1] + " " + \
                             data_string_list[i+2] + " " + data_string_list[i+3]
            print("Adding to list: " + product_string)
            product_sub_list.append(product_string)

        return product_sub_list
    except Exception as e:
        print("Problem getting product list: " + str(e))


def try_parse_to_float(string):
    try:
        new_float = float(string)
        return True
    except Exception as e:
        return False


def is_not_empty(element):
    if element == " ":
        return False
    else:
        return True
