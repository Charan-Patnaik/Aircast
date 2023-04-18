import os
import time
import boto3
from dotenv import load_dotenv

load_dotenv()

log_group_name = os.environ.get('AWS_LOG_GROUP_NAME')

# Initializing boto3 client with AWS credntials
clientlogs = boto3.client(
                        'logs', 
                        region_name=os.environ.get('AWS_REGION_NAME'),
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
                        )


def _log_event(log_stream:str, message:str):
    """Send a log event to a specified log stream.

    Args:
    log_stream (str): The name of the log stream to send the event to.
    message (str): The message to include in the log event.

    Returns:
    None: This function does not return any value.

    Raises:
    None: This function does not raise any exception.

    This is a private function which sends a log event with the specified message to the specified log stream. The event timestamp is set to the current time in milliseconds since the Unix epoch.
    """

    clientlogs.put_log_events(
    logGroupName = log_group_name,
    logStreamName = log_stream,
    logEvents=[
        {
            'timestamp':int(time.time()*1e3),
            'message': message
        }
    ]
)


def log_login_success(username: str):
    """Log a successful user login event.

    Args:
    username (str): The username of the user who logged in.

    Returns:
    None: This function does not return any value.

    Raises:
    None: This function does not raise any exception.

    This function sends a log event to the AWS CloudWatch Logs service indicating that a user has logged in successfully. The log event includes the username of the user who logged in.
    """

    _log_event(str(os.environ.get('AWS_LOG_USER_LOGIN')), f"User with username '{username}' logged in successfully!")

def log_login_failed(username: str):
    """Log a failed user login event.

    Args:
    username (str): The username of the user who failed to log in.

    Returns:
    None: This function does not return any value.

    Raises:
    None: This function does not raise any exception.

    This function sends a log event to the AWS CloudWatch Logs service indicating that a user has failed to log in. The log event includes the username of the user who failed to log in.
    """

    _log_event(str(os.environ.get('AWS_LOG_USER_LOGIN')), f"User with username '{username}' failed to login with provided password!")

def log_sign_up(username: str, email: str):
    """Log a user sign-up event.

    Args:
    username (str): The username of the user who signed up.
    email (str): The email address of the user who signed up.

    Returns:
    None: This function does not return any value.

    Raises:
    None: This function does not raise any exception.

    This function sends a log event to the AWS CloudWatch Logs service indicating that a user has signed up. The log event includes the username and email address of the user who signed up.
    """
    
    _log_event(str(os.environ.get('AWS_LOG_USER_SIGNUP')), f"User with username '{username}' and email '{email}' signed up successfully")



