import os 
from dto import example_ai_metadata
from genai_processor import GeminiImageAnalyzer
from update_metadata import create_seo_optimized_image
from dotenv import COPYRIGHT_INFO, AUTHOR, INPUT_DIR, OUTPUT_PATH, LOG, ACCEPT_EXTENSION, LOG_JSON

def get_input_images(accept_extension: list[str] = ACCEPT_EXTENSION) -> list[str]:
    files = []
    for file in os.listdir(INPUT_DIR):
        if file.split('.')[-1] in accept_extension:
            files.append(os.path.join(INPUT_DIR, file))
    return files

# all input files
images = get_input_images()

def create_seo_image(path: str, generated_files: list[str]) -> str:
    if LOG: print(f"📸 Analyzing: {path.split('/')[-1]}")
    
    analyzer = GeminiImageAnalyzer()
    ai_metadata = analyzer.analyze_image(path)
    # ai_metadata = example_ai_metadata()

    new_image_path = create_seo_optimized_image(
        path, 
        ai_metadata, 
        author=AUTHOR if AUTHOR else "",
        copyright_info=COPYRIGHT_INFO,
        output_dir=OUTPUT_PATH
    )
    
    if LOG: print(f"✅ ({len(generated_files) + 1}/{len(images)}) ~ {new_image_path}\n")
    return new_image_path

if __name__ == "__main__":
    generated_files = []

    print("\n🤖 Starting AI-powered image analysis...")
    print(f"📂 ({len(images)}) ~ Input directory: {INPUT_DIR}")
    print(f"📂 Output directory: {OUTPUT_PATH}")
    print(f"\n---------------------------------------------------\n")

    for image in images:
        file = create_seo_image(image, generated_files)
        generated_files.append(file)

    # Print the generated files
    print(f"\n---------------------------------------------------\n")
    print(f"🤖 {len(generated_files)} SEO optimized images created")
    print(f"🔍 Use this for better search engine visibility!")
    

