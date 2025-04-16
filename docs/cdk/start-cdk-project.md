# Setting Up Your Environment
## Prerequisites

1) Node.js and NPM: CDK CLI is built on Node.js, so you need to have Node.js and npm installed.
   `npm install -g aws-cdk`

2) Python: Install Python and set up a virtual environment.
   ```
   python3 -m venv .env
   source .env/bin/activate
   ```

3) AWS CLI: Configure AWS CLI with your credentials.
   ```
   pip install awscli
   aws configure
   ```
## Initialize a New CDK Project

1) Create and Initialize CDK App:
   ```
   mkdir my-cdk-app
   cd my-cdk-app
   cdk init app --language python
   ```

2) Install Dependencies:
   pip install -r requirements.txt