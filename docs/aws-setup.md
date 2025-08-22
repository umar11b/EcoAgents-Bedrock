# AWS Bedrock Setup Guide

## Prerequisites

1. **AWS Account** with access to Bedrock
2. **AWS CLI** installed and configured
3. **Proper IAM permissions** for Bedrock

## Step 1: AWS Console Setup

### Enable Bedrock

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Click "Get started" or "Enable Bedrock"
3. Accept the terms of service
4. Wait for activation (may take a few minutes)

### Request Model Access

1. In Bedrock console, go to "Model access"
2. Request access to:
   - `anthropic.claude-3-sonnet-20240229-v1:0` (or latest version)
   - `anthropic.claude-3-haiku-20240307-v1:0` (for faster/cheaper testing)

## Step 2: IAM Permissions

Create an IAM user or role with these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
        "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
      ]
    }
  ]
}
```

## Step 3: Local AWS Configuration

```bash
# Configure AWS CLI
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1  # or your preferred region
```

## Step 4: Test Bedrock Access

```bash
# Test with AWS CLI
aws bedrock-runtime invoke-model \
    --model-id anthropic.claude-3-sonnet-20240229-v1:0 \
    --body '{"prompt":"Hello, how are you?","max_tokens":100}' \
    --cli-binary-format raw-in-base64-out
```

## Step 5: Update Our Agent

Once Bedrock is set up, we can update our agent to use real LLM calls instead of keyword matching.
