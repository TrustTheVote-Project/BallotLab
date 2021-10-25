# data.py
# read and write structured data

# from posixpath import relpath
from files import FileTools
import xmltodict
import json
import jsonschema

# import pprint

# error codes
## JSON errors
### JSON file isn't formatted correctly (can't be parsed)
ERR_JSON_FORMAT = 200
### JSON data didn't validate against the schema
ERR_JSON_SCHEMA = 201

# supported_ext_types = [".xml", ".XML"]
# supported_ext_types = [".json", ".JSON", ".xml", ".XML"]
supported_ext_types = [".json", ".JSON"]
# create a string of supported extensions from list
ext_types_str = " ".join(str(item) for item in supported_ext_types)


class ElectionData:
    """
    Open the specified Election Data File (EDF)
    Read data into Python objects.
    Read well-formatted json and xml only
    Raises RuntimeError for bad data
    """

    def __init__(self, data_file, data_dir, print_rpt=False):

        election_file = FileTools(data_file, data_dir)
        if not election_file.file_found:
            msg = "Election data file {} not found in directory {}"
            raise RuntimeError(msg.format(str(data_file, data_dir)))

        self.data_file = data_file
        self.data_dir = data_dir
        self.abs_path_to_data = election_file.abs_path_to_file
        self.ext = election_file.ext

        if self.ext not in supported_ext_types:
            msg = "Election data must be one of the following file types: " "{}. Got {}"
            raise RuntimeError(msg.format(ext_types_str, self.ext))

        # read data file into Python objects, based on type.
        if self.ext in [".xml", ".XML"]:
            self.election_rpt = self.parse_xml(self.abs_path_to_data)
        elif self.ext in [".json", ".JSON"]:
            # let's try to read the file
            self.election_rpt = self.parse_json(self.abs_path_to_data)
            if self.election_rpt != ERR_JSON_FORMAT:
                self.elect_name = self.election_rpt["Election"][0]["Name"]
                self.start_date = self.election_rpt["Election"][0]["StartDate"]
                self.end_date = self.election_rpt["Election"][0]["EndDate"]
                self.elect_type = self.election_rpt["Election"][0]["Type"]
                self.gpunits = self.election_rpt["GpUnit"]
                ## Disable schema validation code
                # if self.validate_json(self.election_rpt):
                #     # Read Election data from JSON dict, which is
                #     self.elect_name = self.election_rpt["Election"][0]["Name"]
                #     self.start_date = self.election_rpt["Election"][0]["StartDate"]
                #     self.end_date = self.election_rpt["Election"][0]["EndDate"]
                #     self.elect_type = self.election_rpt["Election"][0]["Type"]
                # else:
                #     print("JSON Schema Error!")

        if self.election_rpt != ERR_JSON_FORMAT:
            rpt_title = "Election Report"
            self.text_rpt = "{}\n".format(rpt_title)
            self.text_rpt += ("=" * len(rpt_title)) + "\n"

            # EDF file info
            self.text_rpt += "EDF name: {}\n".format(self.data_file)
            self.text_rpt += "Location:\n {}\n".format(self.abs_path_to_data)
            # Election contains BallotStyle, Candidate and Contest.
            self.text_rpt += "Election name: {}\n".format(self.elect_name)
            self.text_rpt += "Election type: {}\n".format(self.elect_type)
            self.text_rpt += "Start date: {}\n".format(self.start_date)
            self.text_rpt += "End date: {}\n".format(self.end_date)
            self.text_rpt += "GPUnits: \n{}\n".format(self.gpunits)
        else:
            self.text_rpt = "Report can't be generated. Error code:"

        if print_rpt:
            print(self.text_rpt)
        # pprint.pprint(self.election_rpt)

    def parse_xml(self, xml_file):
        """
        parse xml file into JSON-style dict
        """
        with open(xml_file) as xmlf:
            xml = xmlf.read()
        return xmltodict.parse(xml, dict_constructor=dict)

    def parse_json(self, json_file):
        """
        parse json file into dictionary
        """
        # read JSON file and perform basic JSON validation
        try:
            with open(json_file, "r") as jsf:
                json_data = json.load(jsf)
            return json_data
        except json.decoder.JSONDecodeError:
            print("JSON file is not well-formed: {}".format(json_file))
            return ERR_JSON_FORMAT

    def validate_json(self, json_data):
        json_schema_file = FileTools(
            "NIST_V2_election_results_reporting.json", "assets/schema"
        )
        json_schema = self.parse_json(json_schema_file.abs_path_to_file)
        jsonschema.validate(instance=json_data, schema=json_schema)
        # try:
        #     jsonschema.validate(instance=json_data, schema=json_schema)
        # except jsonschema.exceptions.ValidationError as err:
        #     return ERR_JSON_SCHEMA
        # return True


if __name__ == "__main__":
    # xml_election = ElectionData("nist_sample_election_report.xml", "assets/data")
    # json_election = ElectionData("NIST_sample.json", "assets/data/")
    json_election = ElectionData(
        "BallotStudio_16_Edits.JSON", "assets/data/", print_rpt=True
    )
    json_election = ElectionData(
        "JESTONS_PAPARDEV_&_AUG_2021.json", "assets/data/", print_rpt=False
    )
