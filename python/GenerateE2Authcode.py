import hashlib
import random
import typing

"""
This is an example how to calculate AUTHCODE Paytrail E2 payment interface.
More information about AUTHCODE can be found in: https://docs.paytrail.com/payments/e2-interface/authcode/
"""


def generateParamsIn(paymentParameters: typing.Dict[str, str]) -> str:
    """
    Generates PARAMS_IN parameter from paymentParameters
    :param paymentParameters:
    :return paramsIn:
    """

    paramsIn = [key for key in paymentParameters.keys() if key != "MERCHANT_HASH"]
    return ",".join(paramsIn)


def generateAuthcode(paymentParameters: typing.Dict[str, str]) -> str:
    """
    Generates authcode for E2 payment
    :param paymentParameters:
    :return authcode:
    """

    authcodeString = "|".join([str(value) for value in paymentParameters.values()])
    return hashlib.sha256(str.encode(authcodeString)).hexdigest().upper()


def formatItemRows(itemRows) -> dict:
    """
    Formats array of item rows to form
    {
         "ITEM_TITLE[0]": "test title",
         "ITEM_TITLE[1]": "test title 2"
    }

    :param itemRows:
    :return:
    """

    items = {}
    for title, item in itemRows.items():
        for index, value in enumerate(item):
            items[f"{title}[{index}]"] = value

    return items


def formatHTML(params: typing.Dict[str, str]) -> None:
    """
    Formats and prints paymentParameters as working HTML form

    :param params:
    :return None:
    """

    inputs = "\n".join([f'{"":4}<input name="{key}" type="hidden" value="{value}">' for key, value in params.items()])

    print("HTML form for testing")
    print("----------------------")
    print('<form action="https://payment.paytrail.com/e2" method="post">')
    print(inputs)
    print(f'{"":4}<input type="submit" value="Pay here">')
    print("</form>")


# Demo merchant id and hash
merchantId = 13466
merchantHash = "6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ"
amount = 59
paymentMethods = "1,2"

# See accepted parameters from https://docs.paytrail.com/payments/e2-interface/validation/
paymentParameters = {
    "MERCHANT_HASH": merchantHash,
    "MERCHANT_ID": merchantId,
    "URL_SUCCESS": "https://test.url.com/success",
    "URL_CANCEL": "https://test.url.com/cancel",
    "ORDER_NUMBER": f"PYTHON-EXAMPLE-ORDER-{random.randrange(1, 9000)}",
    "PARAMS_IN": "",
    "PARAMS_OUT": "PAYMENT_ID,TIMESTAMP,STATUS",
    "PAYMENT_METHODS": paymentMethods,
    "MSG_UI_MERCHANT_PANEL": "Message",
    #"AMOUNT": amount,  # Item rows and AMOUNT shouldn't be provided at the same time, remove this to submit item rows
    "URL_NOTIFY": "https://test.url.com/notify",
    "LOCALE": "fi_FI",
    "CURRENCY": "EUR",
    "REFERENCE_NUMBER": "1205769750",
    "PAYER_PERSON_PHONE": "040123123",
    "PAYER_PERSON_EMAIL": "theodor.tester@testcompany.com",
    "PAYER_PERSON_FIRSTNAME": "Theodor",
    "PAYER_PERSON_LASTNAME": "Tester",
    "PAYER_COMPANY_NAME": "Testcompany",
    "PAYER_PERSON_ADDR_STREET": "Test street",
    "PAYER_PERSON_ADDR_POSTAL_CODE": "23131",
    "PAYER_PERSON_ADDR_TOWN": "Test town",
    "PAYER_PERSON_ADDR_COUNTRY": "Test country",
    "VAT_IS_INCLUDED": "0",  # This is only used when item rows are provided
    "ALG": "1"
}

itemRows = {
    'ITEM_TITLE':
        [
            'Rubber boot',
            'Basket ball',
        ],
    'ITEM_ID':
        [
            '100',
            '101',
        ],
    'ITEM_QUANTITY':
        [
            '2',
            '1',
        ],
    'ITEM_UNIT_PRICE':
        [
            '10',
            '5',
        ],
    'ITEM_VAT_PERCENT':
        [
            '24',
            '24',
        ],
    'ITEM_DISCOUNT_PERCENT':
        [
            '0',
            '0',
        ],
    'ITEM_TYPE':
        [
            '1',
            '1',
        ],
}
# Discards item rows and VAT_IS_INCLUDED if AMOUNT is present in payment parameters
if "AMOUNT" in paymentParameters:
    itemRows = {}
    del paymentParameters['VAT_IS_INCLUDED']

itemRows = formatItemRows(itemRows)

# Merge paymentParameters and itemRows
paymentParameters = {**paymentParameters, **itemRows}
paymentParameters["PARAMS_IN"] = generateParamsIn(paymentParameters)
paymentParameters.update({"AUTHCODE": generateAuthcode(paymentParameters)})
formatHTML(paymentParameters)
