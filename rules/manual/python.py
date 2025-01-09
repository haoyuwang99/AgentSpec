import os
import tempfile
import time
from virustotal_python import Virustotal

def scan_python_code(code_string):
    api_key = os.environ["VIRUS_TOTAL_KEY"]
    """
    Scan a Python code string for malware using VirusTotal API.

    Parameters:
    - code_string (str): The Python code as a string.
    - api_key (str): Your VirusTotal API key.

    Returns:
    - str: Result message indicating whether the code is malware.
    """
    # Initialize VirusTotal API
    vtotal = Virustotal(api_key)

    # Create a temporary file to hold the code
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code_string.encode('utf-8'))
        temp_file_path = temp_file.name

    try:
        # Upload and scan the file
        with open(temp_file_path, "rb") as file:
            response = vtotal.file_scan(file)
            scan_id = response["scan_id"]
            print(f"File uploaded successfully. Scan ID: {scan_id}")

        # Wait for scan results (adjust sleep time as needed)
        time.sleep(20)

        # Retrieve the scan results
        result = vtotal.file_report(scan_id)
        positives = result["positives"]
        total = result["total"]

        if positives > 0:
            return f"Malware detected! {positives}/{total} engines flagged the code as suspicious."
        else:
            return "No malware detected. The code seems clean."

    except Exception as e:
        return f"An error occurred: {e}"

    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

# Example usage:
# result = scan_python_code("print('Hello World')", "YOUR_API_KEY")
# print(result)
