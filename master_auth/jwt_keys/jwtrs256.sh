ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key -N ""
# Don't add passphrase
openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub
cat jwtRS256.key
cat jwtRS256.key.pub