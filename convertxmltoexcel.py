import xml.etree.ElementTree as ET
from openpyxl import Workbook

# Step 1: Clean the XML file by escaping special characters
def clean_xml_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Replace problematic characters with their valid XML entities
            clean_line = line.replace('&', '&amp;')  # Only replace '&' since '<' and '>' are part of tags
            outfile.write(clean_line)
    print(f"Cleaned XML saved to {output_file}")

# Step 2: Convert cleaned XML to Excel with namespace handling
def xml_to_excel(xml_file, excel_file):
    # Parse the cleaned XML file with namespace support
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Failed to parse XML file: {e}")
        return

    # Create a new Excel workbook and select the active sheet
    wb = Workbook()
    ws = wb.active

    # Find the rows in the XML
    rows = root.findall(".//ss:Row", namespaces={'ss': 'urn:schemas-microsoft-com:office:spreadsheet'})
    
    if not rows:
        print("No rows found in the XML file.")
        return

    # Extract and write data to Excel
    for row in rows:
        row_data = []
        cells = row.findall("ss:Cell", namespaces={'ss': 'urn:schemas-microsoft-com:office:spreadsheet'})
        for cell in cells:
            data = cell.find("ss:Data", namespaces={'ss': 'urn:schemas-microsoft-com:office:spreadsheet'})
            if data is not None:
                row_data.append(data.text)
            else:
                row_data.append(None)  # Append None if no data element is found

        print(f"Row data: {row_data}")  # Debugging: print each row data
        ws.append(row_data)

    # Save the Excel file
    wb.save(excel_file)
    print(f"Excel file '{excel_file}' has been created successfully.")

# Example usage:
xml_file_path = r'D:\Learning\Face-Recogination\HistoryData.xml'  # Path to your original XML file
cleaned_xml_file_path = r'D:\Learning\Face-Recogination\CleanedHistoryData.xml'  # Path to save the cleaned XML
excel_file_path = r'D:\Learning\Face-Recogination\output.xlsx'  # Path where you want to save the Excel file

# Step 1: Clean the XML file
clean_xml_file(xml_file_path, cleaned_xml_file_path)

# Step 2: Convert the cleaned XML to Excel
xml_to_excel(cleaned_xml_file_path, excel_file_path)
