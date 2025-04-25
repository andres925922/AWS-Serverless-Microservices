def main(event, context):
    """
    Lambda function handler that returns a greeting message.
    
    Args:
        event (dict): The event data passed to the Lambda function.
        context (LambdaContext): The context object for the Lambda function.
        
    Returns:
        dict: A dictionary containing the status code and greeting message.
    """
    return {
        "statusCode": 200,
        "body": "Hello from AWS Lambda!"
    }