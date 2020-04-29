import hashlib
import random

# https://paytraildocs.netlify.app/payments/e2-interface/authcode/

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
    authcodeString = authcodeString[:-1]
    base64Authcode = str.encode(authcodeString)
    return hashlib.sha256(base64Authcode).hexdigest().upper()

merchantId = 1
merchantHash = ""
amount = 1
paymentMethods = "1,2"

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
