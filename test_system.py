"""
Simple test to verify the AI Blog Generation Pipeline system
"""
from models import ResearchOutput, OutlineOutput, WriterOutput, SEOOutput, EditorOutput, FinalBlogOutput

# Test that the models are properly defined
def test_models():
    print("Testing Pydantic models...")

    # Test ResearchOutput
    research = ResearchOutput(
        topic="Test Topic",
        key_points=["Point 1", "Point 2"],
        facts=["Fact 1", "Fact 2"],
        references=["Ref 1", "Ref 2"]
    )
    print(f"OK ResearchOutput: {research.topic}")

    # Test OutlineOutput
    outline = OutlineOutput(
        blog_title="Test Blog",
        sections=["Intro", "Body", "Conclusion"]
    )
    print(f"OK OutlineOutput: {outline.blog_title}")

    # Test WriterOutput
    writer = WriterOutput(
        title="Test Title",
        section_contents={"Intro": "Content here", "Body": "More content"}
    )
    print(f"OK WriterOutput: {writer.title}")

    # Test SEOOutput
    seo = SEOOutput(
        seo_title="SEO Title",
        meta_description="Description here",
        keywords=["keyword1", "keyword2"]
    )
    print(f"OK SEOOutput: {seo.seo_title}")

    # Test EditorOutput
    editor = EditorOutput(
        final_blog="Full blog content",
        readability_score=8.5,
        improvements_made=["Fixed grammar", "Improved flow"]
    )
    print(f"OK EditorOutput: Readability {editor.readability_score}")

    # Test FinalBlogOutput
    final = FinalBlogOutput(
        title="Final Title",
        blog="Final blog content",
        seo={
            'meta_description': 'Meta desc',
            'keywords': ['kw1', 'kw2']
        }
    )
    print(f"OK FinalBlogOutput: {final.title}")

    print("\nAll models tested successfully!")

if __name__ == "__main__":
    test_models()