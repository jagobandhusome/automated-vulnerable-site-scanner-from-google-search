import requests
import time
import re
from urllib.parse import urlparse, urlunparse

# Replace with your Google API Key and Custom Search Engine ID
API_KEY = "1122222222222222222222222222222222"
CSE_ID = "11111111111111111111111"

# List of Google Dorks for searching vulnerable WordPress sites
GOOGLE_DORKS = [
    "inurl:wp-login.php",
    "inurl:wp-admin",
    "inurl:wp-content/plugins filetype:php",
    "inurl:wp-content/themes filetype:php",
    "inurl:wp-config.php",
    "inurl:backup filetype:sql OR filetype:zip OR filetype:gz",
    "inurl:error_log \"wordpress\"",
    "inurl:wp-content/debug.log",
    "intitle:\"index of\" \"wp-content\"",
    "inurl:timthumb.php",
    "inurl:revslider.php",
    "inurl:readme.html \"wordpress\"",
    "intitle:\"WordPress *.*.*\""
]

# Define a global set for sites_collected to keep track of the unique URLs
sites_collected = set()

def search_google(query, start_index):
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "start": start_index,
        "num": 10,  # Max results per API call
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        return [item["link"] for item in data.get("items", [])]

    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return []

def normalize_url(url):
    """
    Normalize the URL by ensuring it starts with http:// or https://,
    and stripping any extra parts such as query parameters or fragments.
    """
    parsed_url = urlparse(url)

    # Ensure the URL has a scheme (http:// or https://)
    if not parsed_url.scheme:
        url = 'https://' + url  # Default to https://

    # Reparse the URL with scheme (if added) and strip unnecessary query params and fragments
    parsed_url = urlparse(url)
    
    # Clean the netloc (domain part) and make sure it's in the proper format
    domain = parsed_url.netloc.lower()
    domain = domain.split(':')[0]  # Remove port if present
    
    # Construct a normalized URL with https://
    if not domain.startswith("www."):
        domain = "www." + domain
    
    # Rebuild the full URL
    normalized_url = urlunparse((
        'https',  # Force https scheme
        domain,  # Use the normalized domain
        parsed_url.path,  # Keep the path
        '',  # Remove query params
        '',  # Remove fragments
        ''   # Remove any other components
    ))

    return normalized_url

def is_valid_domain(url):
    """
    Check if the URL is a valid .com domain or relevant WordPress site.
    Exclude known non-relevant domains like forums, discussions, and repositories.
    """
    excluded_keywords = ['github', 'stackoverflow', 'community', 'support', 'forum', 'developer', 'wordpress.org']
    
    # Check if the domain ends with .com (can be expanded with other TLDs)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()
    
    if not domain.endswith('.com'):
        return False
    
    # Exclude non-relevant URLs based on keywords
    for keyword in excluded_keywords:
        if keyword in domain:
            return False
    
    return True

def insert_into_db(urls):
    api_endpoint = "http://localhost/scanmanagement/api_store_direct_login_data.php"
    for url in urls:
        try:
            # Check if the URL is already inserted (avoiding duplicates)
            if url in sites_collected:
                print(f"[!] Duplicate URL found: {url}")
                continue

            payload = {
                "api_key": "f2441e3810rt5612xu018tumsqHT34dd7f8f6995df9",
                "siteaddress": url,
                "stat": 1
            }
            response = requests.post(api_endpoint, data=payload)
            response_data = response.json()
            
            if response_data.get("insertion_status") == 'Added':
                print(f"[+] URL inserted: {url}")
                sites_collected.add(url)  # Add to the set of collected sites
            else:
                print(f"[!] Failed to insert: {url}, Response: {response_data}")
        except Exception as error:
            print(f"[!] Error inserting URL: {url}, Error: {error}")

