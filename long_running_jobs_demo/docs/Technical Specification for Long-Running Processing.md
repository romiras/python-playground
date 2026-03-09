# Technical Specification for Long-Running Processing

This technical specification outlines a resilient, asynchronous pattern for handling long-running web requests (5–10 minutes) using a decoupled architecture.

---

## 1. System Components

* **Producer (API):** Handles client connections, persists initial state, and streams updates.
* **Queue (Broker):** Decouples the API from the heavy processing logic.
* **Consumer (Worker):** Executes the long-running query and updates the state.
* **State Store:** Shared storage (Database/Cache) to track job status and results.

---

## 2. API Endpoints

### **POST** `/api/v1/search`

**Goal:** Initialize a job.

* **Request Body:** `{ "query": string }`
* **Processing:**
1. Generate a unique `job_id`.
2. Create a record in State Store: `{ "id": job_id, "status": "pending", "created_at": timestamp }`.
3. Push message to MQ: `{ "job_id": job_id, "query": "..." }`.


* **Response:**
* **Status:** `201 Created`
* **Body:** `{ "job_id": string }`



### **GET** `/api/v1/search_results?job_id=:id`

**Goal:** Establish a long-lived connection for real-time updates.

* **Protocol:** Server-Sent Events (SSE).
* **Response Headers:**
* `Content-Type: text/event-stream`
* `Cache-Control: no-cache`
* `Connection: keep-alive`


* **Processing Algorithm:** (See Section 4).

---

## 3. Data Structures

### Job Status Schema

| Field | Type | Description |
| --- | --- | --- |
| `job_id` | UUID/String | Primary identifier. |
| `status` | Enum | `pending`, `processing`, `completed`, `failed`. |
| `data` | Object | Result payload (null if not completed). |
| `reason` | String | Error message if status is `failed`. |
| `updated_at` | Timestamp | For TTL and cleanup logic. |

### SSE Event Format

* **Heartbeat:** `: heartbeat\n\n` (Sent to prevent connection timeouts).
* **Message:** `data: {"status": string, "data": object|null, "reason": string|null}\n\n`.

---

## 4. Processing Algorithms

### A. The SSE Connection Loop (API)

Upon receiving a GET request for a `job_id`:

1. **Immediate Check:** Query State Store. If status is `completed` or `failed`, send one final event and close.
2. **Subscription:** Subscribe to a notification channel (Pub/Sub) keyed by `job_id`.
3. **Concurrency Loop:**
* **On Notification:** If a "Job Updated" message arrives, fetch the latest state from the Store, send it to the client. If status is terminal (`completed`/`failed`), **Close Connection**.
* **On Heartbeat Ticker:** Every 20 seconds, send a heartbeat comment to the client.
* **On Client Disconnect:** Stop the loop and unsubscribe to free resources.
* **On Global Timeout:** If loop duration > 10 minutes, send a `failed` event (reason: "Timeout") and close.



### B. The Worker Logic (Consumer)

1. **Consume:** Pull job from MQ.
2. **Update State:** Set status to `processing` in State Store. Notify Pub/Sub.
3. **Execution with Guardrail:**
* Wrap the internal service query in a **10-minute timeout** wrapper.
* **If Success:** Write results to `data` field, set status to `completed`.
* **If Timeout/Error:** Set status to `failed`, write error to `reason`.


4. **Finalize:** Update State Store and publish a "Job Updated" message to the notification channel.

---

## 5. Constraints & Resilience

* **Connection Retention:** The API must send a heartbeat at an interval strictly less than the hosting environment's idle timeout (e.g., 20s for Heroku's 30s limit).
* **Terminal States:** Once a job reaches `completed` or `failed`, the API must close the SSE stream to prevent unnecessary open sockets.
* **Client Reconnection:** The frontend must be designed to reconnect if the stream breaks. The backend must handle a "re-attach" by checking the State Store immediately upon connection.
* **Cleanup (TTL):** Job records should have a Time-To-Live in the State Store (e.g., 24 hours) to prevent database bloating.
