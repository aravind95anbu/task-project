import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import re
import os

class BusinessScraper:
    def __init__(self, headless=False):
        """Initialize the business scraper"""
        self.options = Options()
        if headless:
            self.options.add_argument("--headless")
        
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
    def scrape_businesses_comprehensive(self, location, business_type, max_results=25):
        """Comprehensive business scraping for startups, manufacturing, and consultants"""
        driver = webdriver.Chrome(options=self.options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        all_businesses = []
        all_urls = set()
        
        try:
            # Define search terms based on business type
            search_terms = self.get_search_terms(business_type, location)
            
            for search_term in search_terms:
                try:
                    print(f"\n🔍 Searching: {search_term}")
                    
                    driver.get("https://www.google.com/maps")
                    time.sleep(3)
                    
                    search_box = WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable((By.ID, "searchboxinput"))
                    )
                    search_box.clear()
                    search_box.send_keys(search_term)
                    search_box.send_keys(Keys.ENTER)
                    time.sleep(5)
                    
                    urls = self.enhanced_url_collection(driver, max_results)
                    new_urls = [url for url in urls if url not in all_urls]
                    all_urls.update(new_urls)
                    
                    print(f"   Found {len(new_urls)} new business URLs")
                    
                    if len(all_urls) >= max_results:
                        break
                        
                except Exception as e:
                    print(f"   Error with search term '{search_term}': {e}")
                    continue
            
            print(f"\n📊 Total unique business URLs collected: {len(all_urls)}")
            
            url_list = list(all_urls)[:max_results]
            
            for i, url in enumerate(url_list):
                try:
                    print(f"\n📍 Processing business {i+1}/{len(url_list)}...")
                    driver.get(url)
                    time.sleep(4)
                    
                    business_data = self.extract_complete_business_data(driver)
                    
                    if business_data and business_data.get('name') and business_data['name'] != 'Results':
                        business_data['business_type'] = business_type
                        all_businesses.append(business_data)
                        print(f"   ✅ {business_data['name']}")
                        
                        if business_data.get('phone'):
                            print(f"      📞 {business_data['phone']}")
                        if business_data.get('address'):
                            address_preview = business_data['address'][:50] + "..." if len(business_data['address']) > 50 else business_data['address']
                            print(f"      📍 {address_preview}")
                        if business_data.get('rating'):
                            print(f"      ⭐ {business_data['rating']} ({business_data.get('reviews_count', 'N/A')})")
                        if business_data.get('website'):
                            print(f"      🌐 {business_data['website']}")
                        else:
                            print(f"      🌐 No website found")
                    else:
                        print(f"   ❌ Failed to extract valid data")
                    
                except Exception as e:
                    print(f"   ❌ Error processing business {i+1}: {e}")
                    continue
            
            return all_businesses
            
        except Exception as e:
            print(f"Error in comprehensive scraping: {e}")
            return []
        finally:
            driver.quit()
    
    def get_search_terms(self, business_type, location):
        """Get search terms based on business type"""
        base_terms = {
            'startup': [
                f"startup companies {location}",
                f"tech startups {location}",
                f"new businesses {location}",
                f"emerging companies {location}",
                f"startup incubator {location}",
                f"software companies {location}"
            ],
            'manufacturing': [
                f"manufacturing companies {location}",
                f"factories {location}",
                f"industrial companies {location}",
                f"production companies {location}",
                f"textile manufacturers {location}",
                f"auto parts manufacturers {location}",
                f"pharmaceutical manufacturers {location}"
            ],
            'consultant': [
                f"business consultants {location}",
                f"management consultants {location}",
                f"consulting firms {location}",
                f"business advisory {location}",
                f"strategy consultants {location}",
                f"IT consultants {location}",
                f"financial consultants {location}"
            ]
        }
        
        return base_terms.get(business_type, [f"{business_type} {location}"])
    
    def enhanced_url_collection(self, driver, target_count):
        """Enhanced URL collection with aggressive scrolling"""
        business_urls = []
        time.sleep(5)
        
        scroll_attempts = 0
        max_scroll_attempts = 15
        last_count = 0
        stagnant_scrolls = 0
        
        while scroll_attempts < max_scroll_attempts and len(business_urls) < target_count:
            links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")
            
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if href and href not in business_urls:
                        business_urls.append(href)
                except:
                    continue
            
            if len(business_urls) == last_count:
                stagnant_scrolls += 1
                if stagnant_scrolls >= 5:
                    break
            else:
                stagnant_scrolls = 0
                last_count = len(business_urls)
            
            try:
                results_panel = driver.find_element(By.CSS_SELECTOR, "[role='main']")
                driver.execute_script("arguments[0].scrollTop += 500;", results_panel)
                time.sleep(2)
                
                feed = driver.find_element(By.CSS_SELECTOR, "[role='feed']")
                driver.execute_script("arguments[0].scrollTop += 500;", feed)
                time.sleep(1)
                
            except:
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(2)
            
            scroll_attempts += 1
            
            if scroll_attempts % 3 == 0:
                print(f"   Scrolling... found {len(business_urls)} URLs so far")
        
        return business_urls
    
    def extract_complete_business_data(self, driver):
        """Extract complete business data"""
        business_data = {
            'name': '',
            'address': '',
            'phone': '',
            'email': '',
            'website': '',
            'rating': '',
            'reviews_count': '',
            'category': '',
            'business_type': '',
            'hours': '',
            'description': ''
        }
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            time.sleep(3)
            
            # --- COMPANY NAME ---
            name_selectors = [
                "h1.DUwDvf",
                "h1.x3AX1-LfntMc-header-title-title", 
                "h1",
                ".qrShPb",
                ".x3AX1-LfntMc-header-title-title"
            ]
            for selector in name_selectors:
                try:
                    name_element = driver.find_element(By.CSS_SELECTOR, selector)
                    name_text = name_element.text.strip()
                    if name_text and len(name_text) > 1:
                        business_data['name'] = name_text
                        break
                except:
                    continue
            
            # --- ADDRESS ---
            address_selectors = [
                "button[data-item-id='address'] .Io6YTe",
                "button[data-item-id='address'] span",
                "[data-item-id='address'] .Io6YTe",
                "button[aria-label*='Address'] .fontBodyMedium",
                ".rogA2c[data-item-id='address']"
            ]
            for selector in address_selectors:
                try:
                    address_element = driver.find_element(By.CSS_SELECTOR, selector)
                    address_text = address_element.text.strip()
                    if address_text and len(address_text) > 10:
                        business_data['address'] = address_text
                        break
                except:
                    continue
            
            # --- PHONE ---
            phone_selectors = [
                "button[data-item-id*='phone'] .Io6YTe",
                "button[data-item-id*='phone'] span",
                "a[href^='tel:']",
                "button[aria-label*='phone'] .fontBodyMedium",
                "span[dir='ltr']"
            ]
            for selector in phone_selectors:
                try:
                    phone_element = driver.find_element(By.CSS_SELECTOR, selector)
                    if phone_element.tag_name.lower() == 'a':
                        href = phone_element.get_attribute('href')
                        if href and href.startswith('tel:'):
                            business_data['phone'] = href.replace('tel:', '').strip()
                            break
                    else:
                        phone_text = phone_element.text.strip()
                        if phone_text and re.search(r'[\+\d\s\-\(\)]{8,}', phone_text):
                            business_data['phone'] = phone_text
                            break
                except:
                    continue
            
            # --- EMAIL ---
            try:
                # Look for mailto links
                mailto_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href^="mailto:"]')
                if mailto_elements:
                    href = mailto_elements[0].get_attribute('href')
                    business_data['email'] = href.replace('mailto:', '').strip()
                else:
                    # Look for email in text content
                    page_text = driver.find_element(By.TAG_NAME, 'body').text
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    email_matches = re.findall(email_pattern, page_text)
                    if email_matches:
                        for email in email_matches:
                            if not any(skip in email.lower() for skip in ['noreply', 'support@google', 'maps@google']):
                                business_data['email'] = email
                                break
            except:
                pass
            
            # --- WEBSITE ---
            website = self.extract_website_enhanced(driver)
            if website:
                business_data['website'] = website
            
            # --- RATING & REVIEWS ---
            rating, reviews_count = self.extract_rating_and_reviews(driver)
            if rating:
                business_data['rating'] = rating
            if reviews_count:
                business_data['reviews_count'] = reviews_count
            
            # --- CATEGORY/TYPE ---
            category_selectors = [
                "button[jsaction*='pane.category'] .DkEaL",
                ".DkEaL",
                ".YhemCb"
            ]
            for selector in category_selectors:
                try:
                    category_element = driver.find_element(By.CSS_SELECTOR, selector)
                    category_text = category_element.text.strip()
                    if category_text and len(category_text) < 100:
                        business_data['category'] = category_text
                        break
                except:
                    continue
            
            # --- BUSINESS HOURS ---
            try:
                hours_selectors = [
                    "button[data-item-id='oh'] .Io6YTe",
                    "button[aria-label*='Hours'] .fontBodyMedium",
                    ".t39EBf .G8aQO"
                ]
                for selector in hours_selectors:
                    try:
                        hours_element = driver.find_element(By.CSS_SELECTOR, selector)
                        hours_text = hours_element.text.strip()
                        if hours_text:
                            business_data['hours'] = hours_text
                            break
                    except:
                        continue
            except:
                pass
            
            # --- DESCRIPTION/ABOUT ---
            try:
                description_selectors = [
                    ".PYvSYb",
                    ".lI9IFe .fontBodyMedium",
                    "[data-attrid='description']"
                ]
                for selector in description_selectors:
                    try:
                        desc_element = driver.find_element(By.CSS_SELECTOR, selector)
                        desc_text = desc_element.text.strip()
                        if desc_text and len(desc_text) > 20:
                            business_data['description'] = desc_text[:200] + "..." if len(desc_text) > 200 else desc_text
                            break
                    except:
                        continue
            except:
                pass
                
        except Exception as e:
            print(f"      Error extracting business details: {e}")
            
        return business_data
    
    def extract_rating_and_reviews(self, driver):
        """Enhanced rating and review extraction"""        
        rating = ""
        reviews_count = ""
        
        # Rating extraction
        rating_selectors = [
            ".MW4etd", "span.ceNzKf", ".fontDisplayLarge", "[data-value]",
            ".Ob2kfd .ceNzKf", "div[role='img'][aria-label*='star']", 
            "span[aria-label*='star']"
        ]
        
        for selector in rating_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        text = element.text.strip()
                        if text and self.looks_like_rating(text):
                            rating = text
                            break
                        
                        aria_label = element.get_attribute('aria-label')
                        if aria_label:
                            rating_match = re.search(r'(\d+\.?\d*)\s*(?:out of|stars?|star rating)', aria_label.lower())
                            if rating_match:
                                rating = rating_match.group(1)
                                break
                        
                        data_value = element.get_attribute('data-value')
                        if data_value and self.looks_like_rating(data_value):
                            rating = data_value
                            break
                            
                    except Exception:
                        continue
                        
                if rating:
                    break
                    
            except Exception:
                continue
        
        # Reviews count extraction
        review_selectors = [
            "button[aria-label*='review']", "span[aria-label*='review']", 
            "a[href*='review']", ".UY7F9"
        ]
        
        for selector in review_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        text = element.text.strip()
                        if 'review' in text.lower():
                            number_match = re.search(r'(\d+(?:,\d+)*)\s*review', text.lower())
                            if number_match:
                                reviews_count = number_match.group(1)
                                break
                        
                        aria_label = element.get_attribute('aria-label')
                        if aria_label and 'review' in aria_label.lower():
                            number_match = re.search(r'(\d+(?:,\d+)*)\s*review', aria_label.lower())
                            if number_match:
                                reviews_count = number_match.group(1)
                                break
                                
                    except Exception:
                        continue
                        
                if reviews_count:
                    break
                    
            except Exception:
                continue
            
        return rating, reviews_count
    
    def looks_like_rating(self, text):
        """Check if text looks like a rating"""
        if not text:
            return False
        
        try:
            text = str(text).strip()
            float_val = float(text)
            return 0.0 <= float_val <= 10.0 and len(text) <= 5
        except (ValueError, TypeError):
            return False
    
    def extract_website_enhanced(self, driver):
        """Enhanced website extraction"""
        try:
            time.sleep(3)
            
            website_selectors = [
                'a[data-item-id="authority"]',
                'button[data-item-id="authority"]',
                'a[data-value="Website"]',
                'a[href^="http"]:not([href*="google"]):not([href*="maps"])',
                'button[aria-label*="Website"]',
                '.CsEnBe a'
            ]
            
            for selector in website_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.tag_name.lower() == 'a':
                            href = element.get_attribute('href')
                            if href and not self._is_google_url(href):
                                return href
                        else:
                            text_content = element.text.lower()
                            if 'website' in text_content:
                                try:
                                    original_window = driver.current_window_handle
                                    driver.execute_script("arguments[0].click();", element)
                                    time.sleep(3)
                                    
                                    if len(driver.window_handles) > 1:
                                        driver.switch_to.window(driver.window_handles[-1])
                                        current_url = driver.current_url
                                        if not self._is_google_url(current_url):
                                            website_url = current_url
                                            driver.close()
                                            driver.switch_to.window(original_window)
                                            return website_url
                                        driver.close()
                                        driver.switch_to.window(original_window)
                                except Exception:
                                    continue
                except Exception:
                    continue
            
            # Look for domain names in page text
            try:
                page_text = driver.find_element(By.TAG_NAME, "body").text
                domain_patterns = [
                    r'\b[a-zA-Z0-9-]+\.com\b', r'\b[a-zA-Z0-9-]+\.in\b',
                    r'\b[a-zA-Z0-9-]+\.org\b', r'\b[a-zA-Z0-9-]+\.net\b'
                ]

                for pattern in domain_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    for match in matches:
                        if not any(skip in match.lower() for skip in ['google', 'maps', 'schema', 'android']):
                            website_url = 'https://' + match.lower()
                            if self._is_likely_business_website(website_url):
                                return website_url
            except:
                pass
                    
        except Exception as e:
            print(f"Error extracting website: {e}")
        
        return None
    
    def _is_google_url(self, url):
        """Check if URL is a Google service URL"""
        if not url:
            return True
            
        google_domains = [
            'google.com', 'google.co.in', 'googleapis.com',
            'gstatic.com', 'googleusercontent.com', 'maps.google'
        ]
        return any(domain in url.lower() for domain in google_domains)
    
    def _is_likely_business_website(self, url):
        """Check if URL looks like a business website"""
        if not url:
            return False
            
        avoid_domains = [
            'facebook.com', 'twitter.com', 'instagram.com', 
            'youtube.com', 'linkedin.com'
        ]
        
        for domain in avoid_domains:
            if domain in url.lower():
                return False
        
        return True
    
    def save_business_csv(self, businesses, filename, business_type):
        """Save business data to CSV with enhanced formatting and prominent path display"""
        if not businesses:
            print("❌ No business data to save")
            return 0
            
        valid_businesses = []
        for business in businesses:
            if (business.get('name') and 
                business['name'] not in ['Results', ''] and 
                len(business['name']) > 2):
                valid_businesses.append(business)
        
        if not valid_businesses:
            print("❌ No valid business data found after filtering")
            return 0
            
        df = pd.DataFrame(valid_businesses)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        
        # Enhanced CSV path display
        file_path = os.path.abspath(filename)
        file_size = os.path.getsize(filename)
        file_size_kb = file_size / 1024
        
        print(f"\n{'='*80}")
        print(f"💾 CSV FILE SAVED SUCCESSFULLY!")
        print(f"{'='*80}")
        print(f"📁 FILE PATH: {file_path}")
        print(f"📊 FILE SIZE: {file_size_kb:.2f} KB ({file_size} bytes)")
        print(f"📄 FILENAME: {filename}")
        print(f"🗂️  DIRECTORY: {os.path.dirname(file_path)}")
        print(f"{'='*80}")
        
        print(f"\n🎉 SUCCESSFULLY EXTRACTED {len(valid_businesses)} {business_type.upper()} COMPANIES")
        
        # Statistics
        with_website = sum(1 for b in valid_businesses if b.get('website'))
        with_phone = sum(1 for b in valid_businesses if b.get('phone'))
        with_email = sum(1 for b in valid_businesses if b.get('email'))
        with_rating = sum(1 for b in valid_businesses if b.get('rating'))
        
        print(f"📞 Phone numbers: {with_phone}/{len(valid_businesses)} ({with_phone/len(valid_businesses)*100:.1f}%)")
        print(f"📧 Email addresses: {with_email}/{len(valid_businesses)} ({with_email/len(valid_businesses)*100:.1f}%)")
        print(f"🌐 Websites: {with_website}/{len(valid_businesses)} ({with_website/len(valid_businesses)*100:.1f}%)")
        print(f"⭐ Ratings: {with_rating}/{len(valid_businesses)} ({with_rating/len(valid_businesses)*100:.1f}%)")
        
        # Sample data display
        print(f"\n📋 SAMPLE {business_type.upper()} DATA:")
        for i, business in enumerate(valid_businesses[:5], 1):
            print(f"\n{i}. 🏢 {business['name']}")
            if business.get('category'):
                print(f"   🏷️  Category: {business['category']}")
            if business.get('address'):
                print(f"   📍 Address: {business['address']}")
            if business.get('phone'):
                print(f"   📞 Phone: {business['phone']}")
            if business.get('email'):
                print(f"   📧 Email: {business['email']}")
            if business.get('website'):
                print(f"   🌐 Website: {business['website']}")
            if business.get('rating'):
                rating_display = business['rating']
                if business.get('reviews_count'):
                    rating_display += f" ({business['reviews_count']} reviews)"
                print(f"   ⭐ Rating: {rating_display}")
        
        # Final path reminder
        print(f"\n🔗 CSV FILE LOCATION: {file_path}")
        print(f"📋 You can open this file in Excel, Google Sheets, or any CSV viewer")
                
        return len(valid_businesses)