def main():
    # Get the number of results from the user
    try:
        total_sites_target = int(input("Enter the number of URLs you want to collect: "))
        if total_sites_target <= 0:
            print("[!] Please enter a positive integer.")
            return
    except ValueError:
        print("[!] Invalid input. Please enter a valid integer.")
        return

    max_results_per_query = 100  # Max results to fetch per dork

    for dork in GOOGLE_DORKS:
        print(f"\n[!] Searching for dork: {dork}")
        start_index = 1

        while start_index <= max_results_per_query:
            if len(sites_collected) >= total_sites_target:
                break

            print(f"Fetching results {start_index} to {start_index + 9}...")
            results = search_google(dork, start_index)

            if not results:
                print("[!] No more results or API limit reached.")
                break

            # Filter out non-valid .com domains and subdomains
            filtered_results = []
            for url in results:
                valid_domain = normalize_url(url)  # Normalize the URL
                if valid_domain and valid_domain not in sites_collected and is_valid_domain(valid_domain):
                    sites_collected.add(valid_domain)
                    filtered_results.append(valid_domain)

            # Insert filtered valid URLs into the database
            insert_into_db(filtered_results)

            start_index += 10
            time.sleep(1)  # To avoid hitting rate limits

        if len(sites_collected) >= total_sites_target:
            break

    # Save collected sites to a file
    with open("vulnerable_sites.txt", "w") as file:
        file.write("\n".join(sites_collected))

    print(f"\n[+] Collected {len(sites_collected)} unique sites.")
    print("Results saved to vulnerable_sites.txt")

if __name__ == "__main__":
    main()


# import requests  working
# import time

# # Replace with your Google API Key and Custom Search Engine ID
# API_KEY = "AIzaSyDNm5ZunFGOYUxVm2zUiBLE4izXIZhJ0x8"
# CSE_ID = "666b716c0785b40b3"

# # List of Google Dorks for searching vulnerable WordPress sites
# GOOGLE_DORKS = [
#     "inurl:wp-login.php",
#     "inurl:wp-admin",
#     "inurl:wp-content/plugins filetype:php",
#     "inurl:wp-content/themes filetype:php",
#     "inurl:wp-config.php",
#     "inurl:backup filetype:sql OR filetype:zip OR filetype:gz",
#     "inurl:error_log \"wordpress\"",
#     "inurl:wp-content/debug.log",
#     "intitle:\"index of\" \"wp-content\"",
#     "inurl:timthumb.php",
#     "inurl:revslider.php",
#     "inurl:readme.html \"wordpress\"",
#     "intitle:\"WordPress *.*.*\""
# ]

# def search_google(query, start_index):
#     base_url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         "key": API_KEY,
#         "cx": CSE_ID,
#         "q": query,
#         "start": start_index,
#         "num": 10,  # Max results per API call
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         return [item["link"] for item in data.get("items", [])]

#     except requests.exceptions.RequestException as e:
#         print(f"Error during API call: {e}")
#         return []

# def insert_into_db(urls):
#     api_endpoint = "http://localhost/scanmanagement/api_store_direct_login_data.php"
#     for url in urls:
#         try:
#             payload = {
#                 "api_key": "f2441e3810rt5612xu018tumsqHT34dd7f8f6995df9",
#                 "siteaddress": url,
#                 "stat": 1
#             }
#             response = requests.post(api_endpoint, data=payload)
#             response_data = response.json()
            
#             if response_data.get("insertion_status") == 'Added':
#                 print(f"[+] URL inserted: {url}")
#             else:
#                 print(f"[!] Failed to insert: {url}")
#         except Exception as error:
#             print(f"[!] Error inserting URL: {url}, Error: {error}")

# def main():
#     # Get the number of results from the user
#     try:
#         total_sites_target = int(input("Enter the number of URLs you want to collect: "))
#         if total_sites_target <= 0:
#             print("[!] Please enter a positive integer.")
#             return
#     except ValueError:
#         print("[!] Invalid input. Please enter a valid integer.")
#         return

#     max_results_per_query = 100  # Max results to fetch per dork
#     sites_collected = set()  # Store unique sites

#     for dork in GOOGLE_DORKS:
#         print(f"\n[!] Searching for dork: {dork}")
#         start_index = 1

#         while start_index <= max_results_per_query:
#             if len(sites_collected) >= total_sites_target:
#                 break

#             print(f"Fetching results {start_index} to {start_index + 9}...")
#             results = search_google(dork, start_index)

#             if not results:
#                 print("[!] No more results or API limit reached.")
#                 break

#             # Update collected sites and insert current batch
#             new_results = [url for url in results if url not in sites_collected]
#             sites_collected.update(new_results)
#             insert_into_db(new_results)

#             start_index += 10
#             time.sleep(1)  # To avoid hitting rate limits

#         if len(sites_collected) >= total_sites_target:
#             break

#     # Save collected sites to a file
#     with open("vulnerable_sites.txt", "w") as file:
#         file.write("\n".join(sites_collected))

#     print(f"\n[+] Collected {len(sites_collected)} unique sites.")
#     print("Results saved to vulnerable_sites.txt")

# if __name__ == "__main__":
#     main()
# import requests
# import time

