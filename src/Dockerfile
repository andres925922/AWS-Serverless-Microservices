FROM public.ecr.aws/lambda/python:3.12

ARG LAMBDA_ROOT_SOURCE
# Copy common code and microservice code
COPY _layers/dependencies/python/common ${LAMBDA_TASK_ROOT}/common
COPY ${LAMBDA_ROOT_SOURCE} ${LAMBDA_TASK_ROOT}

# Copy shared requirements and install
COPY _layers/dependencies/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["${LAMBDA_HANDLER}"]