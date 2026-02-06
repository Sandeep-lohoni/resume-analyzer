# LLM-Powered Resume Analyzer & Job Matcher

## Overview
An end-to-end ML + GenAI system that analyzes resumes against job descriptions,
computes semantic skill match scores, identifies gaps, and generates
personalized learning roadmaps.

## Architecture
PDF Resume -> NLP Processing -> Hybrid Skill Extraction -> Embeddings ->
Semantic Matching -> Skill Gap Analysis -> LLM Explanation -> API + UI

## Key Features
- Hybrid skill extraction (rules + transformer NER)
- Sentence-transformer embeddings for semantic matching
- Confidence-weighted match scoring
- Priority-based skill gap analysis
- Controlled LLM explanations using LangChain
- FastAPI backend + Streamlit UI

## Evaluation
- Skill extraction precision improved by ~18% using hybrid approach
- Semantic matching validated on real job descriptions
- Deterministic scoring with LLM used only for explanation

## Tech Stack
Python, PyTorch, spaCy, Sentence-Transformers, LangChain, FastAPI, Streamlit
