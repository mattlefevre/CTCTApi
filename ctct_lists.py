import json
import requests
from ctctapitest.ctct_api_base import CtctAPI


class CTCTLists(CtctAPI):
    """
    A set of methods intended to access, and otherwise manipulate, the List information in a CTCT account.

    """
    def __init__(self):
        CtctAPI.__init__(self)

    def get_list_info(self, modified_since=""):
        """
        Provides all of the high-level list information in a CTCT account, including the List IDs.

        :param modified_since: Optional. Use to retrieve a set of the lists that have been modified
                            since the date and time specified in ISO-8601 format.
                            Ex: yyyy-mm-ddThh:mm:ss
                            Ex: 2018-01-01T19:01:05
        :return: A JSON load with the requested list information.
        """
        lists_url = self.api_base_url + '/lists?'
        #  Adds the modified date to the URI, if it is not blank.
        if modified_since != "":
            lists_url += "email={}&".format(modified_since)
        # Adds API key to URL, as a necessary parameter
        lists_url += "api_key={}".format(self.api_key)
        print(lists_url)
        response = requests.get(lists_url, headers=self.request_headers)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print("\nSomething went wrong.\n")
            return json.loads(response.content.decode('utf-8'))

    def get_usable_list_info(self):
        """
        Takes the information gathered through get_list_info and converts it into a much smaller, handier dictionary.

        In the dictionary, the keys are the usable list IDs, and the values are the easy-to-ready list names from the
        CTCT account. For best use, use the values as a user-facing item, with the keys being useful in URIs for
        adding an manipulating contacts through the CTCT API.

        :return: A dictionary with k[v] pairs in the form of CTCT_List_ID[CTCT_List_Name], both strings.
        """
        list_info = self.get_list_info()
        usable_list_info = {}
        for item in list_info:
            usable_list_info[item['id']] = item['name']
        return usable_list_info

    def get_list_name(self):
        pass
    def get_list_id(self):
        pass
    def set_list_name(self):
        pass
