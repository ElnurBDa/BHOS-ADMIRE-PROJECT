```bash
docker build --add-host yelka.us-central1-b.c.getmoney-437018.internal:104.155.157.226 -t vulnerable-app .
docker run --add-host yelka.us-central1-b.c.getmoney-437018.internal:104.155.157.226  -p 3000:3000 -d vulnerable-app  

openssl s_client -connect elkhost:9200 -showcerts </dev/null 2>/dev/null | openssl x509 -outform PEM > elastic-ca.crt
```
