from event import Event
import boto3
import os

if os.environ.get('AWS_EXECUTION_ENV'):
    from aws_xray_sdk.core import xray_recorder
    from aws_xray_sdk.core import patch_all

    patch_all()

ssm = boto3.client('ssm',region_name='us-east-2')

signature_public_key_parameter = ssm.get_parameter(
    Name='/external/accounts/dev/sso_signature_public_key',
    WithDecryption=True
)
encryption_private_key_parameter = ssm.get_parameter(
    Name='/external/accounts/dev/sso_encryption_private_key',
    WithDecryption=True
)
sso_cookie_name_parameter = ssm.get_parameter(
    Name='/external/accounts/dev/sso_cookie_name',
    WithDecryption=True
)

from oxauth import Strategy2

strategy = Strategy2(
    signature_public_key=signature_public_key_parameter['Parameter']['Value'],
    signature_algorithm="RS256",
    encryption_private_key=encryption_private_key_parameter['Parameter']['Value'],
    encryption_algorithm="A256GCM",
    encryption_method="dir"
)

class Output:
    def __init__(self):
        self.set_user_uuid(None)

    def set_user_uuid(self, value):
        self.__user_uuid = value

    def set_country_code(self, value):
        self.__country_code = value

    def to_dict(self):
        return {
            'general': {
                'user_uuid': self.__user_uuid or 'not logged in',
                'country_code': self.__country_code
            },
            'reading_progress': {
                'a_book_uuid': 'a_page_uuid'
            },
            'accounts': {
                'faculty_status': 'confirmed_faculty (dummy value for now)'
            },
            'diagnostics': {
                'region': os.environ.get('AWS_REGION'),
                'hostname': os.environ.get('HOSTNAME'),
                'lambda_event_body': os.environ.get('AWS_LAMBDA_EVENT_BODY'),
                'aws_execution_env': os.environ.get('AWS_EXECUTION_ENV'),
                'lambda_task_root': os.environ.get('LAMBDA_TASK_ROOT'),
            }
        }

def lambda_handler(event, context):
    event = Event(event)
    request = event.request()

    sso_cookie = request.parsedCookies().get(sso_cookie_name_parameter['Parameter']['Value'])

    output = Output()

    if sso_cookie != None:
        payload = strategy.decrypt(sso_cookie)
        output.set_user_uuid(payload.user_uuid)

    output.set_country_code(request.country_code())

    return render_diagnostic(output.to_dict())


def render_diagnostic(something):
    content = f"""
        <html>
            <head>
                <meta name="robots" content="noindex">
                <title>Me Spike diagnostics</title>
            </head>
            <body>
                {something}
            </body>
        </html>
        """

    response = {
        'status': '200',
        'headers': {
            'x-robots-tag': [{
                'key': 'X-Robots-Tag',
                'value': 'noindex'
            }]
        },
        'body': content
    }

    return response
