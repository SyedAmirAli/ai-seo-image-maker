import os
import shutil
from PIL import Image
import piexif 
from dto import AIGeneratedMetadata
from dotenv import AUTHOR, IMAGE_SUBJECT_KEY, LOG, REMOVE_BACKUP_FILE, WEBSITE, EMAIL, OUTPUT_PATH, IMAGE_DESCRIPTION_KEY, LOG_JSON

debug_print = LOG and LOG_JSON

# Add IPTC support
try:
    from iptcinfo3 import IPTCInfo
    IPTC_AVAILABLE = True
    if debug_print: print("✅ IPTC support loaded - Adobe Stock compatible keywords enabled!")
except ImportError:
    IPTC_AVAILABLE = False
    if debug_print: print("⚠️  IPTC support not available - Adobe Stock keywords will use EXIF fallback")

def process_keywords_individually(keywords: str) -> list:
    """
    Process keywords individually and clean unwanted characters
    """
    if not keywords or not keywords.strip():
        return []
    
    # Characters to remove from keywords
    unwanted_chars = [';', '#', '/', '!', '?', '*', '<', '>', '|', '\\', '"', "'", '`', 
                     '~', '@', '%', '^', '&', '(', ')', '+', '=', '{', '}', '[', ']']
    
    # Split by common separators
    keyword_list = []
    
    # Handle both comma and semicolon separated keywords
    if ';' in keywords:
        keyword_list = keywords.split(';')
    elif ',' in keywords:
        keyword_list = keywords.split(',')
    else:
        keyword_list = [keywords]
    
    # Clean each keyword by looping and removing unwanted characters
    cleaned_keywords = []
    for keyword in keyword_list:
        # Start with the original keyword
        clean_keyword = keyword.strip()
        
        # Loop through and remove each unwanted character
        for char in unwanted_chars:
            clean_keyword = clean_keyword.replace(char, '')
        
        # Remove extra spaces and convert multiple spaces to single space
        clean_keyword = ' '.join(clean_keyword.split())
        
        # Only add if not empty and not duplicate
        if clean_keyword and clean_keyword.lower() not in [k.lower() for k in cleaned_keywords]:
            cleaned_keywords.append(clean_keyword)
    
    return cleaned_keywords
 
def safe_encode_utf16le(text) -> bytes: 
    if text is None or not str(text).strip():
        return b''
    return str(text).encode('utf-16le', errors='ignore')

def add_iptc_keywords(image_path: str, keywords_list: list, title: str) -> bool:
    """
    Add IPTC Keywords that Adobe Stock can read
    This is the PROPER way to add keywords that Adobe Stock recognizes
    """
    if not IPTC_AVAILABLE:
        if debug_print: print("⚠️  IPTC library not available - cannot set Adobe Stock compatible keywords")
        return False
        
    try:
        # Open image with IPTC support
        info = IPTCInfo(image_path)
        
        # Set IPTC Keywords (comma separated list)
        info['keywords'] = keywords_list
        
        # The 'object name' is used as the Title in Adobe Stock and other software
        info['object name'] = title
        info['caption/abstract'] = ', '.join(keywords_list) if keywords_list else ""
        
        # Save the IPTC data
        info.save()
        
        if debug_print:
            print(f"✅ IPTC Keywords set for Adobe Stock: {keywords_list}")
            print(f"✅ Total keywords: {len(keywords_list)}")
        
        return True
        
    except Exception as e:
        if debug_print: print(f"❌ IPTC Keywords error: {e}")
        return False

