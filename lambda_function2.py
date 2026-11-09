import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    # S3 and Auto Scaling configuration
    s3 = boto3.client('s3')
    autoscaling = boto3.client('autoscaling')
    
    bucket_name = "iot-sensor-data"  # Replace with your S3 bucket name
    file_name = "Hybridpredictions/Hybridpredicted_cpu_usage_next_2_hours.csv"  # Replace with your CSV file name
    auto_scaling_group_name = "auto_scaling_group"  # Replace with your Auto Scaling Group name

    # Fetch the CSV file from S3
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_name)
        csv_data = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_data))  # Read CSV into a DataFrame
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error fetching or parsing CSV: {str(e)}"
        }

    # Fetch the current capacity of the Auto Scaling group
    try:
        response = autoscaling.describe_auto_scaling_groups(AutoScalingGroupNames=[auto_scaling_group_name])
        current_capacity = response['AutoScalingGroups'][0]['DesiredCapacity']
        desired_capacity = current_capacity
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error fetching current Auto Scaling group capacity: {str(e)}"
        }

    # Process prediction data
    # Assuming the CSV has columns: Timestamp, Predicted_CPU_Usage
    actions = []
    for _, row in df.iterrows():
        load = row['Predicted_CPU_Usage']
        
        if load < 5:
            action = "Scale Down"
            desired_capacity = max(1, desired_capacity - 1)  # Minimum of 1 instance
        elif 5 <= load <= 10:
            action = "Maintain"
        else:
            action = "Scale Up"
            desired_capacity += 1

        actions.append({"Predicted_CPU_Usage": load, "action": action})
    
    # Log the calculated desired capacity
    print(f"Final desired capacity calculated: {desired_capacity}")

    # Trigger Auto Scaling if there's a valid desired capacity to set
    if desired_capacity is not None and desired_capacity != current_capacity:
        try:
            autoscaling.set_desired_capacity(
                AutoScalingGroupName=auto_scaling_group_name,
                DesiredCapacity=desired_capacity,
                HonorCooldown=True
            )
        except Exception as e:
            return {
                "statusCode": 500,
                "body": f"Error setting desired capacity in Auto Scaling: {str(e)}"
            }

    # Return scaling actions for logging or further processing
    return {
        "statusCode": 200,
        "body": actions
    }
