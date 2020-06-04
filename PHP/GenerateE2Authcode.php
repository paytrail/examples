<?php
function generateParamsIn(array $paymentParameters): string
{
    unset($paymentParameters["MERCHANT_HASH"]);
    return implode(",", array_keys($paymentParameters));
}

function generateAuthcode($paymentParameters): string
{
    $authcodeString = implode("|", array_values($paymentParameters));
    return strtoupper(hash("sha256", $authcodeString));
}

function formatHtml($paymentParameters): void
{
    array_walk($paymentParameters, function ($value, $key) use (&$inputs) {
        $inputs .= "<input name=\"$key\" type=\"hidden\" value=\"$value\">\n";
    });

    echo <<<END
HTML form for testing
-----------------------
<form action="https://payment.paytrail.com/e2" method="post">
$inputs
<input type="submit" value="Pay here">
</form>
END;
}

$merchantId = 13466;
$merchantHash = "6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ";
$amount = 59;
$paymentMethods = "1,2";

$paymentParameters = [
    "MERCHANT_HASH" => $merchantHash,
    "MERCHANT_ID" => $merchantId,
    "URL_SUCCESS" => "https://test.url.com/success",
    "URL_CANCEL" => "https://test.url.com/success",
    "ORDER_NUMBER" => "ORDER-" . random_int(0, 1000),
    "PARAMS_IN" => "",
    "PARAMS_OUT" => "PAYMENT_ID,TIMESTAMP,STATUS",
    "AMOUNT" => $amount,
    "PAYMENT_METHODS" => $paymentMethods
];

$paymentParameters["PARAMS_IN"] = generateParamsIn($paymentParameters);
$paymentParameters["AUTHCODE"] = generateAuthcode($paymentParameters);
formatHtml($paymentParameters);
