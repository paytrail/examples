<?php

$account = '375917';
$secret = 'SAIPPUAKAUPPIAS';
$method = 'POST';

$headers = [
    'checkout-account' => $account,
    'checkout-algorithm' => 'sha256',
    'checkout-method' => $method,
    'checkout-nonce' => '564635208570151',
    'checkout-timestamp' => '2022-08-24T10:01:31.904Z',
    'content-type' => 'application/json; charset=utf-8'
];

$body = [
    'stamp' =>  'e77880bd52bd45559bbd0467ffa86b77', // Unique identifier for payment
    'reference' => '3759170',
    'amount' => 1525,
    'currency' => 'EUR',
    'language' => 'FI',
    'customer' => [
        'email' => 'test.customer@example.com'
    ],
    'redirectUrls' => [
        'success' => 'https://ecom.example.com/cart/success',
        'cancel' => 'https://ecom.example.com/cart/cancel'
    ]
];

// JSON encode body
$body = json_encode($body, JSON_UNESCAPED_SLASHES);

// Keep only checkout- params, more relevant for response validation. Filter query
// string parameters the same way - the signature includes only checkout- prefixed values.
$includedKeys = array_filter(array_keys($headers), function ($key) {
    return preg_match('/^checkout-/', $key);
});

// Keys must be sorted alphabetically
sort($includedKeys, SORT_STRING);

// Format headers in key:value format
$hmacPayload = array_map(
    function ($key) use ($headers) {
        return join(':', [ $key, $headers[$key] ]);
    },
    $includedKeys
);
/**
 * hmacPayload array:
 * checkout-account:375917
 * checkout-algorithm:sha256
 * checkout-method:POST
 * checkout-nonce:564635208570151
 * checkout-timestamp:2022-08-24T10:01:31.904Z
 */

// Append hmacPayload to body
array_push($hmacPayload, $body);

// Add line breaks to payload
$hmacPayload = join("\n", $hmacPayload);

$hmac = hash_hmac('sha256', $hmacPayload, $secret); // 15d65afa74ba4a118869503f097bd42890c696350043ab7c1e51c790e8c22baf

// Use hmac in signature header
$headers['signature'] = $hmac;

/**
 * Headers array:
 * [checkout-account] => 375917
 * [checkout-algorithm] => sha256
 * [checkout-method] => POST
 * [checkout-nonce] => 564635208570151
 * [checkout-timestamp] => 2022-08-24T10:01:31.904Z
 * [content-type] => application/json; charset=utf-8
 * [signature] => 15d65afa74ba4a118869503f097bd42890c696350043ab7c1e51c790e8c22baf
 */