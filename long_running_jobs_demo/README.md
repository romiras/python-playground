# Long-Running Jobs Demo

This project demonstrates how to handle long-running web requests efficiently in a FastAPI application.

By leveraging FastAPI's `BackgroundTasks`, "heavy" processing logic is offloaded to the background, ensuring that user requests remain non-blocking and responsive. Job execution is tracked using a database-backed `SearchJob` model, which persists the status and results of each task.

## API

### Search Initiation
`POST /api/v1/search`

Initiates a new background search task.

**Request Body (form-data):**
- `q`: The search query string.

**Response (201 Created):**
```json
{
  "job_id": "uuid-string"
}
```

### Job Status Polling
`GET /api/v1/search_results_polling`

Retrieves the current status and results of a previously initiated search job.

**Query Parameters:**
- `job_id`: The unique identifier returned by the search initiation endpoint.

**Response:**
```json
{
  "status": "pending | processing | completed | failed",
  "reason": "Error message if failed",
  "data": { ... } // Result data if completed
}
```

## Roadmap / TODO

- [ ] Implement Server-Sent Events (SSE) instead of short-polling for real-time updates.
