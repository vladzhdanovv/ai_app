# AI Driven Interview System

The AI Driven Interview System is an application designed to streamline and enhance the interview process using artificial intelligence. This system leverages modern web technologies and AI capabilities to provide a seamless and efficient interview experience.

## Environment Configuration

The application requires certain environment variables to be set for proper operation. These are defined in the `.env` file:

- `REDIS_ENDPOINT`: The endpoint for the Redis server (e.g., `redis`).
- `REDIS_PORT`: The port for the Redis server (e.g., `6379`).
- `OPENAI_API_KEY`: The API key for accessing OpenAI services.
- `AWS_REGION`: The region for your AWS services (e.g., `eu-north-1`).
- `AWS_ACCESS_KEY_ID`: Your access key ID for AWS.
- `AWS_SECRET_ACCESS_KEY`: Your secret access key for AWS.
- `AWS_BUCKET`: The name of your AWS S3 bucket.
- `AWS_TABLE`: The name of your AWS DynamoDB table.

## Deployment

The project includes Docker support for containerized deployment, ensuring easy setup and scalability across different environments.
```sh
docker compose up
```
## API Usage

The API provides endpoints to manage the interview process:

- **Start Interview**: Initiates a new interview session.
  - **Endpoint**: `POST /api/v1/interviews/start`
  - **Request Body**: `InterviewStartEvent` containing the job title.
  - **Response**: Returns a `candidate_id` and a list of questions.

- **Submit Interview**: Submits responses and receives feedback.
  - **Endpoint**: `POST /api/v1/interviews/{candidate_id}/submit`
  - **Request Body**: `InterviewSubmitEvent` containing the responses.
  - **Response**: Returns questions, responses, scores, and feedback.

more complete documentation is available at http://localhost:8000/docs