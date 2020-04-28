#!/usr/local/bin/python3

import json
import os
import xml.etree.ElementTree as xmltree
from logger import Logger
import shapefile


# 1 to read xml, 2 to read json, 3 to read csv

class Program:
    # !/usr/local/bin/python3
    import json
    import os
    import xml.etree.ElementTree as xmltree
    from logger import Logger

    class Program:
        def __init__(self, x, t, n):
            # this is the name of shapefile
            self.out_file = "\GPS_Pts.shp"
            self.type = t
            self.filename = n
            self.this_folder = os.path.dirname(x)
            # this_folder  = C:\
            self.data_folder = os.path.join(self.this_folder, os.pardir, os.pardir, "Internship")
            # data_folder = C:\..\..\Internship
            self.data_folder = os.path.abspath(self.data_folder)
            # data_folder = C:\Internship
            self.out_file = self.data_folder + self.out_file

            self.logger = Logger(os.path.join(self.data_folder, "log.txt"))
            # logger = C:\Internship

        def run(self):
            try:
                self.log_startup()
                # based on the key a certain file will be read
                if self.type == 1:
                    self.load_xml()
                elif self.type == 2:
                    self.load_json()
                else:
                    self.load_csv()
            except Exception as e:
                print(e.__repr__())

        # (Runs first) lets us know status of Reading folders and the location
        def log_startup(self):
            self.logger.log("Application starting up...")
            self.logger.log("Data folder: {0}".format(self.data_folder))

        # (1) Loads_XML
        def load_xml(self):
            filename = os.path.join(self.data_folder, self.filename)
            self.logger.log("Loading XML file: {0}".format(filename))
            dom = xmltree.ElementTree()
            dom.parse(filename)
            print()
            print("Titles of recent posts:")
            items = list(dom.findall("channel/item"))
            self.logger.log("Found {0} titles in RSS feed.".format(len(items)))
            for item in items:
                print("{0} [{1}]".format(
                    item.find("title").text,
                    item.find("link").text))
            print()

        # (2) Loads Json
        def load_json(self):
            filename = os.path.join(self.data_folder, self.filename)
            self.logger.log("Loading JSON file: {0}".format(filename))

            with open(filename, "r") as fin:
                data = json.loads(fin.read())
                print("Course title: {0}".format(data["Name"]))
                self.logger.log("Found course title to be: {0}".format(data["Name"]))
                engagements = data["Engagements"]
                print("Number of engagements: {0}".format(len(engagements)))
                print("Locations:")
                for e in engagements:
                    print("\t" + e["City"] + " on " + e["StartDate"] + " [active? " + str(e["ActiveEngagement"]) + "]")
            print()

        # (3) Loads CSV_Done
        def load_csv(self):
            filename = os.path.join(self.data_folder, self.filename)

            self.logger.log("Loading CSV file: {0}".format(filename))

            number = self.build_coordinates_lookup(filename, self.out_file,self.data_folder)

            case1 = number["1"]
            case2 = number["79"]

            address1 = case1["Address"]
            address2 = case2["Address"]

            self.logger.log("Case 1 is in {}".format(address1))
            self.logger.log("Case 2 is in {}".format(address2))

        @staticmethod
        def build_coordinates_lookup(filename, z,k):
            #k = 'shapefiles/test/testfile'
            cnt = 1
            print(z)
            output_shp = shapefile.Writer(z)
            output_shp.autoBalance = 1
            output_shp.field('X', 'F', 10, 8)
            output_shp.field('Y', 'F', 10, 8)
            output_shp.field('Date')
            output_shp.field('ID', 'N')

            location = dict()
            with open(filename, "r") as fin:
                for line in fin:
                    if line is None:
                        continue
                    if line.strip().startswith("#"):
                        continue
                    if line.strip().startswith("No"):
                        continue

                    parts = line.split(sep=',')
                    entry = {
                        "No": parts[0].strip(),
                        "IncidntNum": parts[1].strip(),
                        "Category": parts[2].strip(),
                        "Descript": parts[3].strip(),
                        "DayOfWeek": parts[4].strip(),
                        "Date": parts[5].strip(),
                        "Time": parts[6].strip(),
                        "PdDistrict": parts[7].strip(),
                        "Resolution": parts[8].strip(),
                        "Address": parts[9].strip(),
                        "X": parts[10].strip(),
                        "Y": parts[11].strip(),
                        "Location": parts[12].strip(),
                        "Pdld": parts[13].strip()
                    }
                    # create the point geometry
                    output_shp.point(float(parts[10].strip()), float(parts[11].strip()))
                    # add attribute data
                    output_shp.record(float(parts[10].strip()), float(parts[11].strip()), " ", parts[1].strip())
                    print("Feature " + str(cnt) + " added to Shapefile.")
                    cnt = cnt + 1
                    # formats the date correctly

            # Save shapefile
            output_shp.close()

            return location

    if __name__ == "__main__":
        X = "C:\Internship"
        filename = "Police_Department_Incidents_-_Previous_Year__2016_.csv"
        p = Program(X, 3, filename)
        p.run()
