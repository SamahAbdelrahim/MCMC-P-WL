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
import requests  # Added for direct URL download

def wait_for_new_mp4(download_dir, before_files, timeout=180):
    """Wait for a new .mp4 file to appear in the download directory."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        current_files = set(os.listdir(download_dir))
        new_files = current_files - before_files
        mp4_files = [f for f in new_files if f.lower().endswith('.mp4')]
        if mp4_files:
            return mp4_files[0]  # Return the new file name
        time.sleep(1)  # Check every second
    raise TimeoutError("Timed out waiting for .mp4 file to appear.")

def convert_stl_to_mp4(stl_files):
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
                time.sleep(5)

                abs_path = os.path.abspath(stl_file)
                if not os.path.exists(abs_path):
                    print(f"Error: File not found - {abs_path}")
                    continue

                print(f"File exists at: {abs_path}")

                # Upload file and wait for processing
                try:
                    file_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "le"))
                    )
                    file_input.send_keys(abs_path)
                    print("File uploaded, waiting for processing...")
                    time.sleep(45)  # Increased wait time after upload
                    
                except Exception as e:
                    print(f"Error uploading file: {str(e)}")
                    continue

                # Click the download button to open format options
                try:
                    # Wait for the download button to be visible first
                    download_button = WebDriverWait(driver, 600).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'span.lj.gp'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                    time.sleep(2)
                    driver.execute_script("arguments[0].click();", download_button)
                    print("Opened download options...")
                    time.sleep(5)

                    # Select MP4 format with explicit waits
                    format_select = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'select.b'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", format_select)
                    time.sleep(3)
                    driver.execute_script("arguments[0].click();", format_select)
                    time.sleep(3)
                    
                    # Find and select MP4 option
                    mp4_option = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'option[value="mp4"]'))
                    )
                    mp4_option.click()
                    print("Selected MP4 format...")
                    time.sleep(3)

                    # Click the convert button with explicit wait
                    convert_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.i'))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", convert_button)
                    time.sleep(3)
                    driver.execute_script("arguments[0].click();", convert_button)
                    print("Clicked convert button...")
                    time.sleep(10)

                    # Get the download URL from the final download button
                    final_download = WebDriverWait(driver, 300).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'a.ja'))
                    )
                    download_url = final_download.get_attribute('href')
                    print(f"Got download URL: {download_url}")

                    # Download the file using requests
                    print("Starting direct download...")
                    response = requests.get(download_url)
                    if response.status_code != 200:
                        raise Exception(f"Download failed with status code: {response.status_code}")

                    # Save the file
                    new_name = os.path.splitext(os.path.basename(stl_file))[0] + '.mp4'
                    new_path = os.path.join(download_dir, new_name)
                    
                    with open(new_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Successfully downloaded and saved as: {new_name}")

                    # Wait before next file
                    time.sleep(15)

                except Exception as e:
                    print(f"Error during conversion/download: {str(e)}")
                    print("Full error details:", str(e))
                    continue

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