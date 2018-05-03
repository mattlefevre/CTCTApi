import json
import requests
from ctctapitest.ctct_api_base import CtctAPI
from ctctapitest.ctct_lists import CTCTLists


class CTCTContacts(CtctAPI):
    """
    This class builds on the items in the CtctAPI class, with explicit intention of setting up getter
    and setter methods for manipulating contact data within a Constant Contact account.
    """

    def __init__(self):
        CtctAPI.__init__(self)

    def get_contact_info(self, email="", status="ALL", limit="500", modified_since=""):
        """
        This is a broad method that, when taken with the base parameters, will return all contact information
        within a CTCT account.

        Additional information can be found here:
            http://developer.constantcontact.com/docs/contacts-api/contacts-collection.html

        Expected type for all parameters: string

        :param email: Optional - A standard email address. Ex: 'name@constantcontact.com'
        :param status: Optional (defaults to "ALL" when omitted)
            A selector for which contact types the query should return. Possible options include:
            - ALL: Default. Returns all contacts
            - ACTIVE: Contact considered an active member of account (not in any other status)
            - UNCONFIRMED: Contact has not confirmed membership to account.
            - OPTOUT: Contact has unsubscribed from mailings of this account.
            - REMOVED: Contact has been removed from all lists but can still be added to a list
        :param limit: Optional (defaults to 50 when omitted).A value between 1 and 500.
        :param modified_since: Optional. Use to retrieve a list of only contacts that have been modified
                            since the date and time specified in ISO-8601 format.
                            Ex: yyyy-mm-ddThh:mm:ss
                            Ex: 2018-01-01T19:01:05
        :return: a JSON string with requested information, accessible as a python dictionary.
        """
        print("Starting get_contact_info\n")
        contact_url = self.api_base_url + '/contacts?'
        #  Next few lines identify which parameters to include in URI and omit any that are blank.
        if email != "":
            contact_url += "email={}&".format(email)
        if status != "":
            contact_url += "status={}&".format(status)
        if limit != "":
            contact_url += "limit={}&".format(str(limit))
        if modified_since != "":
            contact_url += "modified_since={}&".format(modified_since)
        # Adds API key to URL, as a necessary parameter
        contact_url += "api_key={}".format(self.api_key)
        print(contact_url)
        response = requests.get(contact_url, headers=self.request_headers)
        if response.status_code == 200:
            print("\n200, baby!\n")
            return json.loads(response.content.decode('utf-8'))
        else:
            print("\nSomething went wrong.\n")
            return json.loads(response.content.decode('utf-8'))

    def set_add_new_contact(self, contact_email, action_by="ACTION_BY_OWNER",):
        """
        Adds a contact to Constant Contact, or updates the details, if the contact already exists.

        All parameters are expected to be strings.

        :param action_by: Indicates whether the contact initiated the action or the owner. Two
        possible values:
            - ACTION_BY_OWNER
            - ACTION_BY_VISITOR
        :param contact_email: The email address that's being added to this CTCT account.
        :return: An updated contact in CTCT.
        """
        print("Starting set_add_new_contact\n")
        # Updates URI
        add_contact_url = self.api_base_url + '/contacts?'
        if action_by != "":
            add_contact_url += "action_by={}&".format(action_by)
        add_contact_url += "api_key={}".format(self.api_key)
        # JSON object to be submitted to CTCT
        import_data = {
            "confirmed": True,
            "email_addresses": [{
                "confirm_status": "CONFIRMED",
                "email_address": contact_email,
                "opt_in_source": "ACTION_BY_OWNER",
                "status": "ACTIVE",
            }],
            "lists": [{
                "id": "1441322750"
            }]
        }
        print(add_contact_url)
        response = requests.post(url=add_contact_url, headers=self.request_headers, json=import_data)
        print(response)
        if response.status_code == 200:
            return json.loads(response.content.decode(encoding='utf-8'))
        elif response.status_code == 409:
            print("This contact already exists!")
            contact_id = contact_test.get_contact_info(contact_email)['results'][0]['id']
            print("GOT AN ID: ", contact_id, "\n See above\n")
            update_contact = self.set_update_contact(contact_email=contact_email, contact_id=contact_id)
            print("Done!")
            return update_contact
        else:
            print("\nSomething's amiss...\n")
            return json.loads(response.content.decode(encoding='utf-8'))

    def set_update_contact(self, contact_email, contact_id):
        """
        This method updates an existing contact within a CTCT account.

        :param contact_email: The email address of the contact to be updated.
        :param contact_id: The numerical identifier of a contact within a specific CTCT account. Accessed through
        the self.get_contact_info(contact_email)['results'][0]['id'] method[slices].
        :return: A json string that includes all updated info from the contact, accessible as a python dictionary
        """

        print("Starting set_update_contact\n")
        contact_url = self.api_base_url + '/contacts/'
        #  Next few lines identify which parameters to include in URI and omit any that are blank.
        contact_url += "{}?".format(str(contact_id))
        contact_url += "api_key={}".format(self.api_key)
        print(contact_url)
        import_data = {
            "confirmed": True,
            "email_addresses": [{
                "confirm_status": "CONFIRMED",
                "email_address": contact_email,
                "opt_in_source": "ACTION_BY_OWNER",
                "status": "ACTIVE",
            }],
            "lists": [{
                "id": "1441322750"
            }]
        }
        response = requests.put(url=contact_url, headers=self.request_headers, json=import_data)
        if response.status_code == 200:
            print("200, baby!")
            return json.loads(response.content.decode(encoding='utf-8'))
        else:
            print("\nSomething's amiss...\n")
            return json.loads(response.content.decode(encoding='utf-8'))

    def set_unsubscribe_contact(self, email_address):
        """
        A method that will update a contact in a CTCT account to be unsubscribed, effectively
        removing them from receiving any further email communications.

        :return: A JSON Load, probably? # TODO: Update this to tell me what, for real, is returned.
        """
        contact_id = str(self.get_contact_info(email_address)['results'][0]['id'])
        print('Starting set_unsubscribe_contact')
        contact_url = self.api_base_url + '/contacts/' + contact_id + "?"
        contact_url += "api_key={}".format(self.api_key)
        print("Contact ID =", contact_id)
        print(contact_url)
        response = requests.delete(contact_url, headers=self.request_headers)
        if response.status_code == 204:
            print("\nContact Deleted. This contact has been unsubscribed.\n")
            return None
        else:
            print("\nSomething's gone awry.\n")
            return json.loads(response.content.decode(encoding='utf-8'))


contact_test = CTCTContacts()
