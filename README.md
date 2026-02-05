# LLM-Powered Resume Analyzer & Job Matcher

## Problem Statement
Recruiters manually screen resumes against job descriptions, which is time-consuming and subjective.
This project automates resume analysis using NLP, embeddings, and LLMs to compute skill match scores, identify gaps, and recommend personalized learning paths.

## Features
- Resume PDF parsing
- Skill extraction using NLP
- Semantic skill matching
- Skill gap analysis
- LLM-based explanations (LangChain)

## Tech Stack
- Python, PyTorch
- spaCy, sentence-transformers
- LangChain
- FastAPI, Streamlit

## Architecture
Resume + Job Description → NLP Processing → Embeddings → Matching → LLM Explanation