# # Replace with your Google API Key and Custom Search Engine ID
# API_KEY = "AIzaSyDNm5ZunFGOYUxVm2zUiBLE4izXIZhJ0x8"
# CSE_ID = "666b716c0785b40b3"

# # Single Google Dork for testing
# GOOGLE_DORK = "inurl:wp-login.php"

# def search_google(query, start_index):
#     """
#     Search Google using the Custom Search JSON API for a given query and start index.
    
#     Args:
#         query (str): The Google Dork query string.
#         start_index (int): The starting index for the search results.

#     Returns:
#         list: A list of URLs found in the search results.
#     """
#     base_url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         "key": API_KEY,
#         "cx": CSE_ID,
#         "q": query,
#         "start": start_index,
#         "num": 10,  # Max results per API call
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         # Return all URLs from the API response
#         return [item["link"] for item in data.get("items", [])]

#     except requests.exceptions.RequestException as e:
#         print(f"Error during API call: {e}")
#         return []
# def insert_into_db(urls):
#     api_endpoint = "http://localhost/scanmanagement/api_store_direct_login_data.php"
#     for url in urls:
#         try:
#             payload = {
#                 "api_key": "f2441e3810rt5612xu018tumsqHT34dd7f8f6995df9",
#                 "siteaddress": url,
#                 "stat": 1
#             }
#             response = requests.post(api_endpoint, data=payload)
#             response_data = response.json()
            
#             if response_data.get("insertion_status") == 'Added':
#                 print(f"[+] URL inserted: {url}")
#             else:
#                 print(f"[!] Failed to insert: {url}")
#         except Exception as error:
#             print(f"[!] Error inserting URL: {url}, Error: {error}")

# # def insert_into_db(urls):
# #      api_endpoint = "http://localhost/scanmanagement/api_store_direct_login_data.php"
# #     for url in urls:
# #         try:
# #             payload = {
# #                 "api_key": "f2441e3810rt5612xu018tumsqHT34dd7f8f6995df9",
# #                 "siteaddress": url,
# #                 "stat": 1
# #             }
# #             response = requests.post(api_endpoint, data=payload)
# #             response_data = response.json()
            
# #             if response_data.get("insertion_status") == 'Added':
# #                 print(f"[+] URL inserted: {url}")
# #             else:
# #                 print(f"[!] Failed to insert: {url}")
# #         except Exception as error:
# #             print(f"[!] Error inserting URL: {url}, Error: {error}")

# def main():
#     try:
#         target_sites_count = int(input("Enter the number of URLs you want to collect: "))
#         if target_sites_count <= 0:
#             print("[!] Please enter a positive integer.")
#             return
#     except ValueError:
#         print("[!] Invalid input. Please enter a valid integer.")
#         return

#     max_results_per_query = 100  # Max results to fetch per dork
#     sites_collected = set()  # Store unique sites

#     print(f"\n[!] Searching for dork: {GOOGLE_DORK}")
#     start_index = 1

#     while start_index <= max_results_per_query:
#         if len(sites_collected) >= target_sites_count:
#             break

#         print(f"Fetching results {start_index} to {start_index + 9}...")
#         results = search_google(GOOGLE_DORK, start_index)

#         if not results:
#             print("[!] No more results or API limit reached.")
#             break

#         # Update collected sites and print them
#         # new_results = [url for url in results if url not in sites_collected]
#         # for url in new_results[:target_sites_count - len(sites_collected)]:
#         #     print(f"[+] Collected site: {url}")

#         # sites_collected.update(new_results[:target_sites_count - len(sites_collected)])
#         # print(new_results[:target_sites_count - len(sites_collected)])

#         new_results = [url for url in results if url not in sites_collected]
#         sites_collected.update(new_results)
#         insert_into_db(new_results)

#         start_index += 10
#         time.sleep(1)  # To avoid hitting rate limits

#     # Save collected sites to a file
#     with open("vulnerable_sites.txt", "w") as file:
#         file.write("\n".join(sites_collected))

#     print(f"\n[+] Collected {len(sites_collected)} unique sites.")
#     print("Results saved to vulnerable_sites.txt")

# if __name__ == "__main__":
#     main()
# import requests
# import time

# API_KEY = "AIzaSyDNm5ZunFGOYUxVm2zUiBLE4izXIZhJ0x8"
# CSE_ID = "666b716c0785b40b3"

# GOOGLE_DORK = "inurl:wp-login.php"

