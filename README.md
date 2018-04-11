# FileRESTAPI
small REST API for large files


## How to start?
1. Install docker(version 18.03.0-ce)
2. Run: "docker build -t filerestapi ."
3. Run: "docker run -p 80:80 filerestapi"
3. Run the tests: "docker exec -it CONTAINER_ID /opt/filerestapi/tests/run.sh"
