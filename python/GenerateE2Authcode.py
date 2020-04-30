import hashlib
import random

"""
This is an example how to calculate authcode for Paytrail E2 payment interface.
More information about authcode can be found in: https://paytraildocs.netlify.app/payments/e2-interface/authcode/
"""

def generateParamsIn(paymentParameters) -> str:
    """
    Generates PARAMS_IN parameter from paymentParameters
    :param paymentParameters:
    :return:
    """

    paramsIn = ""
    for key, value in paymentParameters.items():
        if key is not "MERCHANT_HASH":
            paramsIn += f"{key},"

    # Remove trailing comma ','
    paramsIn = paramsIn[:-1]
    return paramsIn


def generateAuthcode(paymentParameters) -> str:
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


merchantId = 1
merchantHash = ""
amount = 1
paymentMethods = "1,2"

# See accepted parameters from https://paytraildocs.netlify.app/payments/e2-interface/fields/
paymentParameters = {
    "MERCHANT_HASH": merchantHash,
    "MERCHANT_ID": merchantId,
    "URL_SUCCESS": f"https://test.url.com/success",
    "URL_CANCEL": f"https://test.url.com/cancel",
    "ORDER_NUMBER": f"ORDER-{random.randrange(1, 9000)}",
    "PARAMS_IN": "",
    "PARAMS_OUT": "PAYMENT_ID,TIMESTAMP,STATUS",
    "AMOUNT": str(amount),
    "PAYMENT_METHODS": paymentMethods
}
paymentParameters["PARAMS_IN"] = generateParamsIn(paymentParameters)
paymentParameters.update({"AUTHCODE": generateAuthcode(paymentParameters)})

print(generateAuthcode(paymentParameters))
