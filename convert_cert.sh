#! /bin/bash

# $1 must be the certificate in p12 format

openssl pkcs12 -in $1 -out $1.crt.pem -clcerts -nokeys
openssl pkcs12 -in $1 -out $1.key.pem -nocerts -nodes
