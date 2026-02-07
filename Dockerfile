# =========================================================
# TEMPORARY ISOLATION DOCKERFILE (RENDER DEBUG)
# =========================================================
# Purpose:
# - Verify Render can start a container
# - Verify Docker CMD is executed
# - Verify logs appear
#
# NOTE:
# - This is NOT the final production Dockerfile
# - We will revert after confirmation
# =========================================================

FROM python:3.11-slim

# Diagnostic command:
# Print a message and keep container alive for 5 minutes
CMD ["sh", "-c", "echo 'HELLO FROM RENDER CONTAINER' && sleep 300"]
