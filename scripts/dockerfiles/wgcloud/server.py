#!/usr/bin/env python3
"""WGCloud FastAPI wrapper — exposes the Java monitoring platform as a REST API."""

import os
import subprocess
import sys
from fastapi import FastAPI

app = FastAPI(
    title='WGCloud',
    version='1.0.0',
    description='WGCloud — Distributed monitoring system with Spring Boot (tianshiyeben/wgcloud)'
)


@app.get('/health')
async def health():
    # Check if the Spring Boot JAR is running by probing the upstream health endpoint
    import urllib.request
    port = os.environ.get('WGCLOUD_PORT', '9999')
    try:
        # WGCloud doesn't have a dedicated health endpoint, but hitting the context path
        # with a short timeout confirms the server is up
        req = urllib.request.Request(
            f'http://localhost:{port}/wgcloud',
            method='HEAD'
        )
        urllib.request.urlopen(req, timeout=5)
        return {'status': 'ok', 'framework': 'WGCloud', 'upstream': 'tianshiyeben/wgcloud'}
    except Exception:
        return {'status': 'starting', 'framework': 'WGCloud', 'note': 'Spring Boot may still be initializing'}


@app.get('/info')
async def info():
    return {
        'name': 'WGCloud',
        'description': 'Distributed monitoring system — CPU, memory, disk, GPU, Docker, network, service API monitoring with web SSH',
        'port': int(os.environ.get('WGCLOUD_PORT', '9999')),
        'context_path': '/wgcloud',
        'upstream': 'https://github.com/tianshiyeben/wgcloud',
        'stars': '5.1k+'
    }


def load_mysql_schema():
    """Load the WGCloud SQL schema into MySQL on first start."""
    port = os.environ.get('WGCLOUD_PORT', '9999')
    mysql_host = os.environ.get('MYSQL_HOST', 'mysql')
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', 'changeme')
    mysql_database = os.environ.get('MYSQL_DATABASE', 'wgcloud')
    sql_file = '/app/wgcloud.sql'

    if not os.path.isfile(sql_file):
        print(f"WARN: SQL schema not found at {sql_file} — skipping database init")
        return

    print(f"Loading WGCloud SQL schema into {mysql_host}/{mysql_database}...")
    try:
        result = subprocess.run(
            ['mysql', '-h', mysql_host, '-u', mysql_user,
             f'-p{mysql_password}', mysql_database],
            input=open(sql_file, 'rb').read(),
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0:
            print("Schema loaded successfully.")
        else:
            # Schema may already exist — this is fine
            stderr_text = result.stderr.decode('utf-8', errors='replace')
            if 'already exists' in stderr_text.lower():
                print("Schema already initialized — continuing.")
            else:
                print(f"NOTE: Schema load returned {result.returncode}: {stderr_text[:200]}")
    except FileNotFoundError:
        print("WARN: mysql client not available — schema must be loaded externally")
    except Exception as e:
        print(f"WARN: Schema load failed: {e} — the database may need manual setup")


if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('WGCLOUD_PORT', '9999'))

    # Load schema on first start
    load_mysql_schema()

    # Build Spring Boot args — override datasource from environment
    mysql_host = os.environ.get('MYSQL_HOST', 'mysql')
    mysql_user = os.environ.get('MYSQL_USER', 'root')
    mysql_password = os.environ.get('MYSQL_PASSWORD', 'changeme')
    mysql_database = os.environ.get('MYSQL_DATABASE', 'wgcloud')

    java_args = [
        'java', '-jar', '/app/wgcloud-server-release.jar',
        f'--server.port={port}',
        f'--spring.datasource.url=jdbc:mysql://{mysql_host}:3306/{mysql_database}?characterEncoding=utf-8&useSSL=false&allowMultiQueries=true',
        f'--spring.datasource.username={mysql_user}',
        f'--spring.datasource.password={mysql_password}',
    ]

    # Start WGCloud JAR in background
    subprocess.Popen(
        java_args,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    uvicorn.run(app, host='0.0.0.0', port=port)
