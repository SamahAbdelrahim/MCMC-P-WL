import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import random
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

def convert_stl_to_mp4(stl_files):
    # Set up Chrome options with custom download directory
    chrome_options = webdriver.ChromeOptions()
    download_dir = os.path.join(os.getcwd(), 'mp4_outputs')
    os.makedirs(download_dir, exist_ok=True)
    
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        for stl_file in stl_files:
            try:
                print(f"\nProcessing file: {os.path.basename(stl_file)}")
                
                driver.get('https://imagetostl.com/convert/file/stl/to/mp4')
                time.sleep(5)  # Give time to load page

                abs_path = os.path.abspath(stl_file)
                if not os.path.exists(abs_path):
                    print(f"Error: File not found - {abs_path}")
                    continue

                print(f"File exists at: {abs_path}")

                # Upload file
                try:
                    file_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "le"))
                    )
                    file_input.send_keys(abs_path)
                except Exception as e:
                    print(f"Error uploading file: {str(e)}")
                    continue
                
                print("File uploaded. Waiting for conversion...")

                # Now wait for the download button to become clickable
                try:
                    download_button = WebDriverWait(driver, 600).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'span.lj.gp'))
                    )
                    download_button.click()
                except Exception as e:
                    print(f"Error finding or clicking download button: {str(e)}")
                    continue

                print(f"Waiting for download to complete for {os.path.basename(stl_file)}")
                time.sleep(30)  # Wait time for download to finish

            except Exception as e:
                print(f"Error processing {stl_file}: {str(e)}")
                
    except Exception as e:
        print(f"Critical error setting up ChromeDriver: {str(e)}")
    
    finally:
        try:
            driver.quit()
        except:
            pass


def get_stl_files_from_csv(sample_size=2):
    stl_files = []
    with open('stimulus_database.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            stl_file = row['stl_file']
            if os.path.exists(stl_file):
                stl_files.append(stl_file)
    
    # Randomly select sample_size files
    if len(stl_files) > sample_size:
        stl_files = random.sample(stl_files, sample_size)
    
    return stl_files

if __name__ == "__main__":
    # Get list of random STL files from the CSV
    stl_files = get_stl_files_from_csv(sample_size=2)
    print(f"Selected {len(stl_files)} random STL files to convert:")
    for file in stl_files:
        print(f"- {os.path.basename(file)}")
    
    # Convert selected files
    convert_stl_to_mp4(stl_files)