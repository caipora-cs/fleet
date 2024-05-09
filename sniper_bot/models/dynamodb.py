import boto3

# from botocore.exceptions import ClientError
from sniper_bot.utils.style import style


class DynamoDB:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource("dynamodb")
        self.client = boto3.client(
            "application-autoscaling"
        )  # The AWS SDK for Python (Boto3) to make connections

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


def main():
    db = DynamoDB()
    db.create_table()


if __name__ == "__main__":
    main()
