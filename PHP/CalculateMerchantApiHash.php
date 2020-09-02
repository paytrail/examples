<?php

/**
 * This is example for calculating Merchant API authentication hash in case of refund.
 * Merchant API GET requests have always empty content, in this case use empty string as $requestContent variable when calculating content MD5
 */

$paymentId = 102402728626; // Payment id is returned after returning from payment back, $_GET['PAYMENT_ID'];

// Test merchant credentials
$merchantId = 13466;
$merchantSecret = '6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ';

$url = '/merchant/v1/payments/' . $paymentId . '/refunds';
$method = 'POST'; // Creating refund uses POST method

// Product we want to refund
$product = [
   'amount' => 1000, // Price is in cents, in this case price is 10.00€
   'description' => 'Test Product',
   'vatPercent' => 2400, // Vat 24.00%, comma is removed
];

// Create message content
$content = [
   'rows' => [
      $product,
   ],
   'email' => 'customer@email.com', // Customer email address
   'notifyUrl' => 'https://url.to.shop/apiNotification/', // Paytrail API will send return message to this url
];

$requestContent = json_encode($content);
/* Output is following
{"rows":[{"amount":1000,"description":"Test Product","vatPercent":2400}],"email":"customer@email.com","notifyUrl":"https:\/\/url.to.shop\/apiNotification\/"}
*/

$timestamp = (new DateTime())->format(DateTimeInterface::RFC3339); // 2020-05-01T12:00:00+0300

$md5Hash = hash('md5', $requestContent, true); // MD5 hash is in binary
$contentMd5 = base64_encode($md5Hash); // nYDNvmvsxI4ZxJL8OghRTw==

$hashHmacContent = implode("\n", [
   $method,
   $url,
   'PaytrailMerchantAPI ' . $merchantId,
   $timestamp,
   $contentMd5,
]);
/* This will output following string with line break character \n
POST
/merchant/v1/payments/102402728626/refunds
PaytrailMerchantAPI 13466
2020-05-01T12:00:00+0300
nYDNvmvsxI4ZxJL8OghRTw==
*/

$hashHmac = hash_hmac('sha256', $hashHmacContent, $merchantSecret, true); // Merchant secret is used as key, result is in binary

$authenticationHash = base64_encode($hashHmac); // tc51Vrg3HuLvwE1v0vul95Ux2hIE+COC3kT4EohrqTI=

// Message headers
$requestHeaders = [
   'Timestamp' => $timestamp, // This needs to be same timestamp used in calculating $authenticationHash
   'Content-MD5' => $contentMd5,
   'Authorization' => 'PaytrailMerchantAPI ' . $merchantId . ':' . $authenticationHash,
   'Refund-Origin' => 'internal', // This is required when using payment id as identifier
];

// Request body is $requestContent variable set earlier.
// Request is sent to 'https://api.paytrail.com/' . $url
