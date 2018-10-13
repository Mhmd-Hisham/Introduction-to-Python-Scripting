#!/usr/bin/env python3
#
# Instructors: Dr. Scott Rixner, Dr. Joe Warren
# Course: Python Data Visualization, University of Michigan, Coursera.
#
# Submission datetime: 'Wed Sep 26 08:13:25 EET 2018'
#

"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
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

def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output:
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """

    plot_values = []

    for key in gdpdata:
        try:
            if gdpinfo["min_year"] <= int(key) <= gdpinfo["max_year"]:
                plot_values.append((int(key), float(gdpdata[key])))

        except ValueError:
            continue

    plot_values.sort()

    return plot_values

def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    mapping = {}
    gdpdata = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                      gdpinfo["country_name"],
                                      gdpinfo["separator"],
                                      gdpinfo["quote"])

    gdpdata = {key:{y:gdpdata[key][y] for y in gdpdata[key] if y.isdigit()} for key in gdpdata}
    for country in country_list:
        mapping[country] = build_plot_values(gdpinfo, gdpdata.get(country, {}))

    return mapping

def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """

    xy_chart = pygal.XY()
    xy_chart.title = 'Plot for GDP for selected countries spanning {} to {}'.format(
                                                                            gdpinfo["min_year"],
                                                                            gdpinfo["max_year"])
    xy_chart.x_title = "Year"
    xy_chart.y_title = "GDP in current US dollars"

    mapping = build_plot_dict(gdpinfo, country_list)
    for country in mapping:
        xy_chart.add(country, mapping[country])


    xy_chart.render_to_file(plot_file)

def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")



# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

test_render_xy_plot()
