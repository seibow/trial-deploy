### プロジェクトタイトル  
***
# Habi(ハビ)　「人生設計をするアプリです」
### ロゴ画像  
<img width="350" height="300" alt="image" src="https://github.com/user-attachments/assets/ce620792-ec90-40a7-9ab6-8ef76b6dfe9d" />  

### プロジェクト概要
***
**Habi**は、人生の長期的な目標や夢を小さなステップに分け、  
日常の中で「小さな達成感」を積み重ねながら目標を実現するための**人生設計アプリ**です。  
忙しい日々の中でも、自分のペースで目標や夢に近づける設計になっています。
### 必要条件
***
- Python 3.10 以上  
- Django 5.2  
- MySQL 8.0 以上
- AWS EC2 環境（Linux）
### 開発環境構築手順  
***仮想環境（venv）を使用する場合***
***
###### リポジトリをクローン
`$ git clone https://github.com/2025-Autumn-RareTECH-Team-B/app.git`

###### ディレクトリへ移動
`$ cd app`

###### 仮想環境を作成・有効化
`$ python -m venv venv`  
`$ source venv/bin/activate`

###### 依存パッケージをインストール
`$ pip install -r requirements.txt`

###### DBマイグレーション
`$ python manage.py migrate`

###### 開発サーバー起動
`$ python manage.py runserver`  

もしくは、Docker を使用して環境を構築しても問題ありません。
### 環境変数設定（.env）
***
Djangoで使用する環境変数を、プロジェクト直下に `.env` ファイルとして作成してください。
###### Django設定
`SECRET_KEY=django-insecure-your-secret-key`

###### DB設定
`DB_NAME=app`  
`DB_USER=testuser`  
`DB_PASSWORD=testuser`

>※ MySQLをDockerで構築する場合は、
>以下の変数を docker-compose.yml 内で指定してください。
>###### MySQL設定
>`MYSQL_ROOT_PASSWORD=root`  
>`MYSQL_DATABASE=app`  
>`MYSQL_USER=testuser`  
>`MYSQL_PASSWORD=testuser` 

### セキュリティ対策
***
###### 本アプリは学習用に開発しています。
###### Djangoで開発するにあたり、理解しておくべきセキュリティ対策についてまとめます

#### SQLインジェクション
悪意あるSQL文を入力・実行された場合、脆弱性のあるアプリではデータベースの情報が盗まれたり、書き換えられたりする可能性がある。
- 対策：SQL文の組み立てには全てプレースホルダを使用、エスケープ処理をして実行させる→Django ORMを使用してSQL文をパラメータ化し、DBエンジン（今回はdjango.db.backends.mysql）でエスケープ処理を行っている

#### CSRF
ユーザーのセッション情報を盗み、正規のユーザーとしてなりすますことでユーザーの意図しない操作を実行させる。
- 対策：処理を実行するページをPOSTメソッドでアクセスするようにし、その「hiddenパラメータ」に秘密情報が挿入されるよう、前のページを自動生成して、実行ページではその値が正しい場合のみ処理を実行する→入力情報を送信する処理は全てPOSTメソッドでアクセス、{% csrf_token %}によりhiddenパラメータに秘密情報を挿入できるようにして、django.middleware.csrf.CsrfViewMiddlewareが実行前のページでcsrfトークンの発行・Cookieのセット、実行後のページでトークンの検証を行う。

#### XSS
脆弱性のあるアプリでは、悪意あるスクリプトが実行され、ユーザーのCookieなど重要な情報が盗まれる可能性がある。
- 対策1：ウェブページに出力する全ての要素に対して、エスケープ処理を施す。→Djangoのテンプレートエンジンでautoescape=onにしてあり、全ての出力要素はエスケープ処理される。
- 対策2：script要素の内容を動的に生成する仕様にはしていない→今回使用しているJavascriptにユーザー入力を求めるところはありません。
- 対策3：CSPを設定する→CSPはどの外部スクリプトの実行を許可するか？といった決まり事を設定したもの。今回時間の都合上、本アプリでは設定しておりません。

#### クリックジャッキング
通常のページにアクセスしたつもりが、見た目ではわからない仕込まれたページを操作したことになっていて、ユーザーの意図しない操作が行われ、重要な情報が公開されたりする可能性がある。
- 対策1：HTTPレスポンスヘッダに、X-Frame-Optionsヘッダフィールドを出力し、他ドメインのサイトからのframe要素やiframe要素による読み込みを制限する→django.middleware.clickjacking.XFrameOptionsMiddlewareの設定がdefaultでDENYになっていることから、全てのページで制限をかけている。
- 対策2：CSPでframe-ancestorsを設定する→今回時間の都合上CSPを設定しておりませんが、現状iframeを将来的にも使うことがないため、noneで設定するのが本来であるという認識です。

#### CORS設定
外部から本アプリのAPIを勝手に呼ばれることを防ぎたい時に設定する
- 対策：外部からのアクセスを許可する場合には、django-cors-headersというミドルウェアを使用して許可するORIGINだけを設定する→本アプリは全て同一originだけのやり取りであり、将来的にも同様の予定であるため、現時点での設定は不要、という認識です。

> 参考資料
> - 安全なウェブサイトの作り方
> <https://www.ipa.go.jp/security/vuln/websecurity/index.html>
> - Django公式ドキュメント    
> <https://docs.djangoproject.com/ja/5.2/topics/security/>