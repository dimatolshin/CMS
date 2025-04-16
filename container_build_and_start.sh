cp /root/cms/cms_backend/app/media/* /root/cms/storage/backend/media_data -v && \
docker-compose down && \
docker-compose up -d --build
