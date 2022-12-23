import subprocess
from pathlib import Path
import os
import CSVManager
import OCR
import pdf_reader
from Configs import Configs
import PyPDF2


def start_console():
    config = Configs()
    source_folder = config.home_directory
    print("Welcome to the Zoho Invoice to CSV Generator:")
    print()
    print("Folder list:")
    if not (os.path.exists(source_folder) or os.path.isdir(source_folder)):
        print("Source folder not found, please configure")
    else:
        print_directories(source_folder)
        print()
        print("Choose a folder to create a CSV for:")
        input_folder = input()
        print()
        if check_input_directory(input_folder, source_folder):
            print("Valid folder, initialising CSV file...")
            main_csv = CSVManager.initialise_csv(source_folder+"\\"+input_folder, input_folder)
            print()
            loop_through_folder(source_folder+"\\"+input_folder, main_csv)
        else:
            print("No such folder exists...")


def check_input_directory(user_input, source_folder):
    file_list = get_folders_in_directory(source_folder)
    if user_input not in file_list:
        return False
    else:
        return True


def print_directories(source_folder):
    # For absolute paths instead of relative the current dir
    root_dir = Path(source_folder)
    file_list = get_folders_in_directory(source_folder)
    for dir_name in file_list:
        print(dir_name)


def get_folders_in_directory(source_folder):
    # For absolute paths instead of relative the current dir
    root_dir = Path(source_folder)
    file_list = os.listdir(root_dir)
    valid_folders = []
    for dir_name in file_list:
        current_file = source_folder + "\\" + dir_name
        if os.path.isdir(current_file):
            valid_folders.append(dir_name)
    return valid_folders


def loop_through_folder(folder_path, target_csv_path):
    # First we must check which files are of type pdf
    root_dir = Path(folder_path)
    file_list = os.listdir(root_dir)
    for current_file in file_list:
        file_breakdown = current_file.rsplit(".",1)
        if file_breakdown[1] == "pdf":
            print("Extracting: "+current_file)
            # Extract data from pdf in desired format
            data_list = pdf_reader.read_pdf(folder_path+"//"+current_file);
            print("Data list: " + str(data_list))

            # We need to check if we have already extracted this invoice
            completed_shipment_numbers = CSVManager.get_shipment_numbers(target_csv_path)
            shipment_number = CSVManager.format_invoice_num(data_list[0])
            if shipment_number not in completed_shipment_numbers:
                CSVManager.data_list_to_csv(data_list, target_csv_path)
                print()
            else:
                print("This invoice has already been processed. Delete from CSV to reprocess")
                print();

start_console()


