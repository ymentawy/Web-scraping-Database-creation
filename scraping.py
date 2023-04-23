from bs4 import BeautifulSoup
import requests
import csv
import re

olx_url = "https://www.olx.com.eg"
counter = 0


def program(link):
    global olx_url
    global counter
    olx = requests.get(link)
    soup = BeautifulSoup(olx.content, "lxml")
    cars = soup.find_all("li", class_="c46f3bfe")  # the cars in the search page
    if len(cars) != 0:
        for car in cars:
            counter += 1
            car_id = 0
            car_brand = ''
            car_model = ''
            car_adtype = ''
            car_fuel = ''
            car_price = ''
            car_ptype = ''
            car_poption = ''
            car_year = ''
            car_ttype = ''
            car_condition = ''
            car_color = ''
            car_btype = ''
            car_capacity = ''
            car_video = ''
            car_vtour = ''
            seller_name = ''
            seller_join_year = ''
            seller_join_month = ''
            start = ''
            end = ''
            car_description = ''
            car_location = ''
            car_url = olx_url + car.article.div.a["href"]
            pattern = r"ID(\d+)\.html"
            result = re.search(pattern, car_url)
            if result:
                car_id = int(result.group(1))
            car_response = requests.get(car_url)
            car_soup = BeautifulSoup(car_response.content, "lxml")
            seller_divs = car_soup.find("div", class_="_1075545d _6caa7349 _42f36e3b d059c029")
            if seller_divs is not None:
                seller_name = seller_divs.find("span", class_="_261203a9 _2e82a662").text
                seller_join_date_div = seller_divs.find("div", class_="_05330198")
                if seller_join_date_div is not None:
                    seller_join_date = seller_join_date_div.find("span", class_="_34a7409b").text
                    seller_join_year = seller_join_date.split()[-1]
                    seller_join_month = seller_join_date.split()[2]
                else:
                    print('Seller date not found')
            else:
                print("Seller information not found.")
            car_description_div = car_soup.find("div", class_="_0f86855a")
            if car_description_div is not None:
                car_description = car_description_div.span.text
            else:
                print("Description not found.")
            car_location_div = car_soup.find("div", class_="_1075545d e3cecb8b _5f872d11")
            if car_location_div is not None:
                car_location = car_location_div.span.text
            else:
                print("Location not found.")
            details = car_soup.find("div", class_="_241b3b1e")
            if details is not None:
                car_details_divs = details.find_all("div", class_="_676a547f")
                for div in car_details_divs:  # extract the car details
                    car_attributes_divs = div.find("div", class_="b44ca0b3")
                    spans = car_attributes_divs.find_all("span")
                    if spans is not None:
                        if len(spans) >= 1:
                            attribute = spans[1].text
                            attribute_name = spans[0].text
                            if attribute_name == "Brand":
                                car_brand = attribute
                            elif attribute_name == "Model":
                                car_model = attribute
                            elif attribute_name == "Ad Type":
                                car_adtype = attribute
                            elif attribute_name == "Fuel Type":
                                car_fuel = attribute
                            elif attribute_name == "Price":
                                car_price = attribute
                            elif attribute_name == "Price Type":
                                car_ptype = attribute
                            elif attribute_name == "Payment Options":
                                car_poption = attribute
                            elif attribute_name == "Year":
                                car_year = attribute
                            elif attribute_name == "Kilometers":
                                car_mileage = attribute
                                if " to " in car_mileage:
                                    start, end = car_mileage.split(' to ')
                                else:
                                    start = end = car_mileage
                            elif attribute_name == "Transmission Type":
                                car_ttype = attribute
                            elif attribute_name == "Condition":
                                car_condition = attribute
                            elif attribute_name == "Color":
                                car_color = attribute
                            elif attribute_name == "Body Type":
                                car_btype = attribute
                            elif attribute_name == "Engine Capacity (CC)":
                                car_capacity = attribute
                            elif attribute_name == "Video":
                                car_video = attribute
                            elif attribute_name == "Virtual Tour":
                                car_vtour = attribute
                        else:
                            print("attribute not found")
            with open('CarInfo.csv', mode='a', newline='', encoding='utf-8-sig') as csv_file:
                writer = csv.writer(csv_file)
                if counter == 1:
                    writer.writerow(
                        ["ID", "Brand", "Model", "Ad Type", "Fuel Type", "Price", "Price Type", "Payment Options",
                         "Year",
                         "Kilometers start", "Kilometers end", "Transmission Type", "Condition", "Color", "Body Type",
                         "Engine Capacity (CC)", "Video", "Virtual Tour", "Description", "Location", "Car URL"])
                writer.writerow([car_id, car_brand, car_model, car_adtype, car_fuel, car_price, car_ptype, car_poption,
                                 car_year, start, end,
                                 car_ttype, car_condition, car_color, car_btype,
                                 car_capacity, car_video, car_vtour, car_description, car_location, car_url
                                 ])
            with open('SellerInfo.csv', mode='a', newline='', encoding='utf-8-sig') as csv1_file:
                writer = csv.writer(csv1_file)
                if counter == 1:
                    writer.writerow(["ID", "Seller Name", "Seller Join Year", "Seller Join Month", "URL"])
                writer.writerow([car_id, seller_name, seller_join_year, seller_join_month, car_url])
    print("in")


def main():
    j = 0
    while True:
        j += 1
        link = "https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?filter=new_used_eq_2%2Cyear_between_2000_to_2023"
        print(link)
        program(link)
        for i in range(2, 76):
            link = "https://www.olx.com.eg/en/vehicles/cars-for-sale/cairo/?page=" + str(
                i) + "&filter=new_used_eq_2%2Cyear_between_2000_to_2023"
            print(link)
            program(link)
        print(j)


main()
