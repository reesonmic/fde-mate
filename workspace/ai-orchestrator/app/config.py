"""
AI Orchestrator configuration.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "fde-ai-orchestrator"
    host: str = "0.0.0.0"
    port: int = 8090

    # LLM Configuration
    llm_provider: str = "dashscope"  # dashscope | openai | mock
    dashscope_api_key: str = ""
    dashscope_model: str = "qwen-plus"
    dashscope_embedding_model: str = "text-embedding-v2"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # RAG Configuration
    milvus_host: str = "localhost"
    milvus_port: int = 19530
    es_host: str = "http://localhost:9200"

    # API service (for tool calls back to business API)
    api_base_url: str = "http://localhost:8080/api/v1"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