# def search_google(query, start_index):
#     base_url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         "key": API_KEY,
#         "cx": CSE_ID,
#         "q": query,
#         "start": start_index,
#         "num": 10,
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         return [item["link"] for item in data.get("items", [])]

#     except requests.exceptions.RequestException as e:
#         print(f"Error during API call: {e}")
#         return []

# def insert_into_db(urls):
#     api_endpoint = "http://localhost/scanmanagement/api_store_direct_login_data.php"
#     for url in urls:
#         try:
#             payload = {
#                 "api_key": "f2441e3810rt5612xu018tumsqHT34dd7f8f6995df9",
#                 "siteaddress": url,
#                 "stat": 1
#             }
#             response = requests.post(api_endpoint, data=payload)
#             response_data = response.json()
            
#             if response_data.get("insertion_status") == 'Added':
#                 print(f"[+] URL inserted: {url}")
#             else:
#                 print(f"[!] Failed to insert: {url}")
#         except Exception as error:
#             print(f"[!] Error inserting URL: {url}, Error: {error}")

# def main():
#     try:
#         target_sites_count = int(input("Enter the number of URLs you want to collect: "))
#         if target_sites_count <= 0:
#             print("[!] Please enter a positive integer.")
#             return
#     except ValueError:
#         print("[!] Invalid input. Please enter a valid integer.")
#         return

#     max_results_per_query = 100  # Max results to fetch per dork
#     sites_collected = set()  # Store unique sites

#     print(f"\n[!] Searching for dork: {GOOGLE_DORK}")
#     start_index = 1

#     while start_index <= max_results_per_query:
#         if len(sites_collected) >= target_sites_count:
#             break

#         print(f"Fetching results {start_index} to {start_index + 9}...")
#         results = search_google(GOOGLE_DORK, start_index)

#         if not results:
#             print("[!] No more results or API limit reached.")
#             break

#         # Update collected sites and insert current batch
#         new_results = [url for url in results if url not in sites_collected]
#         sites_collected.update(new_results[:target_sites_count - len(sites_collected)])
#         insert_into_db(new_results[:target_sites_count - len(sites_collected)])

#         start_index += 10
#         time.sleep(2)  # To avoid hitting rate limits

#     # Save collected sites to a file
#     with open("vulnerable_sites.txt", "w") as file:
#         file.write("\n".join(sites_collected))

#     print(f"\n[+] Collected {len(sites_collected)} unique sites.")
#     print("Results saved to vulnerable_sites.txt")

# if __name__ == "__main__":
#     main()
# import requests
# import time

# # Replace with your Google API Key and Custom Search Engine ID
# API_KEY = "AIzaSyDNm5ZunFGOYUxVm2zUiBLE4izXIZhJ0x8"
# CSE_ID = "666b716c0785b40b3"

# # Google Dork for searching vulnerable WordPress sites
# GOOGLE_DORK = "inurl:wp-login.php"  # Specify the single dork to use

# def search_google(query, start_index):
#     """
#     Search Google using the Custom Search JSON API for a given query and start index.
    
#     Args:
#         query (str): The Google Dork query string.
#         start_index (int): The starting index for the search results.

#     Returns:
#         list: A list of URLs found in the search results.
#     """
#     base_url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         "key": API_KEY,
#         "cx": CSE_ID,
#         "q": query,
#         "start": start_index,
#         "num": 10,  # Max results per API call
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         # Filter to include only .com domains
#         return [item["link"] for item in data.get("items", []) if item["link"].endswith(".com")]

#     except requests.exceptions.RequestException as e:
#         print(f"Error during API call: {e}")
#         return []

# def insert_into_db(urls):
#     """
#     Insert fetched URLs into the database using a POST API call.
    
#     Args:
#         urls (list): List of URLs to insert.
#     """
#     api_endpoint = "http://localhost/scanmanagement/api_store_direct_login_data.php"
#     for url in urls:
#         try:
#             payload = {
#                 "api_key": "f2441e3810rt5612xu018tumsqHT34dd7f8f6995df9",
#                 "siteaddress": url,
#                 "stat": 1
#             }
#             response = requests.post(api_endpoint, data=payload)
#             response_data = response.json()
            
#             if response_data.get("insertion_status") == 'Added':
#                 print(f"[+] URL inserted: {url}")
#             else:
#                 print(f"[!] Failed to insert: {url}")
#         except Exception as error:
#             print(f"[!] Error inserting URL: {url}, Error: {error}")

