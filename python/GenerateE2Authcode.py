import hashlib
import random
import typing

"""
This is an example how to calculate authcode for Paytrail E2 payment interface.
More information about authcode can be found in: https://docs.paytrail.com/en/ch04s07.html#idm4813351648
"""

def generateParamsIn(paymentParameters: typing.Dict[str, str]) -> str:
    """
    Generates PARAMS_IN parameter from paymentParameters
    :param paymentParameters:
    :return paramsIn:
    """

    paramsIn = ""
    for key, value in paymentParameters.items():
        if key is not "MERCHANT_HASH":
            paramsIn += f"{key},"

    # Remove trailing comma ','
    return paramsIn[:-1]


def generateAuthcode(paymentParameters: typing.Dict[str, str]) -> str:
    """
    Generates authcode for E2 payment
    :param paymentParameters:
    :return authcode:
    """

    authcodeString = ""
    for key, value in paymentParameters.items():
        authcodeString += f"{value}|"

    # Remove trailing pipe '|'
    authcodeString = authcodeString[:-1]
    base64Authcode = str.encode(authcodeString)
    return hashlib.sha256(base64Authcode).hexdigest().upper()


# Demo merchant id and hash
merchantId = 13466
merchantHash = "6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ"
amount = 1
paymentMethods = "1,2"

# See accepted parameters from https://docs.paytrail.com/en/ch04s03.html#idm4814369536
paymentParameters = {
    "MERCHANT_HASH": merchantHash,
    "MERCHANT_ID": merchantId,
    "URL_SUCCESS": "https://test.url.com/success",
    "URL_CANCEL": "https://test.url.com/cancel",
    "ORDER_NUMBER": f"ORDER-{random.randrange(1, 9000)}",
    "PARAMS_IN": "",
    "PARAMS_OUT": "PAYMENT_ID,TIMESTAMP,STATUS",
    "AMOUNT": str(amount),
    "PAYMENT_METHODS": paymentMethods
}
paymentParameters["PARAMS_IN"] = generateParamsIn(paymentParameters)
paymentParameters.update({"AUTHCODE": generateAuthcode(paymentParameters)})

html ='<form action="https://payment.paytrail.com/e2" method="post">\n'
for key, value in paymentParameters.items():
    html += f'      <input name="{key}" type="hidden" value="{value}">\n'
html += '   <input type="submit" value="Pay here">\n</form>'

print("Html form to test:")
print(html)
