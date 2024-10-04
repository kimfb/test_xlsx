import pandas as pd


def get_sum_accounts(tb1, tb2, left_on, right_on, sum_column="Цена услуги итоговая", group_fio=False):
    """
    Возвращает таблицу с полями ФИО/ID пациента и суммой выставленных счетов.

            Args:
                tb1: таблица 1 (DataFrame)
                tb2: таблица 2 (DataFrame)
                left_on: название поля tb1 для связи с tb2 (str)
                right_on: название поля tb2 для связи с tb1 (str)
                sum_column: название поля для подсчёта суммы, по умолчанию 'Цена услуги итоговая' (str)
                group_fio: определяет, следует ли формировать поле ФИО, по умолчанию группировка по left_on (str)

            Returns:
                DataFrame объект.
    """

    group_column = left_on
    merged_tables = pd.merge(
        tb1,
        tb2,
        left_on=left_on,
        right_on=right_on,
        how="inner"
    )

    if group_fio:
        merged_tables["ФИО"] = merged_tables[["Фамилия", "Имя", "Отчество"]].agg(" ".join, axis=1)
        group_column = "ФИО"

    res_table = merged_tables.groupby(group_column, as_index=False).agg(Сумма_счетов=(sum_column, "sum"))
    return res_table


def get_sum_payment(tb1, tb2, left_on, right_on, sum_column="Платежи"):
    """
    Возвращает таблицу с полями ФИО пациента, номер телефона и суммой совершенных платежей.

            Args:
                tb1: таблица 1 (DataFrame)
                tb2: таблица 2 (DataFrame)
                left_on: название поля tb1 для связи с tb2 (str)
                right_on: название поля tb2 для связи с tb1 (str)
                sum_column: название поля для подсчёта суммы, по умолчанию 'Платежи' (str)

            Returns:
                DataFrame объект.
    """
    merged_tables = pd.merge(
        tb1,
        tb2,
        left_on=left_on,
        right_on=right_on,
        how="inner"
    )

    merged_tables["ФИО"] = merged_tables[["Фамилия", "Имя", "Отчество"]].agg(" ".join, axis=1)
    res_table = merged_tables.groupby(["ФИО", "Телефон"], as_index=False).agg(Сумма_платежей=(sum_column, "sum"))
    return res_table


def generate_excel_file(df_table, name="new_file"):
    """
    Формирует .xlsx-документ с объекта df_table и сохраняет с именем name.

        Args:
            df_table: таблица с данными (DataFrame)
            name: имя файла, допускается использовать относительный путь для указания расположения (str)
    """

    with pd.ExcelWriter(f"{name}.xlsx") as writer:
        df_table.to_excel(writer, index=False, sheet_name=name.split('/')[-1])