# def main():
#     try:
#         target_sites_count = int(input("Enter the number of URLs you want to collect: "))
#         if target_sites_count <= 0:
#             print("[!] Please enter a positive integer.")
#             return
#     except ValueError:
#         print("[!] Invalid input. Please enter a valid integer.")
#         return

#     max_results_per_query = 100  # Max results to fetch
#     sites_collected = set()  # Store unique sites

#     print(f"\n[!] Searching for dork: {GOOGLE_DORK}")
#     start_index = 1

#     while start_index <= max_results_per_query:
#         if len(sites_collected) >= target_sites_count:
#             break

#         print(f"Fetching results {start_index} to {start_index + 9}...")
#         results = search_google(GOOGLE_DORK, start_index)

#         if not results:
#             print("[!] No more results or API limit reached.")
#             break

#         # Update collected sites and insert current batch
#         new_results = [url for url in results if url not in sites_collected]
#         sites_collected.update(new_results[:target_sites_count - len(sites_collected)])
#         insert_into_db(new_results[:target_sites_count - len(sites_collected)])

#         start_index += 10
#         time.sleep(1)  # To avoid hitting rate limits

#     # Save collected sites to a file
#     with open("vulnerable_sites.txt", "w") as file:
#         file.write("\n".join(sites_collected))

#     print(f"\n[+] Collected {len(sites_collected)} unique sites.")
#     print("Results saved to vulnerable_sites.txt")

# if __name__ == "__main__":
#     main()
# import requests
# import time

# # Replace with your Google API Key and Custom Search Engine ID
# API_KEY = "AIzaSyDNm5ZunFGOYUxVm2zUiBLE4izXIZhJ0x8"
# CSE_ID = "666b716c0785b40b3"

# # List of Google Dorks for searching vulnerable WordPress sites
# GOOGLE_DORKS = [
#     "inurl:wp-login.php",
#     "inurl:wp-admin",
#     "inurl:wp-content/plugins filetype:php",
#     "inurl:wp-content/themes filetype:php",
#     "inurl:wp-config.php",
#     "inurl:backup filetype:sql OR filetype:zip OR filetype:gz",
#     "inurl:error_log \"wordpress\"",
#     "inurl:wp-content/debug.log",
#     "intitle:\"index of\" \"wp-content\"",
#     "inurl:timthumb.php",
#     "inurl:revslider.php",
#     "inurl:readme.html \"wordpress\"",
#     "intitle:\"WordPress *.*.*\""
# ]

# def search_google(query, start_index):
#     """
#     Search Google using the Custom Search JSON API for a given query and start index.
    
#     Args:
#         query (str): The Google Dork query string.
#         start_index (int): The starting index for the search results.

#     Returns:
#         list: A list of URLs found in the search results.
#     """
#     base_url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         "key": API_KEY,
#         "cx": CSE_ID,
#         "q": query,
#         "start": start_index,
#         "num": 10,  # Max results per API call
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         # Filter to include only .com domains
#         return [item["link"] for item in data.get("items", []) if item["link"].endswith(".com")]

#     except requests.exceptions.RequestException as e:
#         print(f"Error during API call: {e}")
#         return []

# def insert_into_db(urls):
#     """
#     Insert fetched URLs into the database using a POST API call.
    
#     Args:
#         urls (list): List of URLs to insert.
#     """
#     api_endpoint = "http://localhost/scanmanagement/api_store_direct_login_data.php"
#     for url in urls:
#         try:
#             payload = {
#                 "api_key": "f2441e3810rt5612xu018tumsqHT34dd7f8f6995df9",
#                 "siteaddress": url,
#                 "stat": 1
#             }
#             response = requests.post(api_endpoint, data=payload)
#             response_data = response.json()
            
#             if response_data.get("insertion_status") == 'Added':
#                 print(f"[+] URL inserted: {url}")
#             else:
#                 print(f"[!] Failed to insert: {url}")
#         except Exception as error:
#             print(f"[!] Error inserting URL: {url}, Error: {error}")

# def main():
#     try:
#         target_sites_count = int(input("Enter the number of URLs you want to collect: "))
#         if target_sites_count <= 0:
#             print("[!] Please enter a positive integer.")
#             return
#     except ValueError:
#         print("[!] Invalid input. Please enter a valid integer.")
#         return

#     max_results_per_query = 100  # Max results to fetch per dork
#     sites_collected = set()  # Store unique sites

#     for dork in GOOGLE_DORKS:
#         print(f"\n[!] Searching for dork: {dork}")
#         start_index = 1

