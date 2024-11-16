# ---- Build the Python App ----
# ---- Build the Python App ----
    FROM python:3.11-bookworm

    # Install supervisor
    RUN apt-get update && apt-get install -y supervisor
    
    # Set the working directory
    WORKDIR /workspace
    
    # Set PYTHONPATH to make `models` accessible as a top-level module
    ENV PYTHONPATH="${PYTHONPATH}:/workspace/svc"
    
    # Copy application code to the container
    COPY . .
    
    # Install Python dependencies
    RUN pip install --no-cache-dir --upgrade -r requirements.txt
    
    # Copy supervisord configuration
    COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
    
    # Expose the port used by the application
    EXPOSE 8088
    
    # Start Supervisor to manage the Python app
    # ENTRYPOINT ["python3", "-m", "svc"]
    # CMD ["python3", "-m", "svc", "--log-level=DEBUG"]
    
# Define default values for processes, workers, and fast mode
    ENV PROCESSES=1
    ENV WORKERS=1
    ENV FAST_MODE="false"

# Use conditional statement for --fast
    ENTRYPOINT ["sh", "-c", "python3 -m svc --processes $PROCESSES --workers $WORKERS $( [ \"$FAST_MODE\" = \"true\" ] && echo \"--fast\" )"]




# # ---- Build the PostgreSQL Base ----
# FROM postgres:latest AS postgres-base

# ENV POSTGRES_USER=postgres
# ENV POSTGRES_PASSWORD=password
# ENV POSTGRES_DB=postgresDB

# # ---- Build the Python App ----
# FROM python:3.11-bookworm

# # Install supervisor
# RUN apt-get update && apt-get install -y supervisor

# WORKDIR /workspace

# COPY . .

# RUN pip install --no-cache-dir --upgrade -r requirements.txt


# # Copy PostgreSQL binaries from the first stage
# COPY --from=postgres-base /usr/local/bin /usr/local/bin
# COPY --from=postgres-base /usr/lib/postgresql /usr/lib/postgresql
# COPY --from=postgres-base /usr/share/postgresql /usr/share/postgresql
# COPY --from=postgres-base /var/lib/postgresql /var/lib/postgresql

# # Add supervisord config
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# EXPOSE 8080 5455

# CMD ["/usr/bin/supervisord"]
