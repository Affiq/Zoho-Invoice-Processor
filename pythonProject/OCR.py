# Here are the system configurations
import numpy as np
import pdf2image as p2i
import pytesseract

import CSVManager
import zohoData
from Configs import Configs

def read_pdf_file(file_path, target_csv_path):
    configs = Configs()
    pytesseract.tesseract_cmd = configs.get_pytesseract_directory
    extracted_text = []

    completed_shipment_numbers = CSVManager.get_shipment_numbers(target_csv_path)

    try:
        print("Converting PDF to image list...")
        converted_pdf = p2i.convert_from_path(file_path)
        print("Image list created successfully...")

        # Custom configuration - 6 - assume uniform block of text
        custom_psm_config = r'--oem 3 --psm 3'

        # We will attempt to do this for one-paged invoices
        # We may run into some trouble doing it for multi-paged invoices
        for img in converted_pdf:
            img = np.array(img)
            extracted_text = pytesseract.image_to_string(img, config=custom_psm_config)
            data_list = zohoData.processDataString(extracted_text)
            print("Data extracted successfully...")
            # We need to check if we have processed this invoice, and we need to fix the S->$ issue
            shipment_number = CSVManager.format_invoice_num(data_list[0])
            if shipment_number not in completed_shipment_numbers:
                CSVManager.data_list_to_csv(data_list, target_csv_path)
            else:
                print("This invoice has already been processed. Delete from CSV to reprocess")
                print();
    except:
        print("An error occurred")