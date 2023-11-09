from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach",True)


driver = webdriver.Chrome(options=chrome_option)
# driver.get("https://www.python.org/")

date_time = "/html/body/div/div[3]/div/section/div[2]/div[2]/div/ul"
# date = driver.find_element(By.XPATH,value = date_time)
# event = [date.text]

# driver.close()
# driver.quit()

data = ['2023-11-05\nTOUFU - Parent-Child Python Programming Workshop\n2023-11-06\nDjangoCon Africa 2023\n2023-11-09\nPyCon Sweden\n2023-11-11\nPyCon Ireland 2023\n2023-11-14\nPyData Tel Aviv 2023']
data = data[0].split("\n")

print(sorted(data))