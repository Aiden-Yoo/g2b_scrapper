from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

driver = webdriver.Chrome(r"C:\Python38\chromedriver.exe")
result = []
keywords = [
    "코어엣지",
    "한드림넷",
    "다산네트웍스",
    "파이오링크",
    "유비쿼스",
    "Arista",
    "Alcatel",
    "Cisco",
    "Dell",
    "Juniper",
    "Extreme",
    "HPE",
]


def get_products():
    try:
        driver.get(
            "http://shopping.g2b.go.kr:8092/sm/pp/goods/SMPPIntgrMainSrchGoodsList.do"
        )
        for keyword in keywords:
            kwd = driver.find_element_by_class_name(
                "srch_txt"
            )  # class값이 srch_txt인 태그 가져오기

            kwd.clear()  # 내용 삭제

            kwd.send_keys(keyword)  # 검색어 입력후 엔터
            kwd.send_keys(Keys.RETURN)

            if driver.find_element_by_link_text("네트워크스위치"):  # 네트워크스위치 선택
                select_switch = driver.find_element_by_link_text("네트워크스위치")
                select_switch.click()
            else:
                pass

            # 목록수 100건 선택 (드롭다운)
            pageSize = driver.find_element_by_class_name("pageSize")
            selector = Select(pageSize)
            selector.select_by_value("100")

            # 적용 버튼 클릭
            refresh_button = driver.find_element_by_xpath("//input[@alt='정렬']")
            refresh_button.click()

            append_list()  # 각 항목 수집
            prdLstFrm = driver.find_element_by_id("prdLstFrm")
            # 다음 페이지 유무 확인 prdLstFrm > page_num > a
            page_num = prdLstFrm.find_element_by_class_name("page_num")
            # page_two = page_num.find_element_by_link_text("2")
            try:
                page_two = page_num.find_element_by_link_text("2")
                print("{} has two page.".format(keyword))
                page_two.click()
                append_list()
            except:
                print("{} has just one page.".format(keyword))

        return result

    except Exception as e:
        print(e)  # 에러가 발생 시 출력

    finally:
        driver.quit()  # 에러와 관계없이 실행되고, 크롬 드라이버를 종료


def append_list():
    itemLst = driver.find_element_by_class_name("itemLst")  # 상품 리스트
    item_lists_tbody = itemLst.find_element_by_tag_name("tbody")
    item_lists_tr = item_lists_tbody.find_elements_by_tag_name("tr")

    for item in item_lists_tr:
        html = item.get_attribute("innerHTML")
        soup = BeautifulSoup(html, "html.parser")

        itemName = soup.find("li", class_="itemName").span.get_text(" ", strip=True)
        print(itemName)
        # itemStd = soup.find("li", class_="itemStd").span.a.get_text(" ", strip=True) # 201127 Changed
        itemStd = soup.find("li", class_="itemStd").span.get_text(" ", strip=True)
        print(itemStd)
        itemId = (
            soup.find("li", class_="itemId").get_text(" ", strip=True).split(" : ")[1]
        )
        print(itemId)
        companyName = soup.find("span", class_="comName").get_text(" ", strip=True)
        print(companyName)
        origin = (
            soup.find("li", class_="origin").get_text(" ", strip=True).split(" : ")[1]
        )
        print(origin)
        itemCntrctEndDt = (
            soup.find("li", class_="itemCntrctEndDt")
            .get_text(" ", strip=True)
            .split(" | ")[0]
            .split(" : ")[1]
        )
        print(itemCntrctEndDt)
        itemDeliveryDeadline = (
            soup.find("li", class_="itemCntrctEndDt")
            .get_text(" ", strip=True)
            .split(" | ")[1]
            .split(" : ")[1]
        )
        print(itemDeliveryDeadline)
        price = soup.find("li", class_="prsNow").get_text(" ", strip=True)
        print(price)
        if "(부품)" in itemStd:
            parts = "O"
        else:
            parts = "-"

        result.append(
            [
                itemName,
                itemStd,
                parts,
                itemId,
                companyName,
                origin,
                itemCntrctEndDt,
                itemDeliveryDeadline,
                price,
            ]
        )
    return

