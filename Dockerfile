FROM public.ecr.aws/lambda/python:3.9
COPY . /var/task
CMD ["lambda_function.lambda_handler"]