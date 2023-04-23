import csv

with open('CarInfo.csv', mode='r', newline='', encoding='utf-8-sig') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)

    with open('insert_queries.sql', mode='w', encoding='utf-8') as sql_file:
        for row in reader:
            values = [f"'{value}'" if index not in (0, 8) else str(value) for index, value in enumerate(row)]
            insert_query = f"INSERT INTO CAR_AD (ID, BRAND, MODEL, AD_TYPE, FUEL_TYPE, PRICE, PRICE_TYPE, PAYMENT_METHOD, YEAR, ODOMETER_RANGE_start, ODOMETER_RANGE_end, TRANSMISSION_TYPE, CAR_CONDITION, COLOR, BODY_TYPE, ENGINE_CAPACITY, VIDEO, VTOUR, DESCRIPTION, LOCATION) VALUES ({', '.join(values)});\n"
            sql_file.write(insert_query)


with open('SellerInfo.csv', mode='r', encoding='utf-8-sig') as csv_file1:
    csv_reader = csv.reader(csv_file1)
    next(csv_reader)
    with open('seller_insert_queries.sql', mode='w', encoding='utf-8') as sql_file:
        for row in csv_reader:
            query = "INSERT INTO SELLER (CAR_AD_ID, NAME, JOINING_DATE_YEAR, JOINING_DATE_MONTH) VALUES ({}, '{}', {}, '{}');".format(row[0], row[1], row[2], row[3])
            with open('seller_insert_queries.sql', mode='a', encoding='utf-8') as sql_file:
                sql_file.write(query + "\n")
