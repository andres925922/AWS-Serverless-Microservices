FROM public.ecr.aws/lambda/python:3.12

ARG LAMBDA_ROOT_SOURCE
# ARG LAMBDA_HANDLER

# Create function directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install AWS Lambda Runtime Interface Client
RUN pip install --no-cache-dir awslambdaric

# Copy common code first
COPY _layers/dependencies/python/common ./common/

# Copy the specific microservice code
COPY ${LAMBDA_ROOT_SOURCE}/ ./

# Copy shared requirements and install dependencies
COPY _layers/dependencies/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# # The handler will be executed using the Lambda Runtime Interface Client
# # LAMBDA_HANDLER environment variable will be in format: module.file.function (e.g. products.handler.handle)
# ENTRYPOINT [ "python3", "-m", "awslambdaric" ]
CMD ["handler.handle"]