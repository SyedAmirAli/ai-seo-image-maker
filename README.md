# 🤖 AI-Powered Image SEO Optimizer

A powerful Python tool that uses **Google Gemini AI** to automatically analyze images and generate SEO-optimized metadata including titles, descriptions, keywords, and filenames.

## 🔐 Credentials Configuration

### 📁 Credentials Folder Structure

The `credentials/` folder contains all configuration files for the application. **All files in this folder are gitignored for security.**

```
credentials/
├── 🔑 gemini_api_key.txt    # REQUIRED: Your Google Gemini API key
├── 👤 author.txt            # Author name for metadata
├── 📝 prompt.txt            # AI prompt template for analysis
├── 🤖 model.txt             # Gemini model version to use
├── 📂 input_dir.txt         # Input directory path
├── 📂 output_dir.txt        # Output directory path
└── ©️ copyright_info.txt    # Copyright information
```

### ⚠️ **CRITICAL: API Key Setup**

**You MUST create the `gemini_api_key.txt` file before using this tool:**

```bash
# Create the credentials directory (if it doesn't exist)
mkdir -p credentials

# Create the API key file
touch credentials/gemini_api_key.txt
```

**Add your Google Gemini API key to `credentials/gemini_api_key.txt`:**

```
your_actual_gemini_api_key_here
```

**🔑 Get Your API Key:**

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it into `credentials/gemini_api_key.txt`

### 📋 Configuration Files Explained

| File                 | Purpose                              | Example Content                           |
| -------------------- | ------------------------------------ | ----------------------------------------- |
| `gemini_api_key.txt` | **REQUIRED** - Google Gemini API key | `AIzaSyD6cOloHhk4wLcYoB40RXdK_pe1XwiBtiE` |
| `author.txt`         | Author name for image metadata       | `Syed Amir Ali`                           |
| `prompt.txt`         | AI analysis prompt template          | Custom JSON prompt for SEO metadata       |
| `model.txt`          | Gemini model version                 | `gemini-1.5-flash`                        |
| `input_dir.txt`      | Input images directory               | `/path/to/your/images`                    |
| `output_dir.txt`     | Output directory                     | `/path/to/output`                         |
| `copyright_info.txt` | Copyright information                | `© 2024 Your Name`                        |

### 🔒 Security Notes

-   ✅ **All credential files are gitignored** - never committed to repository
-   ✅ **Local storage only** - credentials stay on your machine
-   ✅ **File permissions** - ensure proper access control
-   ✅ **No sensitive data in code** - all configuration externalized

**🚨 Without a valid API key in `gemini_api_key.txt`, the tool will not work!**

## ✨ Features

-   🎯 **AI-Powered Analysis** - Uses Google Gemini AI to understand image content
-   📝 **SEO Metadata Generation** - Automatically creates titles, descriptions, keywords
-   🏷️ **Smart Filename Suggestions** - Generates SEO-friendly filenames
-   📊 **Metadata Embedding** - Embeds XMP, EXIF, and IPTC metadata into images
-   🎨 **Batch Processing** - Process multiple images at once
-   🔧 **TypeScript-like Experience** - Auto-completion and type hints in Python
-   📁 **Organized Output** - Clean folder structure for processed images

## 🛠️ Installation

### Prerequisites

-   Python 3.8+
-   Google Gemini API Key

### 1. Clone the Repository

```bash
git clone https://github.com/SyedAmirAli/ai-seo-image-maker.git
cd image-seo
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. **Important: Setup API Key**

**⚠️ Required Step:** Follow the detailed setup instructions in the [Credentials Configuration](#-credentials-configuration) section above.

**Quick Setup:**

```bash
# Create the credentials directory if it doesn't exist
mkdir -p credentials

# Create the API key file (this file is gitignored for security)
touch credentials/gemini_api_key.txt
```

Then edit `credentials/gemini_api_key.txt` and add your Google Gemini API key.

**🔑 Get Your API Key:**

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into `credentials/gemini_api_key.txt`

**📋 See the [Credentials Configuration](#-credentials-configuration) section for complete details about all configuration files.**

### 5. Configure Settings

Edit `dotenv.py` to customize:

```python
# Update these values according to your needs
AUTHOR = "Your Name"
COPYRIGHT_INFO = f"© {datetime.now().year} Your Name. All rights reserved."
INPUT_DIR = "images"  # Your input images folder
OUTPUT_PATH = "ai_generated"  # Output folder
```

## 🚀 Usage

### Basic Usage

Place your images in the `images/` folder and run:

```bash
python main.py
```

The tool will:

1. 📸 Analyze all images in the input directory
2. 🧠 Generate SEO metadata using AI
3. 💾 Create optimized copies with embedded metadata
4. 📁 Save results in the output directory

### Example Output

```
🤖 Starting AI-powered image analysis...
📂 Input directory: images
📂 Output directory: ai_generated

