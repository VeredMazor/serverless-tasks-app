import boto3
import json
import os

# Load environment variable for table name. This is done outside the handler
# to reuse the variable across multiple invocations of the lambda function.
TABLE_NAME = os.getenv('TASKS_TABLE')

# Set up DynamoDB resource outside the handler to reuse the resource
# across multiple invocations.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print('received:', event)

    # Retrieve the user ID from the request context. This assumes the user is authenticated
    # and the principalId is provided by an authorizer (e.g., Cognito or a custom authorizer).
    user = event['requestContext']['authorizer']['principalId']

    # Query DynamoDB for tasks belonging to the user
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('user').eq(f'user#{user}')
    )
    
    # Extract the items from the response
    items = response.get('Items', [])

    # Log the retrieved items for debugging purposes
    print(f'Retrieved items: {items}')

    # Build and return the HTTP response
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'  # Enable CORS
        },
        'body': json.dumps(items)
    }
    return response
