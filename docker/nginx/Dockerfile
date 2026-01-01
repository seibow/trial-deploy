# ベースイメージ
FROM nginx:latest

# デフォルト設定を削除
RUN rm /etc/nginx/conf.d/default.conf

# habi.conf をコピー
COPY ./docker/nginx/conf.d/habi.conf /etc/nginx/conf.d/habi.conf