# How to configure AWS CLI

## AWS CLI instalation 
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

### Check instalation
`aws --version`

## Configure
`aws configure`

## Test connection
```bash
aws sts get-caller-identity

# Result
{
    "UserId": "AIDAY5OXZRUDQBIQYEVJ7",
    "Account": "613022272775",
    "Arn": "arn:aws:iam::613022272775:user/pela"
}
```