📸 Analyzing: my-photo.jpg
✅ SEO optimized image created: ai_generated/tropical-fruits-abundance-healthy-food.jpg

🤖 1 SEO optimized images created
🔍 Use this for better search engine visibility!
```

### Generated Metadata Example

```json
{
    "title": "Tropical Fruit Abundance",
    "description": "Vibrant image of fresh tropical fruits: papaya, pineapple, kiwi, citrus fruits",
    "subject": "Assortment of tropical fruits",
    "keywords": "tropical fruits, papaya, pineapple, kiwi, healthy food, vitamin c, fresh fruit",
    "filename": "tropical-fruit-abundance-healthy-food",
    "category": "food",
    "mood": "vibrant, fresh, healthy",
    "style": "flat lay"
}
```

## 📁 Project Structure

```
image-seo/
├── 📄 main.py              # Main entry point
├── 🤖 genai_processor.py   # AI analysis logic
├── 📋 dto.py              # Data classes with type hints
├── ⚙️ update_metadata.py   # Metadata processing functions
├── 🔧 dotenv.py           # Configuration settings
├── 📁 images/             # Input images (create this folder)
├── 📁 ai_generated/       # AI-processed output
├── 📁 output/            # Manual processing output
├── 🔐 credentials/        # API keys (gitignored)
│   └── gemini_api_key.txt # Your Gemini API key
└── 📋 requirements.txt    # Python dependencies
```

## ⚙️ Configuration

### Supported Image Formats

-   `.jpg`, `.jpeg`, `.png`, `.webp`

### Customizable Settings

Edit `dotenv.py` to change:

-   **Author Information** - Your name and copyright
-   **Input/Output Directories** - Where to read/write images
-   **Logging Options** - Control console output
-   **AI Model Settings** - Gemini model configuration

## 🔧 Advanced Usage

### Using as a Library

```python
from genai_processor import GeminiImageAnalyzer
from update_metadata import create_seo_optimized_image

# Initialize analyzer
analyzer = GeminiImageAnalyzer()

# Analyze single image
metadata = analyzer.analyze_image("path/to/image.jpg")

# Create optimized image
output_path = create_seo_optimized_image(
    "path/to/image.jpg",
    metadata,
    author="Your Name",
    copyright_info="© 2024 Your Name"
)
```

### Custom Metadata Processing

```python
from dto import ImageMetadata
from update_metadata import create_seo_optimized_image

# Create custom metadata
metadata = ImageMetadata(
    title="Custom Title",
    description="Custom description",
    subject="Custom subject",
    keywords="keyword1,keyword2,keyword3",
    filename="custom-filename"
)
```

## 🚨 Important Notes

### Security

-   ✅ **API keys are gitignored** for security
-   ✅ **No sensitive data in repository**
-   ✅ **Local credential management**

### Requirements

-   **Internet connection** required for AI analysis
-   **Valid Gemini API key** with sufficient quota
-   **Write permissions** for output directories

## 🐛 Troubleshooting

### Common Issues

**"No such file: credentials/gemini_api_key.txt"**

```bash
# Create the file manually
mkdir -p credentials
echo "your_api_key_here" > credentials/gemini_api_key.txt
```

**"API key not working"**

-   Verify your API key is correct
-   Check if your Gemini API quota is available
-   Ensure internet connection is stable

**"No images found"**

-   Check if `images/` directory exists
-   Verify image files have supported extensions
-   Check file permissions

### System Dependencies

If you encounter metadata writing issues:

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install libexiv2-dev python3-dev pkg-config libboost-python-dev

# macOS (with Homebrew)
brew install exiv2 boost-python3
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

-   **Google Gemini AI** for powerful image analysis
-   **Python Community** for excellent libraries
-   **ExifTool** for metadata processing capabilities

---

**Made with ❤️ for better image SEO optimization**
