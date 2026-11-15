"""
Orbitalytics 2.0 - Enterprise Application Configuration
Space Research Data Analytics: A Hadoop Ecosystem Approach to Demand Forecasting
"""
from pathlib import Path
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

class Settings(BaseSettings):
    PROJECT_NAME: str = "ORBITALYTICS 2.0"
    PROJECT_VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    DESCRIPTION: str = (
        "An Intelligent Space Research Data Platform for Distributed Analytics, "
        "Predictive Demand Intelligence, and Strategic Resource Optimization."
    )
    
    # Core Data Lakehouse Storage Paths (Medallion Architecture)
    PROJECT_ROOT: Path = PROJECT_ROOT
    BACKEND_DIR: Path = BACKEND_DIR
    DATASETS_DIR: Path = PROJECT_ROOT / "datasets"
    RAW_DATA_DIR: Path = PROJECT_ROOT / "datasets" / "raw"
    BRONZE_DATA_DIR: Path = PROJECT_ROOT / "datasets" / "bronze"
    SILVER_DATA_DIR: Path = PROJECT_ROOT / "datasets" / "silver"
    GOLD_DATA_DIR: Path = PROJECT_ROOT / "datasets" / "gold"
    PROCESSED_DATA_DIR: Path = PROJECT_ROOT / "datasets" / "processed"
    CURATED_DATA_DIR: Path = PROJECT_ROOT / "datasets" / "curated"
    METADATA_DIR: Path = PROJECT_ROOT / "datasets" / "metadata"
    QUALITY_REPORTS_DIR: Path = PROJECT_ROOT / "datasets" / "quality_reports"

    # Hadoop Ecosystem HDFS Storage Zones
    HDFS_SPACE_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research"
    HDFS_BRONZE_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "bronze"
    HDFS_SILVER_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "silver"
    HDFS_GOLD_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "gold"
    HDFS_ANALYTICS_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "analytics"
    HDFS_FORECASTS_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "forecasts"
    HDFS_OPTIMIZATION_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "optimization"
    HDFS_REPORTS_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hdfs" / "space_research" / "reports"

    # Big Data Workspaces
    HIVE_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "hive"
    MAPREDUCE_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "mapreduce"
    SPARK_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "spark"
    YARN_DIR: Path = PROJECT_ROOT / "hadoop_ecosystem" / "yarn"
    
    # ML & Optimization
    MODELS_DIR: Path = PROJECT_ROOT / "models"
    OPTIMIZATION_DIR: Path = PROJECT_ROOT / "optimization"
    REPORTS_DIR: Path = PROJECT_ROOT / "reports" / "generated"
    LOGS_DIR: Path = PROJECT_ROOT / "logs"
    DATABASE_PATH: Path = PROJECT_ROOT / "logs" / "lakehouse_metadata.db"

    # Hadoop Cluster Connection Settings
    HADOOP_NAMENODE_URL: str = "hdfs://localhost:9000"
    HIVE_SERVER2_HOST: str = "localhost"
    HIVE_SERVER2_PORT: int = 10000
    HIVE_DATABASE: str = "space_research_warehouse"
    YARN_RESOURCE_MANAGER_URL: str = "http://localhost:8088"
    SPARK_MASTER: str = "local[*]"
    HDFS_BLOCK_SIZE_MB: int = 128
    HDFS_REPLICATION_FACTOR: int = 3
    DEFAULT_STORAGE_MODE: str = "HYBRID_LOCAL_EMULATION"  # Truthful mode indicator

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "*"
    ]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure all medallion and lakehouse directories exist
for path in [
    settings.RAW_DATA_DIR,
    settings.BRONZE_DATA_DIR,
    settings.SILVER_DATA_DIR,
    settings.GOLD_DATA_DIR,
    settings.PROCESSED_DATA_DIR,
    settings.CURATED_DATA_DIR,
    settings.METADATA_DIR,
    settings.QUALITY_REPORTS_DIR,
    settings.HDFS_BRONZE_DIR,
    settings.HDFS_SILVER_DIR,
    settings.HDFS_GOLD_DIR,
    settings.HDFS_ANALYTICS_DIR,
    settings.HDFS_FORECASTS_DIR,
    settings.HDFS_OPTIMIZATION_DIR,
    settings.HDFS_REPORTS_DIR,
    settings.HIVE_DIR,
    settings.MAPREDUCE_DIR,
    settings.SPARK_DIR,
    settings.YARN_DIR,
    settings.MODELS_DIR / "trained",
    settings.MODELS_DIR / "evaluation",
    settings.MODELS_DIR / "metadata",
    settings.OPTIMIZATION_DIR / "results",
    settings.OPTIMIZATION_DIR / "scenarios",
    settings.REPORTS_DIR,
    settings.LOGS_DIR
]:
    path.mkdir(parents=True, exist_ok=True)
