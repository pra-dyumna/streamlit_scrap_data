
import requests
from bs4 import BeautifulSoup
import re
import time
import random
import pandas as pd
from urllib.parse import urlparse, urljoin
from langchain_community.document_loaders import WebBaseLoader
import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
]

# location_map = {
#     "usa": "us", "uk": "uk", "india": "in", "canada": "ca", "australia": "au"
# }

# def get_driver():
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("start-maximized")
#     options.add_argument("disable-infobars")
#     options.add_argument("--disable-extensions")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_argument(f"user-agent={random.choice(user_agents)}")
#     return webdriver.Chrome(options=options)

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

location_map = {
    "usa": "us",
    "uk": "uk",
    "india": "in",
    "canada": "ca",
    "australia": "au",
}

# def search_google(query, location="usa", num_results=10):
#     gl = location_map.get(location.lower(), "us")
#     urls = []
#     driver = get_driver()
#     try:
#         print("🔍 Google search...")
#         google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}&gl={gl}"
#         driver.get(google_url)
#         time.sleep(random.uniform(2, 5))
#         links = driver.find_elements(By.XPATH, '//a[@href]')
#         for link in links:
#             href = link.get_attribute("href")
#             if href and "/url?q=" in href:
#                 actual_url = href.split("/url?q=")[1].split("&")[0]
#                 domain = urlparse(actual_url).netloc
#                 urls.append((actual_url, domain))
#     except Exception as e:
#         print(f"❌ Google error: {e}")
#     driver.quit()
#     return urls


def search_google(query, location="usa", num_results=10):
    gl = location_map.get(location.lower(), "us")
    urls = []
    seen_urls = set()
    driver = get_driver()
    try:
        print("🔍 Google search...")
        google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num={num_results}&gl={gl}"
        driver.get(google_url)
        time.sleep(random.uniform(2, 5))

        links = driver.find_elements(By.XPATH, '//a[@href]')
        for link in links:
            href = link.get_attribute("href")
            if href and "/url?q=" in href:
                actual_url = href.split("/url?q=")[1].split("&")[0]
                if actual_url and actual_url not in seen_urls:
                    seen_urls.add(actual_url)
                    domain = urlparse(actual_url).netloc
                    urls.append((actual_url, domain))
    except Exception as e:
        print(f"❌ Google error: {e}")
    driver.quit()
    return urls

# def search_bing(query, location="usa", num_results=10):
#     urls = []
#     driver = get_driver()
#     try:
#         print("🔍 Bing search...")
#         bing_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}&count={num_results}"
#         driver.get(bing_url)
#         time.sleep(random.uniform(2, 5))
#         links = driver.find_elements(By.XPATH, '//li[@class="b_algo"]//h2/a')
#         for link in links:
#             href = link.get_attribute("href")
#             if href:
#                 actual_url = href
#                 domain = urlparse(actual_url).netloc
#                 urls.append((actual_url, domain))
#     except Exception as e:
#         print(f"❌ Bing error: {e}")
#     driver.quit()
#     return urls


def search_bing(query, location="usa", num_results=10):
    urls = []
    seen_urls = set()
    driver = get_driver()
    try:
        print("🔍 Bing search...")
        bing_url = f"https://www.bing.com/search?q={query.replace(' ', '+')}&count={num_results}"
        driver.get(bing_url)
        time.sleep(random.uniform(2, 5))

        links = driver.find_elements(By.XPATH, '//li[@class="b_algo"]//h2/a')
        for link in links:
            href = link.get_attribute("href")
            if href and href not in seen_urls:
                seen_urls.add(href)
                domain = urlparse(href).netloc
                urls.append((href, domain))
    except Exception as e:
        print(f"❌ Bing error: {e}")
    driver.quit()
    return urls





def search_duckduckgo(query, location="usa", num_results=10):
    gl = location_map.get(location.lower(), "us")
    urls = []
    driver = get_driver()
    try:
        print("🔍 DuckDuckGo search...")
        duck_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&kl={gl}-en"
        driver.get(duck_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="result__a"]'))
        )
        time.sleep(random.uniform(2, 5))
        links = driver.find_elements(By.XPATH, '//a[@class="result__a"]')
        for link in links[:num_results]:
            href = link.get_attribute("href")
            if href:
                actual_url = href
                domain = urlparse(actual_url).netloc
                urls.append((actual_url, domain))
    except Exception as e:
        print(f"❌ DuckDuckGo error: {e}")
    driver.quit()
    return urls


# def extract_info_with_langchain(url):
#     try:
#         # Step 1: Use LangChain to extract text from URL
#         loader = WebBaseLoader(url)
#         docs = loader.load()
#         text = docs[0].page_content if docs else ""

