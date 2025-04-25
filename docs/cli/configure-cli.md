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
    "UserId": "xxxxxxxxxxxxxxxxxxxxx",
    "Account": "xxxxxxxxxxxxxxxxxxxxxxxx",
    "Arn": "arn:aws:iam::xxxxxxxxxxxxxxx:user/xxxxxx"
}
```