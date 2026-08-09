# AI Knowledge Workspace

A production-ready AI knowledge assistant for uploading documents, indexing them, and chatting with the content through retrieval-augmented generation (RAG).

## Overview

This project combines a FastAPI backend, a React frontend, and supporting infrastructure to provide a secure, containerized knowledge workspace. Users can upload documents, store them in a searchable knowledge base, and ask questions grounded in the source material.

## Architecture

The system is organized into four main layers:

- Client layer: a React-based user interface for authentication, uploads, and chat
- Application layer: a FastAPI service that handles auth, document processing, indexing, retrieval, and chat orchestration
- Data layer: PostgreSQL for structured metadata and Qdrant for vector search
- AI layer: Azure OpenAI for embeddings and response generation

A visual overview is available in [docs/architecture-diagram.svg](docs/architecture-diagram.svg).

## Tech Stack

- FastAPI
- React
- PostgreSQL
- Qdrant
- Docker / Docker Compose
- Azure OpenAI
- Terraform (for infrastructure provisioning)

## Features

- User authentication and authorization
- Document upload and ingestion
- Vector-based retrieval with RAG
- Chat history and conversational responses
- Source citations for grounded answers
- Containerized local development workflow

## Project Structure

- backend/: FastAPI application and API services
- frontend/: React client application
- docs/: architecture diagrams and documentation
- infrastructure/: Terraform modules and environment configuration
- docker-compose.yml: local container orchestration

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Node.js 18+

### Run locally

```bash
docker compose up --build
```

The backend API will be available at http://localhost:8000.

## Development Notes

- The backend is scaffolded with FastAPI and is ready for extension with document processing, embedding generation, and retrieval pipelines.
- The infrastructure folder includes Terraform configuration for provisioning supporting services.
- The frontend folder is currently a placeholder and can be expanded with the UI experience.

## Status

This repository is in an early-stage scaffold and is intended as a foundation for building a full AI knowledge workspace.