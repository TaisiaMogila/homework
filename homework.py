from mysql.connector import connect

con = connect(host='localhost',
              user='root',
              password='root',
              database='agriculture')

print("1. Знайти для кожної культури усі господарства, що її вирощують\n"
      "2. Врожайність по господарству і ґатунок поставленої продукції\n"
      "3. Підвищити вартість певної продукції за всіма ґатунками на 10% (для певної культури)\n"
      "4. Для аналізу роботи господарства показати для кожного з них усі культури, що вони постачають, \n"
      "різницю між врожайністю середньою і по господарству, вартість поставленої продукції, \n"
      "та загальну кількість постачань і за кожним ґатунком на кінець року і їх вартість\n"
      "5. Яку культуру зовсім не поставили за держзамовленням\n"
      "6. Знайти середню вартість продукції кожного ґатунку для кожного господарства\n"
      "7. Знайти культури, в яких врожайність по господарству вища за середню\n"
      "8. Знайти культури, для яких замовлено менше половини від загальної маси замовлення\n"
      "9. Знайти райони, де є господарства з найбільшою та найменшою загальною площею\n"
      "10. Знайти культури, які були поставлені за держзамовленням найбільш часто\n")
cursor = con.cursor()
while True:
    action = int(input())
    if action == 1:
        cursor.execute("SELECT c.culture_name, h.farm_name "
                       "FROM culture c "
                       "INNER JOIN delivered d ON c.culture_id = d.culture_id "
                       "INNER JOIN households h ON d.farm_id = h.farm_id;")
        result = cursor.fetchall()
        print(result)
    elif action == 2:
        cursor.execute("SELECT farm_yield, variety_products "
                       "FROM delivered;")
        result = cursor.fetchall()
        print(result)
    elif action == 3:
        cursor.execute("UPDATE culture "
                       "SET price_for_first = price_for_first * 1.1, "
                       "price_for_second = price_for_second * 1.1, "
                       "price_for_high = price_for_high * 1.1 "
                       "WHERE culture_name = 'Горох';")
        con.commit()
    elif action == 4:
        cursor.execute("SELECT (c.average_yield - d.farm_yield) AS різниця_врожайності, "
                       "(d.delivered_weight * c.price_for_first + "
                       "d.delivered_weight * c.price_for_second + "
                       "d.delivered_weight * c.price_for_high) AS вартість_поставленої_продукції "
                       "FROM households h "
                       "INNER JOIN delivered d ON h.farm_id = d.farm_id "
                       "INNER JOIN culture c ON d.culture_id = c.culture_id;")
        result = cursor.fetchall()
        print(result)
    elif action == 5:
        cursor.execute("SELECT DISTINCT culture_name "
                       "FROM culture c "
                       "WHERE c.culture_id NOT IN ( SELECT DISTINCT culture_id "
                       "FROM delivered);")
        result = cursor.fetchall()
        print(result)
    elif action == 6:
        cursor.execute("SELECT h.farm_name, d.variety_products, AVG(d.delivered_weight * c.price_for_first + "
                       "d.delivered_weight * c.price_for_second + "
                       "d.delivered_weight * c.price_for_high) AS середня_вартість "
                       "FROM delivered d  "
                       "INNER JOIN households h ON d.farm_id = h.farm_id "
                       "INNER JOIN culture c ON d.culture_id = c.culture_id "
                       "GROUP BY h.farm_name, d.variety_products;")
        result = cursor.fetchall()
        print(result)
    elif action == 7:
        cursor.execute("SELECT culture_name "
                       "FROM culture c "
                       "INNER JOIN delivered d ON c.culture_id = d.culture_id "
                       "WHERE d.farm_yield > c.average_yield;")
        result = cursor.fetchall()
        print(result)
    elif action == 8:
        cursor.execute("SELECT culture_name "
                       "FROM culture c "
                       "INNER JOIN delivered d ON c.culture_id = d.culture_id "
                       "GROUP BY c.culture_id "
                       "HAVING SUM(d.order_weight) < 0.5 * (SELECT SUM(order_weight) FROM delivered);")
        result = cursor.fetchall()
        print(result)
    elif action == 9:
        cursor.execute("SELECT district, total_area AS найбільша_площа "
                       "FROM households "
                       "ORDER BY найбільша_площа DESC "
                       "LIMIT 1;")
        result = cursor.fetchall()
        print(result)
    elif action == 10:
        cursor.execute("SELECT culture_name, COUNT(*) AS кількість_поставок "
                       "FROM culture c "
                       "INNER JOIN delivered d ON c.culture_id = d.culture_id "
                       "GROUP BY c.culture_id "
                       "ORDER BY кількість_поставок DESC;")
        result = cursor.fetchall()
        print(result)
    else:
        cursor.close()
        break
