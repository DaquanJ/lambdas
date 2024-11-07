import boto3
import json
import os


def lambda_handler(event, context):

    #testing zone
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(event)
    # }

    # Initialize the SES client
    ses_client = boto3.client('ses', region_name=os.environ['AWS_REGION'])  # Change to your SES region

    # Retrieve parameters from the event
    sender = event['sender']
    subject = event['subject']
    body_html = event['body_html'] 
    body_text = event.get('body_text', None) # Optional

    # set our email details
    from_email = os.environ['FROM_EMAIL']
    to_email = [os.environ['TO_EMAIL']]

    # Set up the email parameters
    try:
        response = ses_client.send_email(
            Source= from_email,
            Destination={
                'ToAddresses': to_email,
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body_text
                    },
                    'Html': {
                        'Data': sender + body_html or body_text
                    }
                }
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps("Email Sent Successfully")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error sending email: {str(e)}')
        }