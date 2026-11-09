# AI-Powered Cloud Resource Scaling

A Python project exploring predictive cloud resource management. Python-based system metrics collection feeds an AWS-based processing pipeline; deep learning models predict future CPU utilisation, and AWS Lambda functions use forecasts to inform Auto Scaling decisions.

## Project components

| File | Purpose |
| --- | --- |
| `cpu.py` | Collects CPU, memory, battery, temperature and network metrics and posts them to a local Node-RED endpoint. |
| `loadPredectionModel.ipynb` | Data exploration, preprocessing, and CPU usage prediction with LSTM and hybrid GRU-LSTM modelling. |
| `lambda_function.py` | AWS Lambda scaling logic using LSTM prediction CSVs stored in S3. |
| `lambda_function2.py` | AWS Lambda scaling logic using hybrid-model prediction CSVs stored in S3. |

## Technologies

Python, pandas, NumPy, scikit-learn, TensorFlow/Keras, Matplotlib, Seaborn, AWS S3, AWS Lambda, Amazon EC2 Auto Scaling, Node-RED, WMI, and psutil.

## Getting started

1. Create a Python virtual environment and install dependencies: `pip install -r requirements.txt`.
2. Configure AWS credentials through your local AWS profile, SSO, or an IAM role. **Do not insert access keys in source code.**
3. Update the example S3 bucket names, object paths, and Auto Scaling group names for your AWS environment.
4. Open `loadPredectionModel.ipynb` in Jupyter Notebook or VS Code and run the relevant cells once your data source is available.
5. For local metrics collection, start the Node-RED endpoint and ensure OpenHardwareMonitor's WMI interface is available on Windows before running `cpu.py`.

> **Important:** The AWS Lambda examples can change EC2 Auto Scaling capacity. Test with a non-production AWS account and review permissions and scaling bounds before running. The notebook requires access to the original project dataset, which is not included in this repository.

## Notes

- Notebook execution outputs have been cleared and embedded AWS credentials removed before publication.
- This repository documents an academic prototype; AWS resources, model artifacts, external datasets and Node-RED flows are not included. It is not a one-click deployable application.
- The `cpu.py` simulated timestamp increments by one hour after each two-second collection cycle, so timestamps do not represent wall-clock observation intervals.
