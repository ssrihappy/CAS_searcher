#----Version Log-----#
# 0.1 ver 시약 재고확인
# 0.2 ver, add 재고 및 위치 정보

from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys

cas_list = []
summary = []

df = pd.DataFrame(columns=['CAS', '시약명', '재고', '위치1', '위치2'])

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
print("---2/3 CAS를 입력완료, DB로부터 검색 중---")
print("---------------------------------------------")

print(cas_list)

link = '$$LINK$$' #link for security

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
        for j in range(1, 10):
            stock = driver.find_elements_by_class_name('rMateH5__DataGridColumn43')[j] #재고조회
            k = stock.text
            if k == '반출불가':
                j += 1
            else: # 반출불가가 아닌 항목에 대해 조회
                loc1 = driver.find_elements_by_class_name('rMateH5__DataGridColumn37')[j]
                loc2 = driver.find_elements_by_class_name('rMateH5__DataGridColumn39')[j]
                loc3 = driver.find_elements_by_class_name('rMateH5__DataGridColumn41')[j]
                location1 = loc1.text + '/' + loc2.text + '/' + loc3.text
                loc1 = driver.find_elements_by_class_name('rMateH5__DataGridColumn37')[j+1]
                loc2 = driver.find_elements_by_class_name('rMateH5__DataGridColumn39')[j+1]
                loc3 = driver.find_elements_by_class_name('rMateH5__DataGridColumn41')[j+1]
                location2 = loc1.text + '/' + loc2.text + '/' + loc3.text
                break
        summary.append([cas, check, k, location1, location2])
    except:
        check = '재고없음'
        summary.append([cas, check, 'N/A', 'N/A', 'N/A'])
    driver.quit()

print("---------------------------------------------")
print("-----3/3 Finish the Search from  Library-----")
print("---------------------------------------------")
df = df.append(pd.DataFrame(summary, columns=['CAS', '시약명', '재고', '위치1', '위치2']))
print(df)
print("---------------------------------------------")
print("---------------------------------------------")

with pd.ExcelWriter('./reagent.xlsx') as writer:
    df.to_excel(writer, sheet_name='reagent', index=False, columns=['CAS', '시약명', '재고', '위치1', '위치2'])

print("---------------------------------------------")
print("---------Success to save as Excel file-------")
print("---------------------------------------------")
