import tkinter as tk
from tkinter import ttk
import mysql.connector

# connect to the database
car_db = mysql.connector.connect(
    host="db4free.net",
    user="",
    password="",
    database="carstuff"
)

# cursor instance of the database
mycursor = car_db.cursor()


# sql query for inserting a new user
def add_new_user(email, username, gender, dob, phone):
    global mycursor
    user_insertion = '''
    INSERT INTO USER (EMAIL, USERNAME, GENDER, DOB, USER_PHONE)
    VALUES (%s, %s, %s, %s, %s)
    '''

    mycursor.execute(user_insertion, (email, username, gender, dob, phone))
    car_db.commit()


# sql query for adding a new sale
def add_new_sale(email, name, car_id, rating):
    global mycursor
    sale_insertion = '''
    INSERT INTO SALE (USER_EMAIL, SELLER_NAME, CAR_ID, RATING)
    VALUES (%s, %s, %s, %s)
    '''

    mycursor.execute(sale_insertion, (email, name, car_id, rating))
    car_db.commit()


# sql query for selecting a car rating
def get_car_rating(car_id):
    global mycursor
    query = '''
    SELECT SALE.RATING
    FROM SALE JOIN CAR_AD
    ON SALE.CAR_ID = CAR_AD.ID
    WHERE CAR_AD.ID = %s;
    '''
    mycursor.execute(query, (car_id,))
    result = mycursor.fetchone()
    if result:
        return result[0]
    else:
        return "No rating found"


# sql query for getting the average rating of a sale by seller
def get_seller_avg_rating(seller_name):
    global mycursor
    query = '''
    SELECT AVG(RATING) as average_rating
    FROM SALE
    WHERE SELLER_NAME = %s;
    '''
    mycursor.execute(query, (seller_name,))
    result = mycursor.fetchone()
    if result and result[0]:
        return round(result[0], 2)
    else:
        return "No rating found"


# sql query for getting the average rating of a sale by user
def get_user_avg_rating(user_email):
    global mycursor
    query = '''
    SELECT AVG(RATING) as average_rating
    FROM SALE
    WHERE USER_EMAIL = %s;
    '''
    mycursor.execute(query, (user_email,))
    result = mycursor.fetchone()
    if result and result[0]:
        return round(result[0], 2)
    else:
        return "No rating found"


# sql query for  getting car ads by some filters
def get_car_ads_by_filters(car_make, car_body_type, car_year, car_location):
    global mycursor
    query = '''
    SELECT
        BRAND,
        MODEL,
        BODY_TYPE,
        YEAR,
        LOCATION,
        AVG(CAST(REPLACE(PRICE, ',', '') AS DECIMAL(10, 2))) AS AVG_PRICE,
        COUNT(ID) AS NUM_LISTINGS
    FROM
        CAR_AD
    WHERE
        BRAND = %s
        AND BODY_TYPE = %s
        AND YEAR = %s
        AND LOCATION = %s
    GROUP BY
        BRAND, MODEL, BODY_TYPE, YEAR, LOCATION
    ORDER BY
        MODEL;
    '''
    mycursor.execute(query, (car_make, car_body_type, car_year, car_location))
    result = mycursor.fetchall()
    if result:
        return result
    else:
        return "No ads found"


# sql query for filtering cars in a certain price range
def get_cars_in_price_range(location, min_price, max_price):
    global mycursor
    query = '''
    SELECT
        LOCATION,
        COUNT(ID) AS NUM_CARS,
        AVG(CAST(REPLACE(PRICE, ',', '') AS DECIMAL(10, 2))) AS AVG_PRICE
    FROM
        CAR_AD
    WHERE
        LOCATION = %s
        AND CAST(REPLACE(PRICE, ',', '') AS DECIMAL(10, 2)) BETWEEN %s AND %s
    GROUP BY
        LOCATION;
    '''
    mycursor.execute(query, (location, min_price, max_price))
    result = mycursor.fetchone()
    if result:
        return result
    else:
        return "No cars found"


