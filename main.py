# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from bs4 import BeautifulSoup
import requests
import csv
import concurrent.futures


# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def scrape(brand):
    brand_name = "_".join(str(brand.a['title']).split(" "))
    header = ['mark', 'model', 'version', 'version_production_years', 'version_doors', 'version_body_type',
              'specific_version', 'year', 'segment', 'transmission_full', 'transmission_short', 'engine_type',
              'fuel_type', 'engine_capacity (cc)', 'turbo', 'urban_consumption (l/100km)',
              'extra_urban_consumption (l/100km)', 'combined_consumption (l/100km)', 'co2_emission (g/km)', 'weight',
              'start/stop_system (yes/no)']

    with open(f'{brand_name}_cars_data.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        brand_scraping(brand, writer)


def brand_scraping(brand, writer):
    brand_name = brand.a['title']
    brand_name_href = brand.a['href']
    # print("_________________________________")
    # print(brand_name)
    # print(brand_name_href)
    # 2 Step: Go to the next url and check all models for each brand
    models_html_text = requests.get(brand_name_href).text
    soup_models = BeautifulSoup(models_html_text, "lxml")
    models_sections = soup_models.find_all('section', class_='models')
    # models = models_sections.find_all('div', class_='col-4')
    # print(models_sections)
    for m_section in models_sections:
        models = m_section.find_all('div', class_='col-4')

        for model in models:
            model_name = model.a['title']
            model_name_href = model.a['href']

            # print(brand_name)
            # print(model_name)
            # print(model_name_href)

            # 3 Step: Go to the next url and check all models versions for each model for each brand
            versions_html_text = requests.get(model_name_href).text
            soup_versions = BeautifulSoup(versions_html_text, 'lxml')
            versions_sections = soup_versions.find_all('section', class_='models')

            for v_section in versions_sections[:-1]:
                versions = v_section.find_all('div', class_='col-4')

                for version in versions:
                    version_name = version.a.p.text.replace(model_name, '').replace(' ', '').strip()
                    version_name_href = version.a['href']

                    version_name_list = version_name.split(",")
                    version_production_years = version_name_list[0]
                    version_doors = version_name_list[1]
                    version_body_type = version_name_list[2]

                    # print("Version of this model: ", version_name)
                    # print("URL: ", version_name_href)

                    # 4 Step: Go to the next url and check all specific versions for all years
                    specific_versions_html = requests.get(version_name_href).text
                    soup_specific_versions = BeautifulSoup(specific_versions_html, 'lxml')
                    specific_version_year = soup_specific_versions.find_all('a', class_='typesallyears')
                    # print("Model name: ", model_name)
                    # print("Version name: ", version_name)
                    # print("Spec_version_year: ", specific_version_year)

                    for year in specific_version_year:
                        version_year = year.text
                        version_year_href = year['href']
                        # print(version_year)
                        # print(version_year_href)
                        # 5 Step: Go to each year bookmark and check all specific versions for each year
                        year_html_text = requests.get(version_year_href).text
                        soup_year_versions = BeautifulSoup(year_html_text, 'lxml')
                        # year_versions_rows = soup_year_versions.find_all('div', class_='row')
                        year_versions_rows = soup_year_versions.find_all('h3')

                        for row in year_versions_rows:
                            final_full_car_name = row.a['title'].replace('specs', '')
                            final_full_car_href = row.a['href']

                            # final_car_transmission = row.find_all('div', class_='col-2')[1].text

                            # print("Final car name: ", final_full_car_name)
                            # print("Final car href: ", final_full_car_href)
                            # print("Fuel type: ", final_car_fuel)
                            # print("Transmission: ", final_car_transmission)
                            # print("Energy label: ", final_car_energy_label)

                            # 6 Step: Go further on specification page for each model and take necessary information
                            tech_specification_html_text = requests.get(final_full_car_href + "/tech").text
                            soup_tech_specification = BeautifulSoup(tech_specification_html_text, 'lxml')
                            tech_tables = soup_tech_specification.find_all('table')

                            sizes_specification_html_text = requests.get(final_full_car_href + "/sizes").text
                            soup_sizes_specification = BeautifulSoup(sizes_specification_html_text, 'lxml')
                            sizes_tables = soup_sizes_specification.find_all('table')

                            options_specification_html_text = requests.get(
                                final_full_car_href + "/options").text
                            soup_options_specification = BeautifulSoup(options_specification_html_text, 'lxml')
                            options_tables = soup_options_specification.find_all('table')

                            segment_spec = transmission_full_spec = transmission_short_spec = engine_type_spec = fuel_type_spec = "No info"
                            engine_capacity_spec = turbo_spec = urban_consumption_spec = co2_emission_spec = extra_urban_consumption_spec = combined_consumption_spec = weight = start_stop_option = "No info"

                            for tech_table in tech_tables:
                                for tr in tech_table:

                                    if "Transmission:" in tr.text:
                                        transmission_full_spec = tr.text.replace("Transmission:", '')
                                        if 'semi-automatic' in transmission_full_spec.lower():
                                            transmission_short_spec = "Semi-Automatic"
                                        elif "automatic" in transmission_full_spec.lower():
                                            transmission_short_spec = "Automatic"
                                        elif "manual" in transmission_full_spec.lower():
                                            transmission_short_spec = "Manual"
                                        else:
                                            transmission_short_spec = "N/A"
                                        # print("Segment: ", segment_spec)

                                    if "Co2 Emissions:" in tr.text and "g/km" in tr.text:
                                        co2_emission_spec = tr.text.replace("Co2 Emissions:", '').replace("g/km",
                                                                                                          '')

                                    if "Segment:" in tr.text:
                                        segment_spec = tr.text.replace("Segment:", '')
                                        # print("Segment: ", segment_spec)

                                    if "Engine/motor" in tr.text:
                                        engine_type_spec = tr.text.replace("Engine/motor Type:", '')
                                        # print("Engine type: ", engine_type_spec)

                                    if "Fuel Type" in tr.text:
                                        fuel_type_spec = tr.text.replace("Fuel Type:", '')
                                        # print("Fuel Type: ", fuel_type_spec)

                                    if "Engine Capacity:" in tr.text:
                                        engine_capacity_spec = tr.text.replace("Engine Capacity:", '').replace(
                                            "cc",
                                            '')
                                        # print("Engine Capacity: ", engine_capacity_spec)

                                    if "Turbo:" in tr.text:
                                        turbo_spec = tr.text.replace("Turbo:", '')
                                        # print("Turbo: ", turbo_spec)

                                    if "Urban Consumption:" in tr.text:
                                        urban_consumption_spec = tr.text.replace("Urban Consumption:",
                                                                                 '').replace(
                                            "l/100km", '')
                                        # print("Urban Consumption: ", urban_consumption_spec)
                                    if "Extra-urban Consumption:" in tr.text:
                                        extra_urban_consumption_spec = tr.text.replace("Extra-urban Consumption:",
                                                                                       '').replace(
                                            "l/100km", '')

                                    if "Combined Consumption:" in tr.text:
                                        combined_consumption_spec = tr.text.replace("Combined Consumption:",
                                                                                    '').replace(
                                            "l/100km", '')

                            # Collecting information from technical specification
                            for options_table in options_tables:
                                for tr in options_table:
                                    if "Start / Stop System:" in tr.text:
                                        start_stop_option = tr.text.replace("Start / Stop System:", '')

                            for sizes_table in sizes_tables:
                                for tr in sizes_table:
                                    if "Curb Weight:" in tr.text:
                                        weight = tr.text.replace("Curb Weight:", '').replace("kg", '')


                            one_row = [brand_name, model_name, version_name, version_production_years,
                                       version_doors, version_body_type, final_full_car_name, version_year,
                                       segment_spec, transmission_full_spec, transmission_short_spec,
                                       engine_type_spec, fuel_type_spec,
                                       engine_capacity_spec, turbo_spec, urban_consumption_spec,
                                       extra_urban_consumption_spec, combined_consumption_spec,
                                       co2_emission_spec, weight,
                                       start_stop_option]
                            writer.writerow(one_row)


def retrieve_all_bands(url_to_scrap):
    brands_html_text = requests.get(url_to_scrap).text
    soup_brands = BeautifulSoup(brands_html_text, "lxml")
    brands = soup_brands.find_all('div', class_='col-2 center')
    return brands


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = "https://www.cars-data.com/en/car-brands-cars-logos.html"
    bands = retrieve_all_bands(url_to_scrap=url)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for brand in bands:
            futures.append(executor.submit(scrape, brand=brand))
        # for future in concurrent.futures.as_completed(futures):
        #     print(future.result())
