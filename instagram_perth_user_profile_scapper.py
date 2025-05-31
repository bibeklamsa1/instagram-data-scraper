from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from cred import username, password  # Assuming you have a credentials.py file with your login details
from bs4 import BeautifulSoup


from selenium.webdriver.chrome.options import Options
chrome_options = Options()




driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)



# Input credentials
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys(username)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

# Wait for login to complete
time.sleep(10)
print("✅ Logged in to Instagram via Selenium")



# now visit this page and find the post contain # the keyword "ben" and "perth". where ben is the name of the person and perth is the location.
data = driver.get("https://www.instagram.com/explore/search/keyword/?q=ben%20perth")

# Wait for the page to load
time.sleep(10)

#load more posts
# Scroll down multiple times
scroll_pause_time = 5  # Adjust based on your internet speed

for i in range(1):  # Scroll 1 time
    print(f"Scrolling {i + 1}/1...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)



#now let's create a function that extracts 
#collect the username,folowers,following from the posts
users_info = []
# Collect post links (example)
posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
post_links = [post.get_attribute('href') for post in posts]
print(f"Found {len(post_links)} post links")
for link in post_links:
    driver.get(link)
      # Wait for the page to load
    time.sleep(0.5)
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the username link
    username_element = bs.find('a', href=lambda href: href and '/p/' not in href)
    
    if username_element and "ben" in username_element.text.lower():
        username = username_element.text.strip()
        try:

            users_info.append({
                'UserName': username
            })

        except Exception as e:
            print(f"Error collecting info for {username}: {e}")
    else:
        print("No username link found.")
    

#write it in a csv file
import pandas as pd
df = pd.DataFrame(users_info)
df.to_csv('instagram_users_info.csv', index=False)
print("✅ User information saved to instagram_users_info.csv")
# Close the driver
driver.quit()