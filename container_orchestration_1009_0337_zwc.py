# 代码生成时间: 2025-10-09 03:37:27
#!/usr/bin/env python

"""Container Orchestration using Bottle framework."""

from bottle import Bottle, request, response, run
import subprocess
import os
import json

# Initialize the Bottle application
app = Bottle()

# Define the base path for Docker commands
DOCKER_CMD = 'docker'

# Define routes for container operations
@app.route('/containers', method='GET')
def list_containers():
    """List all containers."""
    try:
        # Execute Docker command to list containers
        result = subprocess.run([DOCKER_CMD, 'ps', '--format', "{{json .}}"],
                              capture_output=True, text=True, check=True)
        # Parse the output as JSON
        containers = [json.loads(line) for line in result.stdout.strip().split('
') if line]
        return json.dumps(containers)
    except subprocess.CalledProcessError as e:
        # Handle errors in Docker command execution
        return json.dumps({'error': 'Failed to list containers'}), 500

@app.route('/containers/<container_id>', method='GET')
def get_container(container_id):
    """Get details of a specific container."""
    try:
        # Execute Docker command to inspect a container
        result = subprocess.run([DOCKER_CMD, 'inspect', container_id],
                              capture_output=True, text=True, check=True)
        # Parse the output as JSON
        container_details = json.loads(result.stdout)[0]
        return json.dumps(container_details)
    except subprocess.CalledProcessError as e:
        # Handle errors in Docker command execution
        return json.dumps({'error': f'Failed to inspect container {container_id}'}), 500

@app.route('/containers', method='POST')
def create_container():
    """Create a new container."""
    try:
        # Get the image and name from the request data
        data = request.json
        image = data.get('image')
        name = data.get('name')
        if not image or not name:
            return json.dumps({'error': 'Image and name are required'}), 400
        # Execute Docker command to create a container
        result = subprocess.run([DOCKER_CMD, 'create', '--name', name, image],
                              capture_output=True, text=True, check=True)
        # Return the new container ID
        container_id = result.stdout.strip()
        return json.dumps({'container_id': container_id}), 201
    except subprocess.CalledProcessError as e:
        # Handle errors in Docker command execution
        return json.dumps({'error': 'Failed to create container'}), 500

@app.route('/containers/<container_id>:start', method='PUT')
def start_container(container_id):
    """Start a specific container."""
    try:
        # Execute Docker command to start the container
        subprocess.run([DOCKER_CMD, 'start', container_id], check=True)
        return json.dumps({'message': f'Container {container_id} started'}), 200
    except subprocess.CalledProcessError as e:
        # Handle errors in Docker command execution
        return json.dumps({'error': f'Failed to start container {container_id}'}), 500

@app.route('/containers/<container_id>:stop', method='PUT')
def stop_container(container_id):
    """Stop a specific container."""
    try:
        # Execute Docker command to stop the container
        subprocess.run([DOCKER_CMD, 'stop', container_id], check=True)
        return json.dumps({'message': f'Container {container_id} stopped'}), 200
    except subprocess.CalledProcessError as e:
        # Handle errors in Docker command execution
        return json.dumps({'error': f'Failed to stop container {container_id}'}), 500

# Start the Bottle server
if __name__ == '__main__':
    run(app, host='localhost', port=8080)