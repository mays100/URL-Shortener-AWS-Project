import json
import os
import boto3
import random
import string
from urllib.parse import urlparse

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
# Get table name from environment variables
TABLE_NAME = os.environ.get('TABLE_NAME', 'ShortUrls')
table = dynamodb.Table(TABLE_NAME)

def generate_short_id(length=6):
    """Generates a random short ID."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def is_valid_url(url):
    """Checks if a given string is a valid URL."""
    try:
        result = urlparse(url)
        # Check if scheme (http/https) and netloc (domain) exist
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def shorten_url(event_body):
    """Handles POST /shorten requests to shorten a URL."""
    try:
        body = json.loads(event_body)
        long_url = body.get('url')

        if not long_url:
            return {
                'statusCode': 400,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({ 'message': 'Missing URL in request body.' })
            }

        # Ensure URL starts with http:// or https://
        if not long_url.startswith('http://') and not long_url.startswith('https://'):
            long_url = 'https://' + long_url # Default to https for convenience

        if not is_valid_url(long_url):
            return {
                'statusCode': 400,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({ 'message': 'Invalid URL format.' })
            }

        short_id = generate_short_id()
        # In a real-world scenario, you'd check for ID collisions and regenerate if needed.
        # For this simple app, we assume low collision probability.

        table.put_item(
            Item={
                'id': short_id,
                'url': long_url
            }
        )

        return {
            'statusCode': 200,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'short_id': short_id })
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'message': 'Invalid JSON in request body.' })
        }
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return {
            'statusCode': 500,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'message': 'Internal server error.' })
        }

def redirect_url(path):
    """Handles GET /{short_id} requests to redirect to the original URL."""
    # Extract short_id from the path (e.g., /abcde -> abcde)
    short_id = path.lstrip('/')

    if not short_id:
        return {
            'statusCode': 400,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'message': 'Missing short ID in path.' })
        }

    try:
        response = table.get_item(
            Key={
                'id': short_id
            }
        )
        item = response.get('Item')

        if item and 'url' in item:
            long_url = item['url']
            return {
                'statusCode': 302, # Redirect status code
                'headers': {
                    'Location': long_url # The URL to redirect to
                },
                'body': '' # Body is empty for redirects
            }
        else:
            return {
                'statusCode': 404,
                'headers': { 'Content-Type': 'application/json' },
                'body': json.dumps({ 'message': 'Short URL not found.' })
            }
    except Exception as e:
        print(f"Error redirecting URL: {e}")
        return {
            'statusCode': 500,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'message': 'Internal server error.' })
        }

def lambda_handler(event, context):
    """
    Main Lambda handler function.
    Determines if the request is for shortening or redirecting.
    """
    print(f"Received event: {json.dumps(event, indent=2)}")

    http_method = event.get('requestContext', {}).get('http', {}).get('method')
    path = event.get('rawPath')

    if http_method == 'POST' and path == '/':
        # This is a request to shorten a URL
        return shorten_url(event.get('body'))
    elif http_method == 'GET' and path != '/':
        # This is a request to redirect a short URL
        return redirect_url(path)
    else:
        # Handle unsupported methods or paths
        return {
            'statusCode': 405,
            'headers': { 'Content-Type': 'application/json' },
            'body': json.dumps({ 'message': 'Method Not Allowed or Invalid Path' })
        }
