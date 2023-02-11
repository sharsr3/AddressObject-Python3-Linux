import mdAddr_pythoncode
import sys


class DataContainer:
    def __init__(self, address="", city="", state="", zip="", result_codes=[]):
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

        self.result_codes = result_codes


class AddressObject:
    

    def __init__(self, license, data_path):

        """ Create instance of Melissa Address Object """
        self.md_address_obj = mdAddr_pythoncode.mdAddr()

        """ Set license string and set path to data files  (.dat, etc) """
        self.md_address_obj.SetLicenseString(license)
        self.data_path = data_path

        self.md_address_obj.SetPathToUSFiles(data_path)
        self.md_address_obj.SetPathToAddrKeyDataFiles(data_path)
        self.md_address_obj.SetPathToDPVDataFiles(data_path)
        self.md_address_obj.SetPathToLACSLinkDataFiles(data_path)
        self.md_address_obj.SetPathToRBDIFiles(data_path)
        self.md_address_obj.SetPathToSuiteFinderDataFiles(data_path)
        self.md_address_obj.SetPathToSuiteLinkDataFiles(data_path)

        """    
        If you see a different date than expected, check your license string and either download the new data files or use the Melissa Updater program to update your data files.
        """

        p_status = self.md_address_obj.InitializeDataFiles()
        if (p_status != mdAddr_pythoncode.ProgramStatus.ErrorNone):
            print("Failed to Initialize Object.")
            print(p_status)
            return

        print(
            f"                DataBase Date: {self.md_address_obj.GetDatabaseDate()}")
        print(
            f"              Expiration Date: {self.md_address_obj.GetLicenseExpirationDate()}")

        """
        This number should match with file properties of the Melissa Object binary file.
        If TEST appears with the build number, there may be a license key issue.
        """
        print(
            f"               Object Version: {self.md_address_obj.GetBuildNumber()}\n")

    """ This will call the Lookup function to process the input address, city, state, and zip as well as generate the result codes """
    def execute_object_and_result_codes(self, data):
        self.md_address_obj.ClearProperties()

        self.md_address_obj.SetAddress(data.address)
        self.md_address_obj.SetCity(data.city)
        self.md_address_obj.SetState(data.state)
        self.md_address_obj.SetZip(data.zip)

        self.md_address_obj.VerifyAddress()
        result_codes = self.md_address_obj.GetResults()

        """ 
        ResultsCodes explain any issues Address Object has with the object.
        List of result codes for Address object
        https://wiki.melissadata.com/?title=Result_Code_Details#Address_Object

        """

        return DataContainer(data.address, data.city, data.state, data.zip, result_codes)


def parse_arguments():
    license, test_address, test_city, test_state, test_zip, data_path = "", "", "", "", "", ""

    args = sys.argv
    index = 0
    for arg in args:

        if (arg == "--license") or (arg == "-l"):
            if (args[index+1] != None):
                license = args[index+1]
        if (arg == "--address") or (arg == "-p"):
            if (args[index+1] != None):
                test_address = args[index+1]
        if (arg == "--city") or (arg == "-p"):
            if (args[index+1] != None):
                test_city = args[index+1]
        if (arg == "--state") or (arg == "-p"):
            if (args[index+1] != None):
                test_state = args[index+1]
        if (arg == "--zip") or (arg == "-p"):
            if (args[index+1] != None):
                test_zip = args[index+1]
        if (arg == "--dataPath") or (arg == "-d"):
            if (args[index+1] != None):
                data_path = args[index+1]
        index += 1

    return (license, test_address, test_city, test_state, test_zip, data_path)


def run_as_console(license, test_address, test_city, test_state, test_zip, data_path):
    print("\n\n=========== WELCOME TO MELISSA ADDRESS OBJECT LINUX PYTHON3 ===========\n")

    address_object = AddressObject(license, data_path)

    should_continue_running = True

    if address_object.md_address_obj.GetInitializeErrorString() != "No error.":
        should_continue_running = False

    while should_continue_running:
        if (test_address == None or test_address == "") and (test_city == None or test_city == "") and (test_state == None or test_state == "") and (test_state == None or test_state == ""):
            print("\nFill in each value to see the Address Object results")
            address = str(input("Address Line 1: "))
            city =    str(input("          City: "))
            state =   str(input("         State: "))
            zip =     str(input("           Zip: "))
        else:
            address = test_address
            city = test_city
            state = test_state
            zip = test_zip

        data = DataContainer(address, city, state, zip)

        """ Print user input """
        print("\n=============================== INPUTS ================================\n")
        print(f"               Address Line 1: {data.address}")
        print(f"                         City: {data.city}")
        print(f"                        State: {data.state}")
        print(f"                          Zip: {data.zip}")

        data_container = address_object.execute_object_and_result_codes(data)

        """ Print output """
        print("\n=============================== OUTPUT ================================\n")
        print("\n\tAddress Object Information:")

        print(
            f"\t                          MAK: {address_object.md_address_obj.GetMelissaAddressKey()}")
        print(
            f"\t               Address Line 1: {address_object.md_address_obj.GetAddress()}")
        print(
            f"\t               Address Line 2: {address_object.md_address_obj.GetAddress2()}")
        print(
            f"\t                         City: {address_object.md_address_obj.GetCity()}")
        print(
            f"\t                        State: {address_object.md_address_obj.GetState()}")
        print(
            f"\t                          Zip: {address_object.md_address_obj.GetZip()}")

        print(
            f"\t                 Result Codes: {data_container.result_codes}")

        rs = data_container.result_codes.split(',')
        for r in rs:
            print(
                f"        {r}: {address_object.md_address_obj.GetResultCodeDescription(r, mdAddr_pythoncode.ResultCdDescOpt.ResultCodeDescriptionLong)}")

        is_valid = False
        if not (test_address == None or test_address == ""):
            is_valid = True
            should_continue_running = False
        while not is_valid:

            test_another_response = input(
                str("\nTest another address? (Y/N)\n"))

            if not (test_another_response == None or test_another_response == ""):
                test_another_response = test_another_response.lower()
            if test_another_response == "y":
                is_valid = True

            elif test_another_response == "n":
                is_valid = True
                should_continue_running = False
            else:

                print("Invalid Response, please respond 'Y' or 'N'")

    print("\n============= THANK YOU FOR USING MELISSA PYTHON3 OBJECT ==============\n")


"""  MAIN STARTS HERE   """

license, test_address, test_city, test_state, test_zip, data_path = parse_arguments()

run_as_console(license, test_address, test_city, test_state, test_zip, data_path)
