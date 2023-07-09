# Zoho-Invoice-Processor
A Zoho invoice processor used to convert invoice information (pdf or jpg) to CSV format (to be used in Wave Accounting). Implemented in Python alongside PDF2Image and Py2PDF for PDF data extraction, PyTesseract Optical Character Reader for jpg data extraction and Numpy library for image conversion.

<h1>Modes:</h1>
<ul>
  <li> PDF Reader mode (using Py2PDF - default and suggested mode)</li>
  <li> OCR Mode (using PDF2Image and PyTesseract OCR - lower accuracy) </li>
</ul>

<h1>Preqrequesities:</h1>
<ul>
  <li> Python </li>
  <li> Tesseract installed in environment, and have env path to Tesseract.exe set up (can configure in Configs.py)</li>
  <li> PyPDF2 for default mode
  <li> PDF2Image (for OCR mode), and have env path set up to bin file.
  <li> Numpy (for OCR mode)</li>
</ul>

<h1>Set Up:</h1>
<ol>
  <li> <h2> Source Folder, Sub Folder and .pdf Set Up</h1>
  The source folder should function as the home directory containing all the subfolders that should be part of the invoice processing system. For instance,
  <i>C:\\Users\\Affiq\\Zoho</i> contains the folders 
  <i>C:\\Users\\Affiq\\Zoho\\InvoiceBatch1</i>
  <i>C:\\Users\\Affiq\\InvoiceBatch2</i> 
  Each folder has a number of PDFs that should be processed.
  </li>

  <li> <h2> Configurations </h2>
  Under Configs.py, change the home directory attribute to the path to the Source Folder, and change the tesseract directory attribute to the Tesseract.exe path.
  </li>
  
   <li> <h2> Program Execution </h2>
   Execute the main.py under pythonProject to execute the console.
  </li>
</ol>

<h1>Usage:</h1>
Upon execution of main.py, a console should pop-up. Given the source folder path it correct, the program will then list all folders that are available for invoice
processing. The user is then prompted to type which folder should be processed. Once a folder is selected, the program will search for a CSV file with the same name
as the folder (so InvoiceBatch1 in this instance) - if one exists, it will append to the CSV, if not, a new CSV file will be created. The program will then process
one invoice at a time, and if the invoice number (unique identifier) exists in the CSV file, it will not append to the file. The program will then extract the
information into the CSV file.
