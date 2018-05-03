import os

class CtctAPI(object):
    """
    A class that instantiates the base information needed to access the Constant Contact API.
    CTCT: An abbreviation for "Constant Contact." This abbreviation is used extensively.

    - API Key: A key generated through Constant Contact's Mashery instance. Found at the below URL:
    http://developer.constantcontact.com
    - API Secret: Generated at the same time as the CTCT API Key. DO NOT SHARE EITHER ITEM.
    - API Access Token: Account-specific access token. If the program you're using is only used on one CTCT account,
    the token can be generated here: https://constantcontact.mashery.com/io-docs
   If this program is intended to be used with multiple CTCT accounts, you'll need to utilize an O-Auth flow.

    """
    def __init__(self):
        """
        TODO: Update the api_key, api_secret, api_access_token to call to a system location,
        TODO: rather than typing out the actual values.
        """
        self.api_key = os.environ.get('ctct_api_key')
        self.api_secret = os.environ.get('ctct_api_secret')
        self.api_access_token = os.environ.get('ctct_api_token')
        self.api_base_url = 'https://api.constantcontact.com/v2'
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(self.api_access_token),
            'redirect_uri': 'http://localhost',
            "client_secret": "{}".format(self.api_secret)
        }
        # self.response_headers = {
        #     'Content-Type': 'application/json;charset=UTF-8',
        #     'Date': 'Wed, 11 Apr 2018 02:34:54 GMT',
        #     'Server': "Apache",
        #     'X-Mashery-Responder': 'prod-j-worker-us-east-1d-62.mashery.com',
        #     'Content-Length': '423',
        #     'Connection': 'keep-alive'
        # }