# sql query for getting the top 5 areas that has a certain brand and model
def get_top_cairo_areas(brand, model):
    global mycursor
    query = '''
    SELECT
        LOCATION,
        COUNT(ID) AS NUM_CARS,
        AVG(CAST(REPLACE(PRICE, ',', '') AS DECIMAL(10, 2))) AS AVG_PRICE
    FROM
        CAR_AD
    WHERE
        BRAND = %s
        AND MODEL = %s
        AND UPPER(LOCATION) LIKE %s
    GROUP BY
        LOCATION
    ORDER BY
        NUM_CARS DESC,
        AVG_PRICE DESC
    LIMIT 5;
    '''
    mycursor.execute(query, (brand, model, '%CAIRO%'))
    results = mycursor.fetchall()
    if results:
        return results
    else:
        return "No Cars Found"


# sql query for getting the names of the top 5 sellers that lists the highest number of cars
def get_top_sellers():
    global mycursor
    query = '''
    SELECT
        NAME,
        YEAR,
        COUNT(ID) AS NUM_CARS,
        AVG(CAST(REPLACE(PRICE, ',', '') AS DECIMAL(10, 2))) AS AVG_PRICE
    FROM
        CAR_AD C INNER JOIN SELLER S
        ON C.ID = S.CAR_AD_ID
    GROUP BY
        C.YEAR, S.NAME
    ORDER BY
        NUM_CARS DESC
    LIMIT 5;
    '''

    mycursor.execute(query)
    results = mycursor.fetchall()
    if results:
        return results
    else:
        return "No Cars Found"


# sql query for getting all the cars listed by a certain seller
def get_cars_by_seller_name(seller_name):
    global mycursor
    query = '''
    SELECT ID, BRAND, MODEL, YEAR, PRICE
    FROM CAR_AD
    WHERE ID IN (
        SELECT CAR_AD_ID
        FROM SELLER
        WHERE NAME = %s
    )
    '''
    mycursor.execute(query, (seller_name,))
    results = mycursor.fetchall()
    if results:
        return results
    else:
        return "No Cars Found"


# sql query for getting the car brands that has the highest number of listings
def get_top_brands_and_models(start_year, end_year):
    global mycursor
    query = '''
    SELECT
        BRAND,
        MODEL,
        COUNT(ID) AS NUM_CARS,
        AVG(CAST(REPLACE(PRICE, ',', '') AS DECIMAL(10, 2))) AS AVG_PRICE
    FROM
        CAR_AD
    WHERE
        YEAR BETWEEN %s AND %s
    GROUP BY
        BRAND,
        MODEL
    ORDER BY
        NUM_CARS DESC,
        AVG_PRICE DESC
    LIMIT 5;
    '''
    mycursor.execute(query, (start_year, end_year))
    results = mycursor.fetchall()
    if results:
        return results
    else:
        return "No Cars Found"


