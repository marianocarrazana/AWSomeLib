# AWSomeLib

A small module to use fastapi like decorators with AWS lambda and API gateway

Usage example:

```python
from awsomelib import AWSomeApp

app = AWSomeApp()


@app.main
def main(event, context):
    # Default route
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(event),
    }


@app.get("var/{param}")
def get_test(param: str):
    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps({"var": param}),
    }
```

Checkout a full example [here](https://github.com/marianocarrazana/AWSomeApp)