#         while start_index <= max_results_per_query:
#             if len(sites_collected) >= target_sites_count:
#                 break

#             print(f"Fetching results {start_index} to {start_index + 9}...")
#             results = search_google(dork, start_index)

#             if not results:
#                 print("[!] No more results or API limit reached.")
#                 break

#             # Update collected sites and insert current batch
#             new_results = [url for url in results if url not in sites_collected]
#             sites_collected.update(new_results[:target_sites_count - len(sites_collected)])
#             insert_into_db(new_results[:target_sites_count - len(sites_collected)])

#             start_index += 10
#             time.sleep(1)  # To avoid hitting rate limits

#         if len(sites_collected) >= target_sites_count:
#             break

#     # Save collected sites to a file
#     with open("vulnerable_sites.txt", "w") as file:
#         file.write("\n".join(sites_collected))

#     print(f"\n[+] Collected {len(sites_collected)} unique sites.")
#     print("Results saved to vulnerable_sites.txt")

# if __name__ == "__main__":
#     main()

# import requests
# import time

# # Replace with your Google API Key and Custom Search Engine ID
# API_KEY = "AIzaSyDNm5ZunFGOYUxVm2zUiBLE4izXIZhJ0x8"
# CSE_ID = "666b716c0785b40b3"

# # List of Google Dorks for searching vulnerable WordPress sites
# GOOGLE_DORKS = [
#     "inurl:wp-login.php",
#     "inurl:wp-admin",
#     "inurl:wp-content/plugins filetype:php",
#     "inurl:wp-content/themes filetype:php",
#     "inurl:wp-config.php",
#     "inurl:backup filetype:sql OR filetype:zip OR filetype:gz",
#     "inurl:error_log \"wordpress\"",
#     "inurl:wp-content/debug.log",
#     "intitle:\"index of\" \"wp-content\"",
#     "inurl:timthumb.php",
#     "inurl:revslider.php",
#     "inurl:readme.html \"wordpress\"",
#     "intitle:\"WordPress *.*.*\""
# ]

# def search_google(query, start_index):

#     base_url = "https://www.googleapis.com/customsearch/v1"
#     params = {
#         "key": API_KEY,
#         "cx": CSE_ID,
#         "q": query,
#         "start": start_index,
#         "num": 10,  # Max results per API call
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()
#         data = response.json()
        
#         return [item["link"] for item in data.get("items", [])]

#     except requests.exceptions.RequestException as e:
#         print(f"Error during API call: {e}")
#         return []

# def insert_into_db(urls):

#     api_endpoint = "http://localhost/scanmanagement/api_store_direct_login_data.php"
#     for url in urls:
#         try:
#             payload = {
#                 "api_key": "f2441e3810rt5612xu018tumsqHT34dd7f8f6995df9",
#                 "siteaddress": url,
#                 "stat": 1
#             }
#             response = requests.post(api_endpoint, data=payload)
#             response_data = response.json()
            
#             if response_data.get("insertion_status") == 'Added':
#                 print(f"[+] URL inserted: {url}")
#             else:
#                 print(f"[!] Failed to insert: {url}")
#         except Exception as error:
#             print(f"[!] Error inserting URL: {url}, Error: {error}")

# def main():
#     max_results_per_query = 100  # Max results to fetch per dork
#     total_sites_target = 100000  # Target number of sites
#     sites_collected = set()  # Store unique sites

#     for dork in GOOGLE_DORKS:
#         print(f"\n[!] Searching for dork: {dork}")
#         start_index = 1

#         while start_index <= max_results_per_query:
#             if len(sites_collected) >= total_sites_target:
#                 break

#             print(f"Fetching results {start_index} to {start_index + 9}...")
#             results = search_google(dork, start_index)

#             if not results:
#                 print("[!] No more results or API limit reached.")
#                 break

#             # Update collected sites and insert current batch
#             new_results = [url for url in results if url not in sites_collected]
#             sites_collected.update(new_results)
#             insert_into_db(new_results)

#             start_index += 10
#             time.sleep(1)  # To avoid hitting rate limits

#         if len(sites_collected) >= total_sites_target:
#             break

#     # Save collected sites to a file
#     with open("vulnerable_sites.txt", "w") as file:
#         file.write("\n".join(sites_collected))

#     print(f"\n[+] Collected {len(sites_collected)} unique sites.")
#     print("Results saved to vulnerable_sites.txt")

# if __name__ == "__main__":
#     main()