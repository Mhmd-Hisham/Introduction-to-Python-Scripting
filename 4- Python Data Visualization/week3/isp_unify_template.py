#!/usr/bin/env python3
#
# Instructors: Dr. Scott Rixner, Dr. Joe Warren
# Course: Python Data Visualization, University of Michigan, Coursera.
#
# Submission datetime: 'Thu Sep 27 01:54:21 EET 2018'
#

"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

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

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    mapping = {}
    non_matching = set()

    for country_code in plot_countries:
        country = plot_countries[country_code]

        if country in gdp_countries:
            mapping[country_code] = country
            continue

        non_matching.add(country_code)

    return mapping, non_matching

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdpdata = read_csv_as_nested_dict(gdpinfo["gdpfile"], gdpinfo["country_name"],
                                      gdpinfo["separator"], gdpinfo["quote"])

    plot_countries, missing = reconcile_countries_by_name(plot_countries, gdpdata)

    mapping  = {}
    no_data = set()

    for country_code in plot_countries:
        gdpvalue = gdpdata[plot_countries[country_code]][year]
        if gdpvalue:
            mapping[country_code] = math.log10(float(gdpvalue))
            continue

        no_data.add(country_code)

    return mapping, missing, no_data

def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    mapping, missing, no_data = build_map_dict_by_name(gdpinfo, plot_countries, year)

    title = 'GDP by country for {} (log scale) unified by common country NAME'.format(year)
    worldmap_chart = pygal.maps.world.World(width=900, height=800)
    worldmap_chart.title = title
    worldmap_chart.add("GDP for {}".format(year), mapping)
    worldmap_chart.add("Missing from World Bank Data", missing)
    worldmap_chart.add("No GDP data", no_data)

    worldmap_chart.render_to_file(map_file)
    print(os.path.realpath(map_file))

def test_render_world_map():
    """
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
