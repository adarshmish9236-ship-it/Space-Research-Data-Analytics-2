-- =============================================================================
-- ORBITALYTICS Phase 6 — Hive Data Warehouse Setup
-- Script: 01_create_database.sql
-- Database: orbitalytics
-- =============================================================================

CREATE DATABASE IF NOT EXISTS orbitalytics
COMMENT 'Orbitalytics Space Research Big Data Analytics & Forecasting Warehouse'
LOCATION '/user/hive/warehouse/orbitalytics.db';

USE orbitalytics;

