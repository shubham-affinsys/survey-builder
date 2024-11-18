
FROM python:3.11-bookworm
RUN apt-get update && apt-get install -y supervisor
WORKDIR /workspace    
ENV PYTHONPATH="${PYTHONPATH}:/workspace/svc"    
COPY . .    
RUN pip install --no-cache-dir --upgrade -r requirements.txt    
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf    
EXPOSE 8080    
ENV POSTGRES_USER="djgoDBmain_owner"
ENV POSTGRES_PASSWORD="0YvOjC7yEeHi"
ENV POSTGRES_DB="djgoDBmain"
ENV POSTGRES_HOST="ep-lingering-term-a5gpgv2e.us-east-2.aws.neon.tech"
ENV POSTGRES_PORT="5432"
# POSTGRES_DB_URL="postgresql+asyncpg://djgoDBmain_owner:0YvOjC7yEeHi@ep-lingering-term-a5gpgv2e.us-east-2.aws.neon.tech/djgoDBmain"


ENV PROCESSES=1
ENV WORKERS=1
ENV FAST_MODE="false"
    # ENTRYPOINT ["python3", "-m", "svc"]
CMD ["python3", "-m", "svc", "--log-level=INFO"]    


# FROM python:3.11-bookworm
# RUN apt-get update && apt-get install -y supervisor
# WORKDIR /workspace    
# ENV PYTHONPATH="${PYTHONPATH}:/workspace/svc"    
# COPY . .    
# RUN pip install --no-cache-dir --upgrade -r requirements.txt    
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf    
# EXPOSE 8080    
#     # ENTRYPOINT ["python3", "-m", "svc"]
#     # CMD ["python3", "-m", "svc", "--log-level=info"]    
# ENV PROCESSES=1
# ENV WORKERS=1
# ENV FAST_MODE="false"
# ENTRYPOINT ["sh", "-c", "python3 -m svc --processes $PROCESSES --workers $WORKERS $( [ \"$FAST_MODE\" = \"true\" ] && echo \"--fast\" ) --log-level $LOG_LEVEL"]







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
