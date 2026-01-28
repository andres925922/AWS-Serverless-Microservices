FROM rabbitmq:3.13-management

# Enable the RabbitMQ management plugin
RUN rabbitmq-plugins enable --offline rabbitmq_management

# Expose the default RabbitMQ port and the management UI port
EXPOSE 5672 15672

# Run RabbitMQ server
CMD ["rabbitmq-server"]