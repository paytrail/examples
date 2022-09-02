<?php

/**
 * Create payment using Paytrails PHP-SDK
 * https://github.com/paytrail/paytrail-php-sdk
 */

require 'vendor/autoload.php';

use Paytrail\SDK\Client;
use Paytrail\SDK\Request\PaymentRequest;
use Paytrail\SDK\Model\Customer;
use Paytrail\SDK\Model\CallbackUrl;

// Paytrail test credentials
$merchantId = 375917;
$merchantPass = 'SAIPPUAKAUPPIAS';

$platformName = 'CustomPlatform-WebShopName';
$amount = 1500; // Amount is in cents, 15.00 €
$stamp = microtime(); // Use any unique value
$reference = 'testPayment';
$currency = 'EUR';
$language = 'FI';
$email = 'foobar@nomail.com';
$successUrl = 'https://webshopUrl/success';
$cancelledUrl = 'https://webshopUrl/cancel';

// Create customer with minimum values
$customer = new Customer();
$customer->setEmail($email);

// Set minimum required callback urls
$redirectUrls = new CallbackUrl();
$redirectUrls->setSuccess($successUrl);
$redirectUrls->setCancel($cancelledUrl);

// Instantiate Paytrail Client
$client = new Client($merchantId, $merchantPass, $platformName);

// Create payment request with values
$paymentRequest = new PaymentRequest();
// Set minimum required values
$paymentRequest->setAmount($amount)
    ->setStamp($stamp)
    ->setReference($reference)
    ->setCurrency($currency)
    ->setLanguage($language)
    ->setCustomer($customer)
    ->setRedirectUrls($redirectUrls);

// Wrap payment creation to try catch block. In case failed payment, response contains error message.
try {
    $payment = $client->createPayment($paymentRequest);
} catch (\Exception $e) {
    echo $e->getMessage();
}

// Print out link to payment page
echo $payment->getHref();
