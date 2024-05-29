def lambda_handler(event, context):

    user = event['requestContext']['authorizer']['principalId'] 
    task_id = event['pathParameters']['id']

    # Create the item key
    ddb_key={
            'user': f"user#{user}",
            'id': f"task#{task_id}"
        }

    # Update the taskStatus field
    response = table.update_item(
        Key=ddb_key,
        UpdateExpression="set taskStatus = :taskStatus",
        ConditionExpression='attribute_exists(id)',
        ExpressionAttributeValues={
            ':taskStatus': 'Completed'
        },
        ReturnValues="UPDATED_NEW"
    )

    # Fetch the updated item from the response
    item=response['Attributes']

    print('Success - item updated')

    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(item)
    }
    
    return response

