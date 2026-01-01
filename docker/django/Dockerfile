#pythonのイメージを指定
FROM python:3.13-slim
#オプション
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN mkdir /code
#コンテナのワークディレクトリを/codeに指定
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code
#ローカルのrequirements.txtをコンテナの/appフォルダ直下に置く
COPY requirements.txt ./
#pipコマンドとツールを最新にし、txtファイル内のパッケージをpipインストール
RUN pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install -r requirements.txt \
    && pip install boto3 django-storages
#ソースコードをコンテナにコピー
COPY ./app /code/app
COPY ./manage.py /code/manage.py
COPY ./templates /code/templates
COPY ./static /code/static

#Gunicorn起動コマンド
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn app.wsgi:application --chdir /code/app --bind 0.0.0.0:8000 --access-logfile /var/log/app/gunicorn.log --error-logfile /var/log/app/gunicorn.log"]
