-- Initialize pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create schema for application
CREATE SCHEMA IF NOT EXISTS studium;

-- Set search path
SET search_path TO studium, public;
