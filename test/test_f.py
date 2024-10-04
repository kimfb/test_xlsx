"""
Для запуска теста здесь должны быть .xlxs файлы и папка results

"""
import os
import pandas as pd


from main import get_sum_accounts, get_sum_payment, generate_excel_file


# ['Выставленные счета.xlsx', 'Пациенты.xlsx', 'Совершённые платежи.xlsx']
xls_list = [x for x in os.listdir('.') if x.endswith("xlsx")]

accounts, patience, payment = (pd.read_excel(pd.ExcelFile(x)) for x in xls_list)

r1 = get_sum_accounts(accounts, patience, "ИД", "ID", group_fio=True)
print(r1)
r2 = get_sum_payment(payment, patience, "ИД", "ID")
print(r2)

for i, dt in enumerate((r1, r2)):
    generate_excel_file(dt, f"results/doc_{i}")
