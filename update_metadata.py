import os
import shutil
from PIL import Image
import piexif
from datetime import datetime
from typing import Optional
from dto import ImageMetadata, AIGeneratedMetadata
from dotenv import AUTHOR, WEBSITE, EMAIL

OUTPUT_PATH = "output"

# Create SEO optimized image with AI generated metadata
def create_seo_optimized_image(
        image_path: str, 
        ai_metadata: AIGeneratedMetadata, 
        author: str = "AI Generated", 
        copyright_info: Optional[str] = None,
        output_dir: str = OUTPUT_PATH
    ) -> str: 
    
    # Convert AI metadata to ImageMetadata
    metadata = ImageMetadata.from_ai_metadata(
        ai_metadata, 
        author=author, 
        copyright=copyright_info,
        rating=5  # Default high rating for AI-optimized images
    )
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate new filename from AI suggestion, keeping original extension
    original_extension = os.path.splitext(image_path)[1]  # Gets extension with dot (e.g., '.jpg')
    new_filename = f"{ai_metadata.filename}{original_extension}"
    new_path = os.path.join(output_dir, new_filename)
    
    # Copy image
    shutil.copy2(image_path, new_path)
    
    # Prepare EXIF metadata
    exif_dict = {
        "0th": {},
        "Exif": {},
        "GPS": {},
        "1st": {},
        "thumbnail": None,
    }
    
    # Add creator information
    if AUTHOR:
        exif_dict["0th"][piexif.ImageIFD.Artist] = AUTHOR.encode('utf-8')
        exif_dict["0th"][piexif.ImageIFD.XPAuthor] = AUTHOR.encode('utf-16le')
    if WEBSITE:
        exif_dict["0th"][piexif.ImageIFD.XPKeywords] = WEBSITE.encode('utf-16le')
        exif_dict["0th"][piexif.ImageIFD.Copyright] = f"© {AUTHOR}, {WEBSITE}".encode('utf-8')
    if EMAIL:
        exif_dict["0th"][piexif.ImageIFD.XPComment] = EMAIL.encode('utf-16le')
    
    # Add basic EXIF metadata
    if author:
        exif_dict["0th"][piexif.ImageIFD.Artist] = author.encode('utf-8')
    
    if copyright_info:
        exif_dict["0th"][piexif.ImageIFD.Copyright] = copyright_info.encode('utf-8')
    
    # Add creation date
    exif_dict["0th"][piexif.ImageIFD.DateTime] = datetime.now().strftime('%Y:%m:%d %H:%M:%S').encode('utf-8')
    
    # Add image description
    if ai_metadata.description:
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = ai_metadata.description.encode('utf-8')
    
    # Add software info
    exif_dict["0th"][piexif.ImageIFD.Software] = "SEO Image AI".encode('utf-8')
    
    # Add keywords as user comment (using ExifIFD instead of ImageIFD)
    if ai_metadata.keywords:
        keywords_text = f"Keywords: {ai_metadata.keywords}"
        if ai_metadata.category:
            keywords_text += f", Category: {ai_metadata.category}"
        if ai_metadata.mood:
            keywords_text += f", Mood: {ai_metadata.mood}"
        if ai_metadata.style:
            keywords_text += f", Style: {ai_metadata.style}"
        
        # UserComment is in ExifIFD, not ImageIFD
        exif_dict["Exif"][piexif.ExifIFD.UserComment] = keywords_text.encode('utf-8')
    
    # Convert EXIF dict to bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Apply metadata to image
    try:
        with Image.open(new_path) as img:
            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Save with EXIF metadata
            img.save(new_path, exif=exif_bytes, quality=95)
            
    except Exception as e:
        print(f"Warning: Could not apply EXIF metadata to {new_path}: {e}")
        # If EXIF fails, just save the image without metadata
        with Image.open(new_path) as img:
            img.save(new_path, quality=95)
    
    return new_path