#         # Step 2: Extract emails
#         emails = set(re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text))
#         email = ""
#         for e in emails:
#             if any(x in e.lower() for x in ["contact", "", "support", "email", "mail to"]):
#                 email = e
#                 break
#         if not email and emails:
#             email = list(emails)[0]

#         # Step 3: Extract phone numbers
#         phones = re.findall(r"(\+?\d[\d\s().-]{6,20}\d)", text)
#         phone = ""
#         valid_phones = []
#         for ph in phones:
#             clean = re.sub(r"\D", "", ph)
#             if 9 <= len(clean) <= 12:
#                 valid_phones.append(ph)
#         if valid_phones:
#             phone = valid_phones[0]

#         # Step 4: Try to find contact page from metadata or content
#         # Since LangChain's loader does not give anchor tags, you can still do a fallback fetch:
#         from bs4 import BeautifulSoup
#         import requests

#         contact_url = ""
#         try:
#             page = requests.get(url, timeout=10)
#             soup = BeautifulSoup(page.text, "html.parser")
#             for a in soup.find_all("a", href=True):
#                 href = a["href"].lower()
#                 if "contact" in href and not href.startswith("mailto:"):
#                     contact_url = urljoin(url, href)
#                     break
#         except:
#             pass

#         return {
#             "Website URL": url,
#             "Phone Number": phone,
#             "Email Address": email,
#             "Contact Us": contact_url,
#             "Error": ""
#         }

#     except Exception as e:
#         return {
#             "Website URL": url,
#             "Phone Number": "",
#             "Email Address": "",
#             "Contact Us": "",
#             "Error": str(e)
#         }
    

def extract_info_from_page(url):
    headers = {"User-Agent": random.choice(user_agents)}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"Website URL": url, "Error": f"HTTP {response.status_code}"}

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=' ', strip=True)

        # Extract emails
        emails = set()

        # Match standard and slightly obfuscated email formats from text
        raw_emails = re.findall(r"[a-zA-Z0-9_.+-]+(?:\s*\[?@(?:at)?\]?\s*|\s*@\s*)[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+", text)

        for e in raw_emails:
            cleaned = e.replace("[at]", "@").replace("(at)", "@").replace(" at ", "@").replace(" AT ", "@")
            cleaned = re.sub(r"\s+", "", cleaned)
            emails.add(cleaned)

        # Also extract emails from <a href="mailto:..."> links
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            if "mailto:" in href:
                email = href.split("mailto:")[1].split("?")[0].strip()
                emails.add(email)

        # Prioritize emails with common useful keywords
        priority_keywords = ["contact", "info", "support", "hello", "admin", "team", "mail", "email", "help", "service"]

        email = ""
        for e in emails:
            if any(k in e.lower() for k in priority_keywords):
                email = e
                break

# Fallback to first found email
        if not email and emails:
            email = list(emails)[0]

                # Extract phone numbers
        phones = re.findall(r"(\+?\d[\d\s().-]{6,20}\d)", text)
        phone = ""
        valid_phones = []
        for ph in phones:
            clean = re.sub(r"\D", "", ph)
            if 8 <= len(clean) <= 12:
                valid_phones.append(ph)
        if valid_phones:
            phone = valid_phones[0]

        # Find contact page
        contact_url = ""
        for a in soup.find_all("a", href=True):
            href = a["href"].lower()
            if "contact" in href and not href.startswith("mailto:"):
                contact_url = urljoin(url, href)
                break

        return {
            "Website URL": url,
            "Phone Number": phone,
            "Email Address": email,
            "Contact Us": contact_url,
           
        }

    except Exception as e:
        return {
            "Website URL": url,
            "Phone Number": "",
            "Email Address": "",
            "Contact Us": "",
            
        }



def search_and_extract(query, location="usa", num_results=10):

    g_urls = search_google(query, location, num_results)
    print(f"Google URLs: {g_urls}")

    # Step 2: If Google returned no results, fallback to Bing
    if not g_urls:
        b_urls = search_bing(query, location, num_results)  # Make sure Bing accepts 3 args
        print(f"Bing URLs: {b_urls}")
        urls = b_urls if b_urls else []
    else:
        urls = g_urls

    data = []

    for url, _ in urls:
        info = extract_info_from_page(url)
        print(f"Extracted info: {info}")
        
        # Ensure all fields are present and not NaN
        clean_info = {
            "Website URL": info.get("Website URL", url),
            "Phone Number": info.get("Phone Number", ""),
            "Email Address": info.get("Email Address", ""),
            "Contact Us": info.get("Contact Us", "")
        }
        
        data.append(clean_info)
        time.sleep(random.uniform(2, 3))
    
    # Convert to DataFrame at the end if needed
    return pd.DataFrame(data) if data else pd.DataFrame()