def add_metadata_to_image(
        image_path: str, 
        ai_metadata: AIGeneratedMetadata, 
        author: str = '', 
        copyright_info: str = '',
        rating: int = 5
    ) -> bool:
    
    try:
        if debug_print: print(f"📝 Adding metadata to: {image_path}") 
        
        # Create EXIF dict
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        if not ai_metadata.title or not ai_metadata.keywords or not ai_metadata.description or not ai_metadata.subject:
            raise ValueError("Title, keywords, description, and subject are required")

        processed_keywords = process_keywords_individually(str(ai_metadata.keywords))
        comma_keywords = ', '.join(processed_keywords)
        keywords_utf16le = safe_encode_utf16le(comma_keywords)

        if keywords_utf16le:
            exif_dict["0th"][piexif.ImageIFD.XPKeywords] = keywords_utf16le
            if debug_print: print(f"✅ XPKeywords FORCED with commas: {comma_keywords}") 

        # Set Title, Subject, and Description from AI metadata
        title_utf16le = safe_encode_utf16le(ai_metadata.title)
        exif_dict["0th"][piexif.ImageIFD.XPTitle] = title_utf16le

        subject = getattr(ai_metadata, IMAGE_SUBJECT_KEY, None)
        if subject:
            exif_dict["0th"][piexif.ImageIFD.XPSubject] = subject
            if debug_print: print(f"✅ Subject set from global variable: {IMAGE_SUBJECT_KEY}")
        else:
            exif_dict["0th"][piexif.ImageIFD.XPSubject] = title_utf16le # Set Subject to be same as Title
            if debug_print: print(f"✅ Subject set from AI metadata: {ai_metadata.title}")

        description = getattr(ai_metadata, IMAGE_DESCRIPTION_KEY, None)
        if description:
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = description
            if debug_print: print(f"✅ Description set from global variable: {IMAGE_DESCRIPTION_KEY}")
        else:
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = ai_metadata.title
            if debug_print: print(f"✅ Description set from AI metadata: {ai_metadata.title}")
        
        comment_utf16le = safe_encode_utf16le(ai_metadata.description)
        exif_dict["0th"][piexif.ImageIFD.XPComment] = comment_utf16le

        # Set Author, ensuring both standard and Windows fields are populated
        author_name = author or AUTHOR
        if author_name:
            # XPAuthor (Windows specific) uses UTF-16LE
            exif_dict["0th"][piexif.ImageIFD.XPAuthor] = safe_encode_utf16le(author_name)
            
            # Artist (Standard EXIF) uses ASCII
            exif_dict["0th"][piexif.ImageIFD.Artist] = str(author_name).encode('ascii', 'ignore')
            if debug_print: print(f"✅ Author set to: {author_name}")

        # Set Copyright
        email = EMAIL if EMAIL else ''
        if copyright_info:
            # Copyright (Standard EXIF) uses ASCII
            copyright_text = f"{WEBSITE} {copyright_info} {email}"
            exif_dict["0th"][piexif.ImageIFD.Copyright] = str(copyright_text).encode('ascii', 'ignore')
        
        if rating and isinstance(rating, int) and 1 <= rating <= 5:
            exif_dict["0th"][piexif.ImageIFD.Rating] = rating
        
        exif_dict["0th"][piexif.ImageIFD.Software] = "SEO Image AI - github.com:SyedAmirAli/seoimg-ai"

        # Apply EXIF data
        exif_bytes = piexif.dump(exif_dict)
        
        # Save EXIF metadata
        img = Image.open(image_path)
        img.save(image_path, exif=exif_bytes, quality=95, optimize=True)

        # Remove redundant IPTC logic from this function
        return True
            
    except Exception as e:
        if debug_print: print(f"❌ Metadata addition error: {e}")
        return False

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a string to be a valid filename by removing illegal characters.
    """
    if not filename:
        return "image"
    
    # Characters that are invalid in Windows filenames
    invalid_chars = '<>:"/\\|?*!@#$%^&()=[]{};:\'",'
    
    for char in invalid_chars:
        filename = filename.replace(char, '_')
        
    # Trim leading/trailing whitespace and periods
    filename = filename.strip('. ')

    # Ensure the filename is not empty after sanitization
    if not filename:
        return "image"
        
    return filename

def create_seo_optimized_image(
        image_path: str, 
        ai_metadata: AIGeneratedMetadata, 
        author: str = '', 
        copyright_info: str = '',
        output_dir: str = OUTPUT_PATH
    ) -> str: 
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    os.makedirs(output_dir, exist_ok=True)
    original_extension = os.path.splitext(image_path)[1].lower() or '.jpg'
    
    if original_extension == '.png':
        original_extension = '.jpg'
    
    # Sanitize the title to make it a valid filename
    sanitized_title = sanitize_filename(ai_metadata.title if ai_metadata.title else "image")
    new_filename = f"{sanitized_title}{original_extension}"
    new_path = os.path.join(output_dir, new_filename)
    
    counter = 1
    while os.path.exists(new_path):
        new_filename = f"{sanitized_title}_{counter}{original_extension}"
        new_path = os.path.join(output_dir, new_filename)
        counter += 1
    
    try:
        if os.path.splitext(image_path)[1].lower() == '.png' and original_extension == '.jpg':
            with Image.open(image_path) as img:
                if img.mode in ('RGBA', 'LA', 'P'):
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode in ('RGBA', 'LA'):
                        background.paste(img, mask=img.split()[-1])
                    else:
                        background.paste(img)
                    img = background
                img.save(new_path, 'JPEG', quality=95, optimize=True)
        else:
            shutil.copy2(image_path, new_path)

        
        add_metadata_to_image(new_path, ai_metadata, author, copyright_info)
        processed_keywords = process_keywords_individually(str(ai_metadata.keywords))
        if processed_keywords: 
            # Pass the title to be used for the IPTC 'object name'
            add_iptc_keywords(new_path, processed_keywords, ai_metadata.title)

        if REMOVE_BACKUP_FILE:
            bk_path = f"{new_path}~"
            if os.path.exists(bk_path):
                os.remove(bk_path)
                
        return new_path
    except Exception as e:
        if os.path.exists(new_path):
            os.remove(new_path)
        raise 