# Image Share API

---

## ☕ Buy Me a Coffee (or a Beer!)

If you like this project and want to support my caffeine-fueled coding sessions, you can buy me a coffee (or a beer, I won't judge! 🍻) on Ko-fi:

[![Support me on Ko-fi](img/support_me_on_kofi_badge_red.png)](https://ko-fi.com/vladoportos)

Every donation helps to prove to my wife that I'm not a complete idiot :D

---

A lightweight, fast image sharing API service with Docker support. This API provides endpoints to upload, retrieve, and delete images with API key authentication.

## Features

- Simple HTTP API for image management
- API key authentication for secure uploads and deletions
- Docker containerized for easy deployment
- Environment variable configuration
- Supports all image formats
- N8N compatible for automation workflows
- Returns original filenames for easy image identification
- Bulk deletion via wipe-all endpoint

## Pre-built Docker Image

You can find a pre-built Docker image ready to use at:

```
vladoportos/image-api-share
```

To pull and run the pre-built image:

```bash
docker pull vladoportos/image-api-share
docker run -d \
  -p 80:80 \
  -e API_KEY="your-secret-api-key" \
  -e BASE_URL="https://your-domain.com" \
  -v image-data:/app/uploads \
  --name image-share \
  vladoportos/image-api-share
```

## API Endpoints

- `GET /`: API information
- `PUT /images`: Upload an image (requires API key)
- `GET /images/{filename}`: Retrieve an image
- `DELETE /images/{filename}`: Delete an image (requires API key)
- `DELETE /wipe-all`: Delete all images (requires API key)

## API Response Format

When uploading an image, the API returns a JSON response with:

```json
{
  "image_id": "unique-uuid-for-the-image",
  "download_url": "http://your-server/images/filename.jpg",
  "original_filename": "your-original-filename.jpg"
}
```

The `original_filename` field contains the original filename of the uploaded image, making it easier to identify images in your automation workflows.

## Environment Variables

- `API_KEY`: Required. Authentication key for upload and delete operations
- `BASE_URL`: Optional. Base URL for returned image links (defaults to http://localhost)

## Using with N8N

To upload images from N8N to this API:

1. Use an **HTTP Request** node with the following settings:
   - Method: `PUT`
   - URL: `http://your-server/images`
   - Headers:
     - `api-key`: Your API key
     - `x-filename`: (Optional) Set this to pass your original filename
   - Binary Data: Enabled
   - When using binary data from previous nodes:
     - Use "Send Binary Data" option
     - Set "Property Name" to match your binary data field (usually "data")

2. **Important**: The API now supports both:
   - Traditional multipart/form-data uploads (using `file` parameter)
   - Direct binary data uploads (send the binary data directly in the request body)

3. The response will include the original filename, which you can use in subsequent nodes:
   ```json
   {
     "image_id": "3f7c53e4-96bc-4d0f-b7c2-351a5def54e8",
     "download_url": "http://your-server/images/3f7c53e4-96bc-4d0f-b7c2-351a5def54e8.jpg",
     "original_filename": "vacation-photo.jpg"
   }
   ```

4. Sample N8N workflow for binary data:
   ```json
   {
     "nodes": [
       {
         "name": "HTTP Request",
         "type": "n8n-nodes-base.httpRequest",
         "parameters": {
           "method": "PUT",
           "url": "http://your-server/images",
           "authentication": "headerAuth",
           "headerParameters": {
             "parameters": [
               {
                 "name": "api-key",
                 "value": "your-secret-api-key"
               },
               {
                 "name": "x-filename",
                 "value": "={{ $json.filename }}"
               }
             ]
           },
           "sendBinaryData": true,
           "binaryPropertyName": "data",
           "options": {}
         }
       }
     ]
   }
   ```

## Docker Setup

### Build the Docker Image

```bash
docker build -t image-api-share .
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

Response:
```json
{
  "image_id": "3f7c53e4-96bc-4d0f-b7c2-351a5def54e8",
  "download_url": "http://localhost/images/3f7c53e4-96bc-4d0f-b7c2-351a5def54e8.jpg",
  "original_filename": "your-image.jpg"
}
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

### Wipe All Images

```bash
curl -X DELETE \
  http://localhost/wipe-all \
  -H "api-key: your-secret-api-key"
```

Response:
```json
{
  "message": "All images wiped successfully",
  "deleted_count": 42
}
```

## Security Notes

- Always use a strong, randomly generated API key
- When deployed, use HTTPS through a reverse proxy