def main():

    # functions that fetches the result of the corresponding queries
    def register_user():
        user_email = email_entry.get()
        user_username = username_entry.get()
        user_gender = gender_combobox.get()
        user_dob = dob_entry.get()
        user_phone = user_phone_entry.get()
        add_new_user(user_email, user_username, user_gender, user_dob, user_phone)

        # Clear the Entry and Combobox widgets
        email_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        gender_combobox.set('')
        dob_entry.delete(0, tk.END)
        user_phone_entry.delete(0, tk.END)

    def add_sale():
        sale_email = sale_email_entry.get()
        sale_name = sale_seller_name_entry.get()
        sale_car = int(sale_car_id_entry.get())
        sale_rate = int(sale_rating_combobox.get())
        add_new_sale(sale_email, sale_name, sale_car, sale_rate)

        # Clear the Entry and Combobox widgets
        sale_email_entry.delete(0, tk.END)
        sale_seller_name_entry.delete(0, tk.END)
        sale_car_id_entry.delete(0, tk.END)
        sale_rating_combobox.set('')

    def fetch_car_rating():
        car_id = int(car_id_entry.get())
        rating = get_car_rating(car_id)
        car_rating_label.config(text=f"Car Rating: {rating}")
        car_id_entry.delete(0, tk.END)

    def fetch_seller_avg_rating():
        seller_name = seller_name_entry.get()
        avg_rating = get_seller_avg_rating(seller_name)
        seller_avg_rating_label.config(text=f"Seller Average Rating: {avg_rating}")
        seller_name_entry.delete(0, tk.END)

    def fetch_user_avg_rating():
        user_email = user_email_entry.get()
        avg_rating = get_user_avg_rating(user_email)
        user_avg_rating_label.config(text=f"User Average Rating: {avg_rating}")
        user_email_entry.delete(0, tk.END)

    def fetch_car_ads_by_filters():
        input_car_make = brand_entry.get()
        input_car_body_type = body_type_entry.get()
        input_car_year = int(year_entry.get())
        input_car_location = location_entry.get()

        car_ads_result = get_car_ads_by_filters(input_car_make, input_car_body_type, input_car_year, input_car_location)

        if isinstance(car_ads_result, str):
            car_ads_label.config(text=car_ads_result)
        else:
            formatted_result = "\n".join([
                f"{row[0]} {row[1]} ({row[2]}, {row[3]}) - Location: {row[4]}, Avg Price: {row[5]:,.2f}, Num Listings: {row[6]}"
                for row in car_ads_result])
            car_ads_label.config(text=formatted_result)

        brand_entry.delete(0, tk.END)
        body_type_entry.delete(0, tk.END)
        year_entry.delete(0, tk.END)
        location_entry.delete(0, tk.END)

    def fetch_cars_in_price_range():
        input_location = location_entry2.get()
        input_min_price = float(min_price_entry.get())
        input_max_price = float(max_price_entry.get())

        cars_result = get_cars_in_price_range(input_location, input_min_price, input_max_price)

        if isinstance(cars_result, str):
            cars_label.config(text=cars_result)
        else:
            cars_label.config(
                text=f"Location: {cars_result[0]}, Num Cars: {cars_result[1]}, Avg Price: {cars_result[2]:,.2f}")

        location_entry2.delete(0, tk.END)
        min_price_entry.delete(0, tk.END)
        max_price_entry.delete(0, tk.END)

    def fetch_top_cairo_areas():
        input_car_brand = car_brand_entry.get()
        input_car_model = car_model_entry.get()

        result = get_top_cairo_areas(input_car_brand, input_car_model)
        if isinstance(result, str):
            car_areas_label.config(text=result)
        else:
            display_text = ''
            for row in result:
                display_text += f"Location: {row[0]}, Num Cars: {row[1]}, Avg Price: {row[2]:,.2f}\n"
            car_areas_label.config(text=display_text)

        car_brand_entry.delete(0, tk.END)
        car_model_entry.delete(0, tk.END)

    def fetch_top_sellers():
        result = get_top_sellers()
        if isinstance(result, str):
            top_sellers_label.config(text=result)
        else:
            display_text = ''
            for row in result:
                display_text += f"Name: {row[0]}, Year: {row[1]}, Num Cars: {row[2]}, Avg Price: {row[2]:,.2f}\n"
            top_sellers_label.config(text=display_text)

    def fetch_car_ads_by_seller_name():
        input_seller_name = seller_name1_entry.get()

        car_ads_result = get_cars_by_seller_name(input_seller_name)

        if isinstance(car_ads_result, str):
            car_ads_by_seller_label.config(text=car_ads_result)
        else:
            formatted_result = "\n".join([
                f"ID: {row[0]}, Brand: {row[1]}, Model: {row[2]}, Year: {row[3]}, Price: {row[4]}"
                for row in car_ads_result])
            car_ads_by_seller_label.config(text=formatted_result)

        seller_name1_entry.delete(0, tk.END)

    def fetch_top_brands_and_models():
        input_start_year = int(start_year_entry.get())
        input_end_year = int(end_year_entry.get())

        car_ads_result = get_top_brands_and_models(input_start_year, input_end_year)

        if isinstance(car_ads_result, str):
            car_ads_brands_label.config(text=car_ads_result)
        else:
            formatted_result = "\n".join([
                f"Brand: {row[0]}, Model: {row[1]}, Num Cars: {row[2]}, Avg Price: {row[3]:,.2f}"
                for row in car_ads_result])
            car_ads_brands_label.config(text=formatted_result)

        start_year_entry.delete(0, tk.END)
        end_year_entry.delete(0, tk.END)

    # tk instance to create a window
    root = tk.Tk()

    root.title("Car Marketplace")

    # registering a user part
    register_title_label = tk.Label(root, text="Register a User", font=("Helvetica", 10))
    register_title_label.grid(row=0, column=0, columnspan=2)

    email_label = tk.Label(root, text="Email")
    email_label.grid(row=1, column=0)
    email_entry = tk.Entry(root)
    email_entry.grid(row=1, column=1)

    username_label = tk.Label(root, text="Username")
    username_label.grid(row=2, column=0)
    username_entry = tk.Entry(root)
    username_entry.grid(row=2, column=1)

    gender_label = tk.Label(root, text="Gender")
    gender_label.grid(row=3, column=0)
    gender_combobox = ttk.Combobox(root, values=["M", "F"])
    gender_combobox.grid(row=3, column=1)

    dob_label = tk.Label(root, text="Date of Birth (YYYY-MM-DD)")
    dob_label.grid(row=4, column=0)
    dob_entry = tk.Entry(root)
    dob_entry.grid(row=4, column=1)

    user_phone_label = tk.Label(root, text="Phone Number")
    user_phone_label.grid(row=5, column=0)
    user_phone_entry = tk.Entry(root)
    user_phone_entry.grid(row=5, column=1)

    register_button = tk.Button(root, text="Register", command=register_user)
    register_button.grid(row=6, columnspan=2)

    separator = ttk.Separator(root, orient='vertical')
    separator.grid(row=0, column=2, rowspan=8, padx=10, sticky='ns')

    # Adding a sale
    sale_title_label = tk.Label(root, text="Add a Sale", font=("Helvetica", 10))
    sale_title_label.grid(row=0, column=3, columnspan=2)

    sale_email_label = tk.Label(root, text="User Email")
    sale_email_label.grid(row=1, column=3)
    sale_email_entry = tk.Entry(root)
    sale_email_entry.grid(row=1, column=4)

    sale_seller_name_label = tk.Label(root, text="Seller Name")
    sale_seller_name_label.grid(row=2, column=3)
    sale_seller_name_entry = tk.Entry(root)
    sale_seller_name_entry.grid(row=2, column=4)

    sale_car_id_label = tk.Label(root, text="Car ID")
    sale_car_id_label.grid(row=3, column=3)
    sale_car_id_entry = tk.Entry(root)
    sale_car_id_entry.grid(row=3, column=4)

    sale_rating_label = tk.Label(root, text="Rating (0-5)")
    sale_rating_label.grid(row=4, column=3)
    sale_rating_combobox = ttk.Combobox(root, values=[0, 1, 2, 3, 4, 5])
    sale_rating_combobox.grid(row=4, column=4)

    sale_button = tk.Button(root, text="ADD", command=add_sale)
    sale_button.grid(row=5, column=3, columnspan=2)

    separator1 = ttk.Separator(root, orient='vertical')
    separator1.grid(row=0, column=5, rowspan=30, padx=10, sticky='ns')

    seller_properties_title = tk.Label(root, text="Owner Properties")
    seller_properties_title.grid(row=0, column=6, columnspan=5)

    seller_name1_label = tk.Label(root, text="Name:")
    seller_name1_label.grid(row=1, column=6)
    seller_name1_entry = tk.Entry(root)
    seller_name1_entry.grid(row=1, column=7)

    fetch_seller_properties_button = tk.Button(root, text="Fetch Cars", command=fetch_car_ads_by_seller_name)
    fetch_seller_properties_button.grid(row=2, column=6, columnspan=5)

    car_ads_by_seller_label = tk.Label(root, text="Cars:")
    car_ads_by_seller_label.grid(row=3, column=6)

    top_areas_title = tk.Label(root, text="Get The Top 5 Areas in Cairo")
    top_areas_title.grid(row=14, column=6, columnspan=5)

    car_brand_label = tk.Label(root, text="Brand:")
    car_brand_label.grid(row=15, column=6)
    car_brand_entry = tk.Entry(root)
    car_brand_entry.grid(row=15, column=7)

    car_model_label = tk.Label(root, text="Model:")
    car_model_label.grid(row=16, column=6)
    car_model_entry = tk.Entry(root)
    car_model_entry.grid(row=16, column=7)

    fetch_cars_button = tk.Button(root, text="Fetch Areas", command=fetch_top_cairo_areas)
    fetch_cars_button.grid(row=17, column=7, columnspan=2)

    car_areas_label = tk.Label(root, text="")
    car_areas_label.grid(row=18, column=7, columnspan=5)

    horizontal_separator = ttk.Separator(root, orient='horizontal')
    horizontal_separator.grid(row=7, column=0, columnspan=10, pady=10, sticky='ew')

    top_sellers_title = tk.Label(root, text="Get The Top 5 Sellers by Year")
    top_sellers_title.grid(row=8, column=6, columnspan=5)

    fetch_sellers_button = tk.Button(root, text="Fetch Sellers", command=fetch_top_sellers)
    fetch_sellers_button.grid(row=9, column=7, columnspan=2)

    top_sellers_label = tk.Label(root, text="")
    top_sellers_label.grid(row=10, column=7, columnspan=5)

    get_rating_title = tk.Label(root, text="Get Rating for a Car Sale")
    get_rating_title.grid(row=8, column=0, columnspan=5)

    car_id_label = tk.Label(root, text="Car ID:")
    car_id_label.grid(row=9, column=0)
    car_id_entry = tk.Entry(root)
    car_id_entry.grid(row=9, column=1)

    fetch_button = tk.Button(root, text="Fetch Rating", command=fetch_car_rating)
    fetch_button.grid(row=9, column=2)

    car_rating_label = tk.Label(root, text="Sale Rating:")
    car_rating_label.grid(row=9, column=3)

    horizontal_separator = ttk.Separator(root, orient='horizontal')
    horizontal_separator.grid(row=10, column=0, columnspan=5, pady=10, sticky='ew')

    seller_avg_rating_title = tk.Label(root, text="Average Rating by Seller")
    seller_avg_rating_title.grid(row=11, column=0, columnspan=5)

    seller_name_label = tk.Label(root, text="Seller Name:")
    seller_name_label.grid(row=12, column=0)
    seller_name_entry = tk.Entry(root)
    seller_name_entry.grid(row=12, column=1)

    fetch_seller_avg_rating_button = tk.Button(root, text="Fetch Seller Rating", command=fetch_seller_avg_rating)
    fetch_seller_avg_rating_button.grid(row=12, column=2)

    seller_avg_rating_label = tk.Label(root, text="Seller Average Rating:")
    seller_avg_rating_label.grid(row=12, column=3)

    horizontal_separator2 = ttk.Separator(root, orient='horizontal')
    horizontal_separator2.grid(row=13, column=0, columnspan=10, pady=10, sticky='ew')

    user_avg_rating_title = tk.Label(root, text="Average Rating by User")
    user_avg_rating_title.grid(row=14, column=0, columnspan=5)

    user_email_label = tk.Label(root, text="User Email:")
    user_email_label.grid(row=15, column=0)
    user_email_entry = tk.Entry(root)
    user_email_entry.grid(row=15, column=1)

    fetch_user_avg_rating_button = tk.Button(root, text="Fetch User Rating", command=fetch_user_avg_rating)
    fetch_user_avg_rating_button.grid(row=15, column=2)

    user_avg_rating_label = tk.Label(root, text="User Average Rating:")
    user_avg_rating_label.grid(row=15, column=3)


    car_ads_separator = ttk.Separator(root, orient='horizontal')
    car_ads_separator.grid(row=16, column=0, columnspan=5, pady=10, sticky='ew')

    car_ads_title = tk.Label(root, text="Fetch Car Ads by Filters")
    car_ads_title.grid(row=17, column=0, columnspan=5)

    brand_label = tk.Label(root, text="Brand:")
    brand_label.grid(row=18, column=0)
    brand_entry = tk.Entry(root)
    brand_entry.grid(row=18, column=1)

    body_type_label = tk.Label(root, text="Body Type:")
    body_type_label.grid(row=18, column=2)
    body_type_entry = tk.Entry(root)
    body_type_entry.grid(row=18, column=3)

    year_label = tk.Label(root, text="Year:")
    year_label.grid(row=19, column=0)
    year_entry = tk.Entry(root)
    year_entry.grid(row=19, column=1)

    location_label = tk.Label(root, text="Location:")
    location_label.grid(row=19, column=2)
    location_entry = tk.Entry(root)
    location_entry.grid(row=19, column=3)

    fetch_car_ads_button = tk.Button(root, text="Fetch Car Ads", command=fetch_car_ads_by_filters)
    fetch_car_ads_button.grid(row=20, column=1, columnspan=2)

    car_ads_label = tk.Label(root, text="")
    car_ads_label.grid(row=21, column=0, columnspan=5)

    car_ads_separator1 = ttk.Separator(root, orient='horizontal')
    car_ads_separator1.grid(row=22, column=0, columnspan=10, pady=10, sticky='ew')

    price_range_title = tk.Label(root, text="Fetch Number of Cars and Avg Price by Location and Price Range")
    price_range_title.grid(row=23, column=0, columnspan=5)

    location_label2 = tk.Label(root, text="Location:")
    location_label2.grid(row=24, column=0)
    location_entry2 = tk.Entry(root)
    location_entry2.grid(row=24, column=1)

    min_price_label = tk.Label(root, text="Min Price:")
    min_price_label.grid(row=24, column=2)
    min_price_entry = tk.Entry(root)
    min_price_entry.grid(row=24, column=3)

    max_price_label = tk.Label(root, text="Max Price:")
    max_price_label.grid(row=25, column=0)
    max_price_entry = tk.Entry(root)
    max_price_entry.grid(row=25, column=1)

    fetch_cars_button = tk.Button(root, text="Fetch Cars", command=fetch_cars_in_price_range)
    fetch_cars_button.grid(row=26, column=1, columnspan=2)

    cars_label = tk.Label(root, text="")
    cars_label.grid(row=27, column=0, columnspan=5)

    top_brands_title = tk.Label(root, text="Top 5 Brands")
    top_brands_title.grid(row=23, column=6, columnspan=5)

    start_year_label = tk.Label(root, text="Start Year:")
    start_year_label.grid(row=24, column=6)
    start_year_entry = tk.Entry(root)
    start_year_entry.grid(row=24, column=7)

    end_year_label = tk.Label(root, text="End Year:")
    end_year_label.grid(row=25, column=6)
    end_year_entry = tk.Entry(root)
    end_year_entry.grid(row=25, column=7)

    fetch_brands_button = tk.Button(root, text="Fetch Brands", command=fetch_top_brands_and_models)
    fetch_brands_button.grid(row=26, column=7, columnspan=2)

    car_ads_brands_label = tk.Label(root, text="")
    car_ads_brands_label.grid(row=27, column=7, columnspan=5)

    root.mainloop()
    mycursor.close()
    car_db.close()


if __name__ == "__main__":
    main()
