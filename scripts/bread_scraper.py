from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from parse_image import base64_to_img, url_to_img

def main():
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    bread_list = ["anpan", "bagel", "waffle", "baguette", "dorayaki","pita", "sourdough"]
    for bread in bread_list:
        get_first_n_bread(50, bread, driver)
    driver.quit()
    

def get_first_n_bread(n, bread, driver):
    driver.get("https://images.google.com")
    search_box = driver.find_element(value="q", by=By.NAME)
    search_box.send_keys(bread + " bread")
    search_box.submit()
    time.sleep(2)
   
    actual_counter = 0
    counter = 1
    ids = set()
    while counter <= n:
        actual_counter += 1
        mosaic = driver.find_element(value="[data-id=\"mosaic\"]", by=By.CSS_SELECTOR).get_attribute("outerHTML")
        soup = BeautifulSoup(mosaic, "html.parser")
        imgs = soup.find_all("img")

        for img in imgs:
            id = img.get("id")
            if id in ids:
                continue
            # ignore icons
            height = img.get("height")
            if int(height) < 128:
                continue

            src = img.get("src")
            file_name = f"{bread}_{counter}"
            if src.startswith("https"):
                isOk = url_to_img(src, f"../dataset/{bread}", file_name)
                time.sleep(0.2)
            else:
                isOk = base64_to_img(src, f"../dataset/{bread}", file_name)
            if isOk:
                print(f"Saving: {file_name}.jpg")

                counter+=1
                ids.add(id)
            if counter > n:
                break
            if actual_counter % 10 == 0:
                driver.execute_script(f"window.scrollBy(0, 512);")
                time.sleep(1)
                break




if __name__=="__main__":
    main()