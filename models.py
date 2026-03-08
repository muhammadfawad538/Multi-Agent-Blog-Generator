from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class ResearchOutput(BaseModel):
    """Structured output from the Research Agent"""
    topic: str
    key_points: List[str]
    facts: List[str]
    references: List[str]

class OutlineOutput(BaseModel):
    """Structured output from the Outline Agent"""
    blog_title: str
    sections: List[str]

class WriterOutput(BaseModel):
    """Structured output from the Writer Agent"""
    title: str
    section_contents: Dict[str, str]

class SEOOutput(BaseModel):
    """Structured output from the SEO Agent"""
    seo_title: str
    meta_description: str
    keywords: List[str]

class EditorOutput(BaseModel):
    """Structured output from the Editor Agent"""
    final_blog: str
    readability_score: float
    improvements_made: List[str]

class FinalBlogOutput(BaseModel):
    """Final output format"""
    title: str
    blog: str
    seo: Dict[str, Any]  # Allow flexible types for SEO data