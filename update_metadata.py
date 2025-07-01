import os
import shutil
import pyexiv2
from datetime import datetime
from dto import ImageMetadata, AIGeneratedMetadata

OUTPUT_PATH = "output"

# Create SEO optimized image with AI generated metadata
def create_seo_optimized_image(
        image_path: str, 
        ai_metadata: AIGeneratedMetadata, 
        author: str = "AI Generated", 
        copyright_info: str = None,
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
    
    # Generate new filename from AI suggestion
    extension = image_path.split('.')[-1]
    new_filename = f"{ai_metadata.filename}.{extension}"
    new_path = os.path.join(output_dir, new_filename)
    
    # Copy image
    shutil.copy2(image_path, new_path)
    
    # Prepare metadata
    xmp_metadata = {
        'Xmp.dc.title': ai_metadata.title,
        'Xmp.dc.subject': ai_metadata.subject,
        'Xmp.dc.description': ai_metadata.description,
        'Xmp.photoshop.DateCreated': datetime.now().strftime('%Y-%m-%d'),
        'Xmp.dc.creator': author,
    }
    
    exif_metadata = {
        'Exif.Image.Artist': author,
    }
    
    iptc_metadata = {}
    
    # Add keywords
    keywords_list = [k.strip() for k in ai_metadata.keywords.split(',')]
    for i, keyword in enumerate(keywords_list):
        xmp_metadata[f'Xmp.dc.subject[{i+1}]'] = keyword
    
    # Add AI-specific metadata
    if ai_metadata.category:
        xmp_metadata['Xmp.photoshop.Category'] = ai_metadata.category
        
    if ai_metadata.mood:
        xmp_metadata['Xmp.photoshop.Instructions'] = f"Mood: {ai_metadata.mood}"
        
    if ai_metadata.style:
        xmp_metadata['Xmp.photoshop.Credit'] = f"Style: {ai_metadata.style}"
        
    if copyright_info:
        xmp_metadata['Xmp.dc.rights'] = copyright_info
        exif_metadata['Exif.Image.Copyright'] = copyright_info
    
    # Apply metadata
    with pyexiv2.Image(new_path) as img:
        img.modify_xmp(xmp_metadata)
        img.modify_exif(exif_metadata)
        if iptc_metadata:
            img.modify_iptc(iptc_metadata)
    
    return new_path
