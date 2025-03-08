# Image Share API

A lightweight, fast image sharing API service with Docker support. This API provides endpoints to upload, retrieve, and delete images with API key authentication.

## Features

- Simple HTTP API for image management
- API key authentication for secure uploads and deletions
- Docker containerized for easy deployment
- Environment variable configuration
- Supports all image formats

## API Endpoints

- `GET /`: API information
- `PUT /images`: Upload an image (requires API key)
- `GET /images/{filename}`: Retrieve an image
- `DELETE /images/{filename}`: Delete an image (requires API key)

## Environment Variables

- `API_KEY`: Required. Authentication key for upload and delete operations
- `BASE_URL`: Optional. Base URL for returned image links (defaults to http://localhost)

## Docker Setup

### Build the Docker Image

```bash
docker build -t image-share-api .
```

### Run the Container

```bash
docker run -d \
  -p 80:80 \
  -e API_KEY="your-secret-api-key" \
  -e BASE_URL="https://your-domain.com" \
  -v image-data:/app/uploads \
  --name image-share \
  image-share-api
```

## GitHub Actions CI/CD

This repository includes a GitHub Actions workflow that automatically builds and pushes the Docker image to Docker Hub whenever changes are pushed to the main branch.

### Setup Instructions

1. Fork or push this repository to GitHub
2. Add the following secrets in your GitHub repository settings:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token (create one at https://hub.docker.com/settings/security)
3. Push to the main branch, and GitHub Actions will automatically build and push the image to: 
   `yourusername/image-api-share:latest`

The workflow file is located at `.github/workflows/docker-build-push.yml`

## API Usage Examples

### Upload an Image

```bash
curl -X PUT \
  http://localhost/images \
  -H "api-key: your-secret-api-key" \
  -F "file=@/path/to/your/image.jpg"
```

### Get an Image

```bash
curl -X GET http://localhost/images/filename.jpg
```

### Delete an Image

```bash
curl -X DELETE \
  http://localhost/images/filename.jpg \
  -H "api-key: your-secret-api-key"
```

## Security Notes

- Always use a strong, randomly generated API key
- When deployed, use HTTPS through a reverse proxy

