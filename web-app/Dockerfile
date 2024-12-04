FROM node:16

RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg \
	&& echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-8.x.list \
	&& apt-get update \
	&& apt-get install filebeat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

EXPOSE ${PORT}

COPY filebeat.yml /etc/filebeat/filebeat.yml

COPY elastic-ca.crt /etc/filebeat/elastic-ca.crt

RUN chmod go-w /etc/filebeat/filebeat.yml

RUN filebeat modules enable system \
	&& sed -i '/enabled:/s/false/true/' /etc/filebeat/modules.d/system.yml

RUN npm install

RUN filebeat setup --dashboards -E setup.kibana.host=http://***

RUN filebeat setup --index-management \
	-E output.logstash.enabled=false \
	-E output.elasticsearch.hosts=[${ELASTICSEARCH_HOST}] \
	-E output.elasticsearch.username=${ELASTICSEARCH_USERNAME} \
	-E output.elasticsearch.password=${ELASTICSEARCH_PASSWORD} \
	-E output.elasticsearch.ssl.certificate_authorities=["/etc/filebeat/elastic-ca.crt"] \
	-E setup.kibana.host=KIBANA_ADDRESS:5601

CMD filebeat -e & node app.js
