import os
import json
from dataclasses import asdict
from datetime import datetime
from genai_processor import GeminiImageAnalyzer
from update_metadata import create_seo_optimized_image
from dotenv import COPYRIGHT_INFO, AUTHOR, INPUT_DIR, OUTPUT_PATH, LOG, ACCEPT_EXTENSION, LOG_JSON

def create_seo_image(path: str, log: bool = LOG, log_json: bool = LOG_JSON) -> str:
    if log: print(f"📸 Analyzing: {path.split('/')[-1]}")
    
    analyzer = GeminiImageAnalyzer()
    ai_metadata = analyzer.analyze_image(path)
    
    if log and log_json: 
        print("\n🎯 AI Generated SEO Metadata:")
        print(json.dumps(asdict(ai_metadata), indent=4))
        print("\n🚀 Creating SEO optimized image...") 
    
    new_image_path = create_seo_optimized_image(
        path, 
        ai_metadata, 
        author=AUTHOR,
        copyright_info=COPYRIGHT_INFO,
        output_dir=OUTPUT_PATH
    )
    
    if log: print(f"✅ SEO optimized image created: {new_image_path}\n")
    return new_image_path

def get_input_images(accept_extension: list[str] = ACCEPT_EXTENSION) -> list[str]:
    files = []
    for file in os.listdir(INPUT_DIR):
        if file.split('.')[-1] in accept_extension:
            files.append(os.path.join(INPUT_DIR, file))
    return files

if __name__ == "__main__":
    print("🤖 Starting AI-powered image analysis...")
    print(f"📂 Input directory: {INPUT_DIR}")
    print(f"📂 Output directory: {OUTPUT_PATH}")
    print(f"\n---------------------------------------------------\n")

    generated_files = []
    images = get_input_images()
    for image in images:
        generated_files.append(create_seo_image(image))

    # Print the generated files
    print(f"\n---------------------------------------------------\n")
    print(f"🤖 {len(generated_files)} SEO optimized images created")
    print(f"🔍 Use this for better search engine visibility!")
    

# def main():
#     print("🤖 Starting AI-powered image analysis...")
#     print(f"📸 Analyzing: {IMAGE_PATH.split('/')[-1]}")
    
#     analyzer = GeminiImageAnalyzer()
#     ai_metadata = analyzer.analyze_image(IMAGE_PATH)
    
#     # Convert dataclass to dict for JSON serialization
#     metadata_dict = asdict(ai_metadata)
    
#     print("\n🎯 AI Generated SEO Metadata:")
#     print(json.dumps(metadata_dict, indent=4))
    
#     # Create SEO optimized image
#     print("\n🚀 Creating SEO optimized image...") 
    
#     new_image_path = create_seo_optimized_image(
#         IMAGE_PATH, 
#         ai_metadata, 
#         author=AUTHOR,
#         copyright_info=COPYRIGHT_INFO,
#         output_dir=OUTPUT_PATH
#     )
    
#     print(f"\n✅ SEO optimized image created: {new_image_path}")
#     print(f"🔍 Use this for better search engine visibility!")

# if __name__ == "__main__":
#     main()
