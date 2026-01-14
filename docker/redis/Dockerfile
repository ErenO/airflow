# Redis image for Celery broker
FROM redis:7-alpine

# Expose Redis port
EXPOSE 6379

# Health check
HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
    CMD redis-cli ping || exit 1

CMD ["redis-server", "--bind", "0.0.0.0", "--port", "6379", "--appendonly", "yes"]