def scrape_business_type(business_type, location, max_results=25):
    """Main function to scrape specific business type"""
    scraper = BusinessScraper(headless=False)
    
    print(f"\n🚀 Starting {business_type} scraping in {location}")
    print(f"📊 Target: {max_results} businesses")
    
    businesses = scraper.scrape_businesses_comprehensive(location, business_type, max_results)
    
    if businesses:
        filename = f'{business_type}_{location.replace(" ", "_").replace(",", "").lower()}_businesses.csv'
        valid_count = scraper.save_business_csv(businesses, filename, business_type)
        return businesses
    else:
        print(f"❌ No {business_type} businesses found")
        return []

def main():
    print("🔧 Google Maps Business Scraper")
    print("=" * 50)
    print("Business Types Available:")
    print("1. Startup Companies")
    print("2. Manufacturing Companies") 
    print("3. Business Consultants")
    print("4. All Three Types")
    
    choice = input("\nChoose business type (1-4, default=1): ").strip() or "1"
    location = input("Enter location (e.g., 'Chennai Tamil Nadu'): ")
    max_results = int(input("Max results per type (default=25): ") or "25")
    
    business_types = {
        "1": ["startup"],
        "2": ["manufacturing"], 
        "3": ["consultant"],
        "4": ["startup", "manufacturing", "consultant"]
    }
    
    types_to_scrape = business_types.get(choice, ["startup"])
    
    all_results = {}
    all_file_paths = []
    
    for business_type in types_to_scrape:
        print(f"\n" + "="*60)
        print(f"SCRAPING {business_type.upper()} COMPANIES")
        print(f"="*60)
        
        results = scrape_business_type(business_type, location, max_results)
        all_results[business_type] = results
        
        if results:
            filename = f'{business_type}_{location.replace(" ", "_").replace(",", "").lower()}_businesses.csv'
            all_file_paths.append(os.path.abspath(filename))
        
        print(f"\n✅ Completed {business_type} scraping: {len(results)} businesses found")
        
        # Add delay between business types
        if len(types_to_scrape) > 1:
            time.sleep(10)
    
    # Final Summary with all file paths
    total_businesses = sum(len(results) for results in all_results.values())
    print(f"\n🎉 FINAL SUMMARY:")
    print(f"=" * 60)
    print(f"Total businesses scraped: {total_businesses}")
    
    for business_type, results in all_results.items():
        if results:
            print(f"{business_type.capitalize()}: {len(results)} companies")
    
    if all_file_paths:
        print(f"\n📁 ALL CSV FILES CREATED:")
        print(f"=" * 60)
        for i, file_path in enumerate(all_file_paths, 1):
            print(f"{i}. {file_path}")
        
        print(f"\n🔗 COPY THESE PATHS TO ACCESS YOUR FILES:")
        for file_path in all_file_paths:
            print(file_path)

if __name__ == "__main__":
    main()