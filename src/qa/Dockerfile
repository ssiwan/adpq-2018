############################################################
# Dockerfile 
# This should be the easiest most bare bone way to run 
# python unittest automation scripts.
############################################################

# The base image to use to start the build process.
# Use an official Python runtime as a parent image
FROM python:3.6

# Usage: MAINTAINER [name]
MAINTAINER Luis F. Escobar-Driver

# The WORKDIR directive is used to set where the 
# command defined with CMD is to be executed.
# Set the working directory to /runner
WORKDIR /runner

# The ADD command gets two arguments: a source and a destination.
# It basically copies the files from the source on the host into 
# the container's own filesystem at the set destination.
# Copy the current directory contents into the container at /runner
ADD . /runner

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# The EXPOSE command is used to associate a specified port to enable 
# networking between the running process inside the container and the 
# outside world
# Make port 80 available to the world outside this container
# EXPOSE 80
# Not needed for bare bones set up

# Usage: ENV key value
# Define environment variable
#ENV NAME World 
# Not needed for bare bones set up

# Set proxy server, replace host:port with values for your servers
#ENV http_proxy host:port
#ENV https_proxy host:port
# Not needed for bare bones set up

# Run runner.py when the container launches
CMD ["python", "runner.py"]
# Bare bones  