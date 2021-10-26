from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys

cas_list = []
summary = []

df = pd.DataFrame(columns=['CAS', '재고'])

print("---------------------------------------------")
print("---1/3 CAS를 입력하세요, f 입력시 종료합니다---")
print("---------------------------------------------")

while True:
    cas = str(input('CAS 입력하세요 (f 입력 시 종료) : ')) # 입력이 끝나면 f 입력
    cas_list.append(cas)
    print(cas_list)
    if cas == 'f':
        cas_list.remove('f')
        break

print("---------------------------------------------")
print("---2/3 CAS를 입력완료, 동아 DB로부터 검색 중---")
print("---------------------------------------------")

print(cas_list)

link = 'Link' #Erased due to security

for i in range(len(cas_list)):

    driver = webdriver.Chrome('chromedriver.exe')  
    driver.get(link)
    driver.implicitly_wait(1) #wait sec
    driver.find_element_by_id("DSH").click()
    driver.implicitly_wait(1) #wait sec
    driver.find_element_by_id("TxtCasNo").send_keys(cas_list[i])
    driver.implicitly_wait(1) #wait sec
    driver.find_element_by_id("TxtBk").send_keys(Keys.TAB + Keys.ENTER)
    driver.implicitly_wait(2) #wait sec
   
    cas = cas_list[i]

    try:
        tag = driver.find_element_by_css_selector('#rMateH5__Content60')
        name = tag.find_element_by_css_selector('span.rMateH5__UITextField.rMateH5__IconItemRenderer')

        check = name.text
        summary.append([cas, check])
    except:
        check = '재고없음'
        summary.append([cas, check])
    driver.quit()

print("---------------------------------------------")
print("--3/3 Finish the Search from Dong-A Library--")
print("---------------------------------------------")
df = df.append(pd.DataFrame(summary, columns=['CAS', '재고']))
print(df)
print("---------------------------------------------")
print("---------------------------------------------")
