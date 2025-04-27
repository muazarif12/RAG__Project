import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

class HadithScraper:
    def __init__(self, save_folder="data/hadith_texts"):
        self.SAVE_FOLDER = save_folder
        os.makedirs(self.SAVE_FOLDER, exist_ok=True)
        
        self.urls = [
            ("bukhari_5", "https://sunnah.com/bukhari/5"),
            ("bukhari_1", "https://sunnah.com/bukhari/1"),
            ("bukhari_2", "https://sunnah.com/bukhari/2"),
            ("bukhari_3", "https://sunnah.com/bukhari/3"),
            ("bukhari_4", "https://sunnah.com/bukhari/4"),
            ("bukhari_6", "https://sunnah.com/bukhari/6"),
            ("bukhari_7", "https://sunnah.com/bukhari/7"),
            ("bukhari_8", "https://sunnah.com/bukhari/8"),
            ("bukhari_9", "https://sunnah.com/bukhari/9"),
            ("bukhari_10", "https://sunnah.com/bukhari/10"),
            ("bukhari_11", "https://sunnah.com/bukhari/11"),
            ("bukhari_12", "https://sunnah.com/bukhari/12"),
            ("bukhari_13", "https://sunnah.com/bukhari/13"),
            ("bukhari_14", "https://sunnah.com/bukhari/14"),
            ("bukhari_15", "https://sunnah.com/bukhari/15"),
            ("bukhari_16", "https://sunnah.com/bukhari/16"),
            ("bukhari_18", "https://sunnah.com/bukhari/18"),
            # Add all other URLs here
        ]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_single_url(self, url_data):
        name, url = url_data
        output_file = os.path.join(self.SAVE_FOLDER, f"{name}_english.txt")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            english_text = ""
            main_containers = soup.find_all('div', class_='actualHadithContainer')
            
            if not main_containers:
                return
                
            for container in main_containers:
                # Your existing scraping logic here
                # Find the hadith text container
                text_container = container.find('div', class_='hadithTextContainers')
                if not text_container:
                    continue

                # Find the english container
                english_container = text_container.find('div', class_='englishcontainer')
                if not english_container:
                    continue

                # Extract narrator and hadith text
                narrator = english_container.find('div', class_='hadith_narrated')
                text_details = english_container.find('div', class_='text_details')

                # Extract reference
                reference = container.find('div', class_='hadith_reference')
                ref_text = reference.get_text(strip=True) if reference else "Reference not available"

                # Extract hadith number
                number = container.find('div', class_='hadith_number')
                num_text = number.get_text(strip=True) if number else ""

                # Format the output
                english_text += "="*50 + "\n"
                if narrator:
                    english_text += "Narrator: " + narrator.get_text(strip=True) + "\n\n"
                if text_details:
                    english_text += "Hadith: " + text_details.get_text(strip=True) + "\n\n"
                english_text += f"Reference: {ref_text} {num_text}\n\n"
                
                pass
                
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(english_text)
                
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

    def scrape_all_urls(self):
        print(f"Starting scraping. Saving files to: {self.SAVE_FOLDER}")
        with ThreadPoolExecutor(max_workers=5) as executor:
            list (tqdm(executor.map(self.scrape_single_url, self.urls), total=len(self.urls)))
        print("All scraping completed!")

