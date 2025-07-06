import json
from typing import Optional
from dotenv import LOG, LOG_JSON
from dataclasses import asdict, dataclass

@dataclass
class AIGeneratedMetadata:
    """AI Generated metadata class for image analysis"""
    title: str
    description: str
    subject: str
    keywords: str
    filename: str
    category: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None

@dataclass
class ImageMetadata:
    """
    Image metadata class with auto-completion support
    Similar to TypeScript interface for better IDE suggestions
    """
    # Required fields
    title: str
    description: str  
    subject: str
    keywords: str
    filename: str
    
    # Optional fields with default None
    author: Optional[str] = None
    copyright: Optional[str] = None
    rating: Optional[int] = None
    location: Optional[str] = None
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    category: Optional[str] = None
    mood: Optional[str] = None
    style: Optional[str] = None
    
    def __post_init__(self):
        """Validate data after initialization"""
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if not self.keywords.strip():
            raise ValueError("Keywords cannot be empty")
        if self.rating is not None and not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
    
    def to_dict(self) -> dict:
        """Convert to dictionary for backward compatibility"""
        return {
            'title': self.title,
            'description': self.description,
            'subject': self.subject,
            'keywords': self.keywords,
            'author': self.author,
            'copyright': self.copyright,
            'rating': str(self.rating) if self.rating else None,
            'location': self.location,
            'camera_make': self.camera_make,
            'camera_model': self.camera_model,
            'category': self.category,
            'mood': self.mood,
            'style': self.style,
            'filename': self.filename
        }
    
    @classmethod
    def create_basic(cls, title: str, description: str, subject: str, keywords: str, filename: str) -> 'ImageMetadata':
        """Factory method to create basic metadata"""
        return cls(title=title, description=description, subject=subject, keywords=keywords, filename=filename)
    
    @classmethod
    def create_full(cls, title: str, description: str, subject: str, keywords: str, filename: str,
                   author: Optional[str] = None, copyright: Optional[str] = None, rating: Optional[int] = None,
                   location: Optional[str] = None, camera_make: Optional[str] = None, camera_model: Optional[str] = None,
                   category: Optional[str] = None, mood: Optional[str] = None, style: Optional[str] = None) -> 'ImageMetadata':
        """Factory method to create full metadata with all optional fields"""
        return cls(
            title=title, description=description, subject=subject, keywords=keywords, filename=filename,
            author=author, copyright=copyright, rating=rating, location=location,
            camera_make=camera_make, camera_model=camera_model,
            category=category, mood=mood, style=style
        )
    
    @classmethod
    def from_ai_metadata(cls, ai_metadata: 'AIGeneratedMetadata', author: Optional[str] = None, 
                        copyright: Optional[str] = None, rating: Optional[int] = None) -> 'ImageMetadata':
        """Create ImageMetadata from AIGeneratedMetadata"""
        return cls(
            title=ai_metadata.title,
            description=ai_metadata.description,
            subject=ai_metadata.subject,
            keywords=ai_metadata.keywords,
            author=author,
            copyright=copyright,
            rating=rating,
            category=ai_metadata.category,
            mood=ai_metadata.mood,
            style=ai_metadata.style,
            filename=ai_metadata.filename
        )

def example_ai_metadata() -> AIGeneratedMetadata:
    ai_metadata = AIGeneratedMetadata(
        title="Fresh Fruit Salad in Coconut Bowl",
        description="Delicious & healthy summer fruit salad with watermelon, strawberries, kiwi, cherries & more! Perfect for a refreshing snack or dessert.",
        subject="Fruit salad",
        keywords="fruit salad, summer fruits, healthy snack, watermelon, strawberries, kiwi, cherries, raspberries, blueberries, coconut bowl, healthy eating, summer food",
        filename="fresh-fruit-salad-coconut-bowl",
        category="food",
        mood="refreshing, healthy, vibrant",
        style="minimalist"
    )

    if LOG and LOG_JSON: 
        print("\n🎯 AI Generated SEO Metadata:")
        print(json.dumps(asdict(ai_metadata), indent=4))
        print("\n🚀 Creating SEO optimized image...")
    return ai_metadata