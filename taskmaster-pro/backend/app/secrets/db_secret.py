import boto3
from botocore.exceptions import ClientError
import json

def get_secret():
    secret_name = "fullstack-dev-db-postgres"
    region_name = "us-west-1"

    # 创建 Secrets Manager 客户端
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # 处理异常
        raise e

    # 秘密内容可能在 SecretString 或 SecretBinary 中
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    # 解析 JSON 格式的秘密
    secret_dict = json.loads(secret)
    return secret_dict

# Call the function
if __name__ == "__main__":
    try:
        secret_value = get_secret()
        print("Secret successfully retrieved.", secret_value)
    except Exception as e:
        print("Failed to retrieve the secret:", e)