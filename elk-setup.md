Ubuntu Server 2 CPU 4 RAM 25 Storage

# Installation ELK

install packages

```bash
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
apt-get update
apt-get install elasticsearch kibana logstash filebeat nginx vim ufw rsyslog

# dont forget to save pass
```

# Nginx (if you want kibana to be on 80 too)

```bash
# add rule
sudo ufw allow 'Nginx FULL' # http and https
sudo ufw enable # if not
sudo ufw status

vim /etc/nginx/sites-available/elkhost
# add
server {
    listen 80;
    server_name elkhost; 
    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
# then link
ln -s /etc/nginx/sites-available/elkhost /etc/nginx/sites-enabled/elkhost

nginx -t # test
# /etc/hosts maybe you will need to change on your PC
systemctl reload nginx # reload
```

# Step by Step

## ES

JVM settings

```bash
echo "-Xms1g
-Xmx1g" > /etc/elasticsearch/jvm.options.d/jvm-heap.options
```

Run ES

```bash
systemctl daemon-reload
systemctl enable --now elasticsearch
```

test

```bash
systemctl status elasticsearch
curl -X GET "https://localhost:9200" --key certificates/elasticsearch-ca.pem  -k -u elastic:fb2Bw9wMRdLMNurrodGx
ss -altnp | grep 9200
tail -f /var/log/elasticsearch/elasticsearch.log
```

## Kibana

config change

```bash
vim /etc/kibana/kibana.yml
# uncomment
server.port: 5601
server.host: "localhost"
```

enrollement token (copy it)

```bash
/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

keys

```bash
/usr/share/kibana/bin/kibana-encryption-keys generate
# output insert into /etc/kibana/kibana.yml
xpack.encryptedSavedObjects.encryptionKey: 
xpack.reporting.encryptionKey: 
xpack.security.encryptionKey: 
```

run Kibana

```bash
systemctl enable --now kibana
```

test

```bash
systemctl status kibana
```

open port if needed

```bash
ufw allow 5601/tcp
```

login now to `elkhost/?code=388897` use token above or generate again, then get verification code from

```bash
/usr/share/kibana/bin/kibana-verification-code
```

## ELK Security Rule

- go to Security / Rules
- create a query rule and put as a payload: `message: "*;" OR message: "*&&*" OR message: "*||*" OR message: "*|*" OR message: "*ls*" OR message: "*cat*"`
- save it as an RCE checker
