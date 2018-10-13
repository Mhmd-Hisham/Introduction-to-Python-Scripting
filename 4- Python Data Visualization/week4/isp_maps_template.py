#!/usr/bin/env python3
# Instructors: Dr. Scott Rixner, Dr. Joe Warren
# Course: Python Data Visualization, University of Michigan, Coursera.
#

"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import os
import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = dict()
    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=separator, quotechar=quote)
        for row in reader:
            table[row[keyfield]] = row

    return table

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    codedata = read_csv_as_nested_dict(codeinfo["codefile"], codeinfo["plot_codes"],
                                       codeinfo["separator"], codeinfo["quote"] )

    return {country: codedata[country][codeinfo["data_codes"]] for country in codedata}

def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    mapping = {}
    missing = set()
    converter = build_country_code_converter(codeinfo)
    converter = {key.lower(): converter[key].lower() for key in converter}
    gdp_codes = {key.lower():key for key in gdp_countries}

    for country_code in plot_countries:
        lowercase = country_code.lower()
        if lowercase in converter and converter[lowercase] in gdp_codes:
            mapping[country_code] = gdp_codes[converter[lowercase]]
            continue

        missing.add(country_code)

    return mapping, missing

def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_countries = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_code"],
                                      gdpinfo["separator"], gdpinfo["quote"])

    mapped_codes, missing = reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries)

    mapping = {}
    no_data = set()

    for country_code in mapped_codes:
        gdpvalue = gdp_countries[mapped_codes[country_code]][year]
        if gdpvalue:
            mapping[country_code] = math.log10(float(gdpvalue))
            continue

        no_data.add(country_code)

    return mapping, missing, no_data

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by map_file.
    """
    mapping, missing, no_data = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)

    title = 'GDP by country for {} (log scale), unified by common country NAME'.format(year)
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = title
    worldmap_chart.add("GDP for {}".format(year), mapping)
    worldmap_chart.add("Missing from World Bank Data", missing)
    worldmap_chart.add("No GDP data", no_data)

    worldmap_chart.render_to_file(map_file)
    print(os.path.realpath(map_file))

    return None

def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
