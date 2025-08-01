import json
import boto3
import uuid
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShortUrls')

def lambda_handler(event, context):
    path = event.get("rawPath", "")
    method = event.get("requestContext", {}).get("http", {}).get("method", "")

    # ✅ OPTIONS handler for CORS preflight
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }

    # ✅ POST /shorten
    if method == "POST" and path == "/shorten":
        try:
            body = json.loads(event.get("body", "{}"))
            long_url = body.get("url")
            if not long_url:
                return {
                    "statusCode": 400,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": "Missing URL"
                }

            short_id = str(uuid.uuid4())[:8]
            ttl = int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp())

            table.put_item(Item={
                "id": short_id,
                "url": long_url,
                "expiresAt": ttl
            })

            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "text/plain"
                },
                "body": short_id
            }

        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": str(e)
            }

    # ✅ GET /{short_id}
    elif method == "GET" and path.startswith("/"):
        short_id = path.lstrip("/")
        try:
            response = table.get_item(Key={"id": short_id})
            item = response.get("Item")
            if item:
                return {
                    "statusCode": 302,
                    "headers": {
                        "Location": item["url"],
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": ""
                }
            else:
                return {
                    "statusCode": 404,
                    "headers": {"Access-Control-Allow-Origin": "*"},
                    "body": "Short URL not found"
                }
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": str(e)
            }

    # ❌ Fallback for unknown requests
    return {
        "statusCode": 400,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": "Invalid request"
    }
