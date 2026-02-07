# =========================================================
# TEMPORARY ISOLATION DOCKERFILE (RENDER DEBUG)
# =========================================================
# Purpose:
# - Verify that Render can start ANY container
# - Verify Docker CMD is executed
# - Verify logs appear in Render
#
# This is NOT the final production Dockerfile.
# We will revert after confirmation.
# =========================================================

FROM python:3.11-slim

# Diagnostic command:
# - Print a message to confirm container execution
# - Sleep for 5 minutes so the container stays alive
CMD ["sh", "-c", "echo 'HELLO FROM RENDER CONTAINER' && sleep 300"]
