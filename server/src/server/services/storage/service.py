from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any
from urllib.parse import quote

import aioboto3
import boto3
import certifi
from botocore.config import Config
from botocore.exceptions import ClientError

from ...config import settings

_CLIENT_PARAMS = {
    "endpoint_url": settings.S3_ENDPOINT_URL,
    "verify": certifi.where(),
    "region_name": settings.S3_REGION,
    "aws_access_key_id": settings.S3_ACCESS_KEY_ID,
    "aws_secret_access_key": settings.S3_SECRET_ACCESS_KEY,
    "config": Config(
        signature_version="s3v4",
        s3={"addressing_style": settings.S3_ADDRESSING_STYLE},
    ),
}

_CORS_METHODS = ["GET", "HEAD", "PUT"]
_CORS_HEADERS = ["content-type"]
_CORS_MAX_AGE_SECONDS = 3600


@lru_cache(maxsize=1)
def _presigner() -> Any:
    return boto3.client("s3", **_CLIENT_PARAMS)


@asynccontextmanager
async def _client() -> AsyncIterator[Any]:
    session = aioboto3.Session()
    async with session.client("s3", **_CLIENT_PARAMS) as client:
        yield client


class StorageService:
    def upload_url(self, key: str, content_type: str) -> str:
        return _presigner().generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.S3_BUCKET,
                "Key": key,
                "ContentType": content_type,
            },
            ExpiresIn=settings.S3_UPLOAD_URL_EXP_SECONDS,
        )

    def download_url(self, key: str, name: str | None = None) -> str:
        params: dict[str, str] = {"Bucket": settings.S3_BUCKET, "Key": key}

        if name is not None:
            params["ResponseContentDisposition"] = (
                f"attachment; filename*=UTF-8''{quote(name)}"
            )

        return _presigner().generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=settings.S3_DOWNLOAD_URL_EXP_SECONDS,
        )

    async def get_size(self, key: str) -> int | None:
        async with _client() as client:
            try:
                res = await client.head_object(Bucket=settings.S3_BUCKET, Key=key)
            except ClientError:
                return None

        return res["ContentLength"]

    async def delete(self, keys: Sequence[str]) -> None:
        if not keys:
            return

        async with _client() as client:
            for key in keys:
                try:
                    await client.delete_object(Bucket=settings.S3_BUCKET, Key=key)
                except ClientError:
                    continue

    async def check_access(self) -> None:
        async with _client() as client:
            await client.head_bucket(Bucket=settings.S3_BUCKET)

    async def set_cors(self, origins: Sequence[str]) -> list[str]:
        async with _client() as client:
            await client.put_bucket_cors(
                Bucket=settings.S3_BUCKET,
                CORSConfiguration={
                    "CORSRules": [
                        {
                            "AllowedOrigins": list(origins),
                            "AllowedMethods": _CORS_METHODS,
                            "AllowedHeaders": _CORS_HEADERS,
                            "MaxAgeSeconds": _CORS_MAX_AGE_SECONDS,
                        }
                    ]
                },
            )
            res = await client.get_bucket_cors(Bucket=settings.S3_BUCKET)

        return [
            origin
            for rule in res["CORSRules"]
            for origin in rule.get("AllowedOrigins", [])
        ]
