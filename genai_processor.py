import os
import json
from PIL import Image
import google.generativeai as genai
from dto import AIGeneratedMetadata
from dotenv import GEMINI_API_KEY, PROMPT, MODEL

class GeminiImageAnalyzer:
    """Gemini AI powered image analyzer for SEO metadata generation"""
    
    def __init__(self, api_key: str = GEMINI_API_KEY):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(MODEL)
    
    def analyze_image(self, image_path: str) -> AIGeneratedMetadata:
        # Load image
        image = Image.open(image_path)
        
        try:
            # Generate content with image
            response = self.model.generate_content([PROMPT, image])
            
            # Clean response text (remove markdown code blocks if present)
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]  # Remove ```json
            if response_text.endswith('```'):
                response_text = response_text[:-3]  # Remove ```
            response_text = response_text.strip()
            
            # Parse JSON response
            metadata_json = json.loads(response_text)
            
            return AIGeneratedMetadata(**metadata_json)
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing AI response: {e}")
            print(f"AI Response: {response.text}")
            # Fallback metadata
            return self._create_fallback_metadata(image_path)
        except Exception as e:
            print(f"❌ Error analyzing image: {e}")
            return self._create_fallback_metadata(image_path)
    
    def _create_fallback_metadata(self, image_path: str) -> AIGeneratedMetadata:
        """Create fallback metadata if AI analysis fails"""
        filename = os.path.basename(image_path).split('.')[0]
        return AIGeneratedMetadata(
            title="Beautiful Image",
            description="A stunning image with great visual appeal",
            subject="Photography",
            keywords="image,photo,beautiful,visual,content",
            filename=f"beautiful-image-{filename}",
            category="general",
            mood="neutral",
            style="natural"
        )