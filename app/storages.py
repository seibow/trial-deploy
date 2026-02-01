# storages.py
from storages.backends.s3boto3 import S3Boto3Storage
from mimetypes import guess_type

class StaticStorage(S3Boto3Storage):
    location = "static"
    custom_domain = 'd2e4sq3futvfaj.cloudfront.net'
    querystring_auth = False

    def _save(self, name, content):
        content_type, _ = guess_type(name)
        if content_type:
            content.content_type = content_type
        return super()._save(name, content)
