# ADK UniqueViolation Error - Minimal Reproducible Example (Dockerized)

This directory contains a minimal, Dockerized setup to reproduce the `sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation)` error observed when using the Google ADK with streaming enabled, `DatabaseSessionService`, and an LLM response containing both text and a function call.

It uses Docker Compose to run the PostgreSQL database and the FastAPI application (with the minimal agent and local ADK source).

## Prerequisites

1.  **Docker & Docker Compose:** Ensure you have Docker Desktop or Docker Engine with Docker Compose installed and running.
2.  **Google Cloud Authentication:** Make sure your local environment is authenticated to use Google Cloud services (for the Gemini model). Run:
    ```bash
    gcloud auth application-default login
    ```
    The Docker container will inherit these credentials.

## Running the Example

1.  **Navigate to Directory:**
    *   Open your terminal in this directory:
        ```bash
        cd adk-streaming-tools-unique-violation-events-repro
        ```
    *   **Set GCP Project/Location:** Edit the `.env` file and set your `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`.


2.  **Build and Start Services:**
    *   Run Docker Compose. This will build the `app` image (including the local ADK source) and start both the `db` (PostgreSQL) and `app` (FastAPI) services.
        ```bash
        docker compose up --build
        ```
    *   Wait for the logs to show that both services are running and healthy. The `app` service log should indicate it's running on `http://0.0.0.0:8001`.

3.  **Access the ADK Web UI:**
    *   Open your web browser and navigate to:
        [http://localhost:8001/dev-ui](http://localhost:8001/dev-ui)
    *   This is the built-in web UI provided by the ADK framework.

4.  **Trigger the Error:**
    *   In the ADK Web UI:
        *   Select the `minimal_agent` app from the "Select app" dropdown.
        *   Click "Create new chat". Give it any name (e.g., "Test") and click "Submit".
        *   In the sidebar, find the "**Enable Streaming**" toggle and make sure it is **ON**.
        *   In the chat input at the bottom, type the following prompt and press Enter:
            ```
            Run the simple tool
            ```

5.  **Observe Server Logs:**
    *   Watch the terminal where `docker compose up` is running (or open a new terminal in the same directory and run `docker compose logs -f app`).
    *   When the agent responds, you should observe logs from the `app` service showing:
        *   The agent processing the request.
        *   The text part ("Okay, I will run the simple tool now.") being generated/saved.
        *   The function call (`simple_tool`) being generated/saved.
        *   **The `sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint "events_pkey"` traceback.**
        *   The stream in the UI might hang or show an error after this point.

6.  **Confirm Without Streaming:**
    *   Go back to the ADK Web UI.
    *   Turn the "**Enable Streaming**" toggle **OFF** in the sidebar.
    *   Send the same prompt ("Run the simple tool") again in the chat input.
    *   Observe the server logs (`docker compose logs -f app`). The interaction should complete successfully without the `UniqueViolation` error. The UI should display the full response (text and tool call/result).

## Cleaning Up

*   When you are finished, stop and remove the containers, network, and volume defined in the `docker-compose.yml` file. In the terminal where you ran `docker compose up`, press `Ctrl+C`. Then run:
    ```bash
    docker compose down -v
    ```
    The `-v` flag removes the named volume (`postgres_data`), deleting the database data. Omit `-v` if you want to keep the data for the next run.

This Dockerized setup provides a consistent environment to demonstrate the issue, making it easier for others to reproduce and investigate.
