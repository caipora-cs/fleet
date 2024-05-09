import boto3
import dataclasses
# from botocore.exceptions import ClientError
from sniper_bot.utils.style import style
from sniper_bot.models.token_model import TokenData

class DynamoDB:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource("dynamodb")
        self.client = boto3.client(
            "application-autoscaling"
        )  # The AWS SDK for Python (Boto3) to make connections
        self.table = self.dynamodb.Table("TokenData")

    def create_table(self):
        """Create the TokenData table in DynamoDB. It will provision a scalable read and write capacity."""
        self.dynamodb.create_table(
            TableName="TokenData",
            KeySchema=[
                {"AttributeName": "pair_id", "KeyType": "HASH"},
                {"AttributeName": "creation_timestamp", "KeyType": "RANGE"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "pair_id", "AttributeType": "S"},
                {"AttributeName": "creation_timestamp", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        # Wait until the table exists.
        self.dynamodb.Table("TokenData").wait_until_exists()

        # Print the table status
        print(style.GREEN + "Table Status: \n" + style.RESET)
        print(self.dynamodb.Table("TokenData").table_status)
        print(style.GREEN + "Table Items: \n" + style.RESET)
        print(self.dynamodb.Table("TokenData").item_count)

        # Define the autoscaling for read capacity
        self.client.register_scalable_target(
            ServiceNamespace="dynamodb",
            ResourceId="table/TokenData",
            ScalableDimension="dynamodb:table:ReadCapacityUnits",
            MinCapacity=5,
            MaxCapacity=100,
        )

        # Define the autoscaling for write capacity
        self.client.register_scalable_target(
            ServiceNamespace="dynamodb",
            ResourceId="table/TokenData",
            ScalableDimension="dynamodb:table:WriteCapacityUnits",
            MinCapacity=5,
            MaxCapacity=100,
        )

        # Define autoscaling policy for read capacity
        self.client.put_scaling_policy(
            PolicyName="ReadAutoScalingPolicy",
            ServiceNamespace="dynamodb",
            ResourceId="table/TokenData",
            ScalableDimension="dynamodb:table:ReadCapacityUnits",
            PolicyType="TargetTrackingScaling",
            TargetTrackingScalingPolicyConfiguration={
                "PredefinedMetricSpecification": {
                    "PredefinedMetricType": "DynamoDBReadCapacityUtilization"
                },
                "TargetValue": 70.0,
                "ScaleOutCooldown": 60,
                "ScaleInCooldown": 60,
            },
        )

        # Define autoscaling policy for write capacity
        self.client.put_scaling_policy(
            PolicyName="WriteAutoScalingPolicy",
            ServiceNamespace="dynamodb",
            ResourceId="table/TokenData",
            ScalableDimension="dynamodb:table:WriteCapacityUnits",
            PolicyType="TargetTrackingScaling",
            TargetTrackingScalingPolicyConfiguration={
                "PredefinedMetricSpecification": {
                    "PredefinedMetricType": "DynamoDBWriteCapacityUtilization"
                },
                "TargetValue": 70.0,
                "ScaleOutCooldown": 60,
                "ScaleInCooldown": 60,
            },
        )

    # CRUD operations
    def create_item(self, token_data: TokenData):
        self.table.put_item(Item=dataclasses.asdict(token_data))

    def read_item(self, pair_id: str):
        response = self.table.get_item(
            Key={
                'pair_id': pair_id,
            }
        )
        item = response.get('Item')
        return TokenData(**item) if item else None

    def update_item(self, pair_id: str, token_data: TokenData):
        item = dataclasses.asdict(token_data)
        update_expression = "SET " + ", ".join(f"{k} = :{k}" for k in item.keys())
        expression_attribute_values = {f":{k}": v for k, v in item.items()}
        self.table.update_item(
            Key={
                'pair_id': pair_id,
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )

    def delete_item(self, pair_id: str):
        self.table.delete_item(
            Key={
                'pair_id': pair_id,
            }
        )

        


def main():
    db = DynamoDB()
    # Create the table in DynamoDB for first time
    # db.create_table()


if __name__ == "__main__":
    main()
