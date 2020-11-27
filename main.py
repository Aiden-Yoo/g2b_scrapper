# from lecture import get_lectures
from products import get_products
import datetime
import csv

nowDate = datetime.datetime.now()


def save_to_file(products_list):
    file = open(
        "G2B_products_" + nowDate.strftime("%y%m%d_%H%M%S") + ".txt",
        mode="w",
        newline="",
        encoding="utf-8",
    )
    writer = csv.writer(file)
    writer.writerow(["세부품명", "품명", "부품", "식별번호", "총판", "원산지", "가격", "계약종료일", "납품기한"])
    for products in products_list:
        writer.writerow(products)
    file.close()
    return


products_list = get_products()
save_to_file(products_list)
