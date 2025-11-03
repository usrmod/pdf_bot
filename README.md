# Multi-Image PDF Creator Telegram Bot

A professional Telegram bot that converts single or multiple images into standardized A4-sized PDF documents. Features intelligent image scaling, aspect ratio preservation, and sequential page ordering. Deployed on self-managed AlmaLinux VPS for continuous operation.

## 🎯 Features

### Core Functionality
- **Single Image to PDF**: Instant PDF generation from any image
- **Multi-Image Batch Processing**: Combine unlimited images into one PDF
- **A4 Standardization**: All pages formatted to A4 dimensions (1238×1754 points)
- **Smart Scaling**: Automatic aspect ratio preservation with centered positioning
- **Order Preservation**: Images appear in PDF exactly as sent
- **High Quality Output**: No compression or quality loss during conversion

### User Experience
- **Interactive Workflow**: Step-by-step guidance through PDF creation
- **Progress Tracking**: Real-time feedback on image collection
- **Cancellation Support**: Abort and restart at any time
- **Clear Instructions**: Inline help and command documentation
- **Error Recovery**: Graceful handling of edge cases

### Production Features
- **Time-Based Logging**: Daily log rotation at midnight, 7-day retention
- **Memory Efficient**: Processes images in-memory without disk writes
- **Async Architecture**: Non-blocking operations for optimal performance
- **Zero Data Retention**: Images cleared immediately after PDF creation

## 🏗️ Architecture

### Project Structure

pdf-creator-bot/
├── main.py # Application entry point and bot initialization
├── bot.py # Command handlers and user interaction logic
├── image_to_pdf.py # PDF generation engine with PyMuPDF
├── config.py # Environment configuration management
├── pyproject.toml # Project dependencies and metadata
├── .env # Environment variables (not in repo)
└── bot.log # Application logs (auto-rotated)

text

### Technology Stack
- **Runtime**: Python 3.13+
- **Bot Framework**: python-telegram-bot 22.5
- **PDF Engine**: PyMuPDF (pymupdf) 1.26.5
- **Image Processing**: Pillow 12.0.0
- **Package Manager**: uv (ultra-fast Python package installer)

### Image Processing Pipeline

User Input → Telegram API → BytesIO Buffer → PIL Image Analysis →
PyMuPDF Processing → A4 Page Creation → Image Scaling & Centering →
PDF Assembly → BytesIO Output → Telegram Delivery

text

## 📋 Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/start` | Welcome message and bot introduction | `/start` |
| `/help` | Display all commands and workflow guide | `/help` |
| `/start_pdf` | Begin image collection for PDF creation | `/start_pdf` |
| `/finish` | Generate PDF from collected images | `/finish` (after sending images) |
| `/cancel` | Cancel current operation and clear images | `/cancel` |
| `/test` | Bot health check | `/test` |

## 🔄 Usage Workflow

### Creating a PDF

1. **Initiate Collection**

User: /start_pdf
Bot: 📸 Send me images one by one...

text

2. **Send Images**

User: [Sends Image 1]
Bot: ✅ Image 1 added! Send more or use /finish

User: [Sends Image 2]
Bot: ✅ Image 2 added! Send more or use /finish

User: [Sends Image 3]
Bot: ✅ Image 3 added! Send more or use /finish

text

3. **Generate PDF**

User: /finish
Bot: 📄 Creating PDF from 3 image(s)...
Bot: [Sends PDF file: combined_3_pages.pdf]
Bot: ✅ PDF created with 3 page(s)!

text

### Cancelling Operation

User: /cancel
Bot: ❌ Cancelled. All images cleared.

text

## 🚀 Deployment

### VPS Infrastructure (AlmaLinux)

#### Server Setup from Scratch

1. Update system packages

sudo dnf update -y
sudo dnf install git curl -y
2. Install uv package manager

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
3. Verify installation

uv --version

text

#### Repository Deployment

1. Clone from GitHub

git clone https://github.com/YOUR_USERNAME/pdf-creator-bot.git
cd pdf-creator-bot
2. Pull latest changes (ongoing updates)

git fetch origin
git merge origin/main
3. Configure environment

echo "BOT_TOKEN=your_bot_token_from_botfather" > .env
4. Install dependencies and create virtual environment

uv sync
5. Launch bot

uv run main.py

text

### Production Deployment with systemd

Create service file

sudo nano /etc/systemd/system/pdf-bot.service

text
undefined

[Unit]
Description=Telegram PDF Creator Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/pdf-creator-bot
Environment="PATH=/home/your_user/.cargo/bin:/usr/bin"
ExecStart=/home/your_user/.cargo/bin/uv run main.py
Restart=always
RestartSec=10
StandardOutput=null
StandardError=journal

[Install]
WantedBy=multi-user.target

text
undefined

Enable and manage service

sudo systemctl daemon-reload
sudo systemctl enable pdf-bot
sudo systemctl start pdf-bot
Check status

sudo systemctl status pdf-bot
View logs

sudo journalctl -u pdf-bot -f

text

### Continuous Integration

Update deployment with latest code

cd /path/to/pdf-creator-bot
git fetch origin
git merge origin/main
uv sync # Update dependencies if changed
sudo systemctl restart pdf-bot

text

## 📊 Logging & Monitoring

### Logging Configuration
- **Strategy**: Time-based rotation
- **Frequency**: Daily at midnight
- **Retention**: 7 days
- **Format**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- **Output**: File-only (no console output in production)

### Log File Structure

bot.log # Current day's logs
bot.log.2025-11-03 # Previous day
bot.log.2025-11-02 # 2 days ago
...
bot.log.2025-10-28 # 7 days ago (automatically deleted)

text

### Monitoring Commands

Real-time log tail

tail -f bot.log
View last 100 lines

tail -n 100 bot.log
Search for errors

grep -i error bot.log*
Count daily operations

grep "PDF created" bot.log | wc -l

text

## 🎨 PDF Specifications

### Page Format
- **Size**: A4 (1238 × 1754 points)
- **Orientation**: Portrait
- **Background**: White (#FFFFFF)
- **Margins**: Dynamic based on image size

### Image Processing
- **Scaling Algorithm**: Proportional fit (maintains aspect ratio)
- **Positioning**: Centered on page
- **Quality**: Lossless (no compression)
- **Supported Formats**: All Telegram-supported image formats

### Example Transformations

Portrait Image (600×800):
→ Scaled to fit A4
→ Centered horizontally
→ No distortion

Landscape Image (1600×900):
→ Scaled to fit A4 width
→ Centered vertically
→ Aspect ratio preserved

Square Image (1000×1000):
→ Scaled to largest fit
→ Centered both axes
→ Perfect square maintained

text

## 🔐 Security & Privacy

### Current Security Measures
- Environment-based secret management (`.env`)
- No database or persistent storage
- Memory-only image processing
- Automatic data cleanup after PDF generation

### Known Limitations & Roadmap
⚠️ **Currently Missing** (Planned Implementation):
- **Rate Limiting**: No per-user request throttling
- **User Authentication**: No access control system
- **File Size Limits**: Relies on Telegram's built-in limits only
- **Concurrent User Handling**: Single-threaded processing

🚧 **In Development**:
1. **Phase 1**: Per-user rate limiting (X PDFs per hour)
2. **Phase 2**: User whitelist/blacklist system
3. **Phase 3**: Admin dashboard for monitoring
4. **Phase 4**: Advanced PDF features (encryption, watermarks)

## 🎥 Live Demo

**Bot Access**: Provided exclusively in my resume for recruiter evaluation.

> **Privacy Note**: The bot link is not publicly available to prevent abuse and maintain service quality. Recruiters and potential employers can find the bot link in my resume or request access via email.

## 🛠️ Local Development

### Prerequisites
- Python 3.13 or higher
- Telegram Bot Token (obtain from [@BotFather](https://t.me/botfather))
- uv package manager

### Development Setup

1. Clone repository

git clone https://github.com/YOUR_USERNAME/pdf-creator-bot.git
cd pdf-creator-bot
2. Install uv (if not present)

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
3. Create environment file

cat > .env << EOF
BOT_TOKEN=your_development_token_here
EOF
4. Install dependencies

uv sync
5. Run in development mode (with console logging)
Edit main.py: Uncomment logging.StreamHandler() line

uv run main.py

text

### Testing Workflow

1. Start bot

uv run main.py
2. Open Telegram and find your bot
3. Test commands:
/start → Welcome message
/start_pdf → Begin collection
[Send 2-3 images]
/finish → Receive PDF
4. Check logs

tail -f bot.log

text

## 📝 Code Architecture

### Module Responsibilities

#### `main.py` - Application Bootstrap
- Bot initialization with Telegram API
- Logging system configuration (TimedRotatingFileHandler)
- Command handler registration
- Application lifecycle management
- Graceful shutdown handling

#### `bot.py` - User Interaction Layer
- Async command handlers following python-telegram-bot patterns
- User state management with `context.user_data`
- Image collection workflow orchestration
- Error handling and user feedback
- Input validation and sanitization

#### `image_to_pdf.py` - PDF Generation Engine
- PyMuPDF document creation and manipulation
- Image-to-PDF conversion pipeline
- A4 page standardization
- Aspect ratio calculation and scaling
- Centered image positioning algorithm
- BytesIO stream handling for memory efficiency

#### `config.py` - Configuration Management
- Environment variable loading with python-dotenv
- Centralized settings management
- Secrets handling (bot token)

### Key Algorithms

**Aspect Ratio Preservation**:

def fit_image_to_page(img_width, img_height, page_width, page_height):
# Calculate scaling ratios for both dimensions
width_ratio = page_width / img_width
height_ratio = page_height / img_height

text
# Use smaller ratio to ensure complete fit
scale = min(width_ratio, height_ratio)

# Apply scaling
new_width = img_width * scale
new_height = img_height * scale

# Center on page
x_offset = (page_width - new_width) / 2
y_offset = (page_height - new_height) / 2

return Rect(x_offset, y_offset, 
            x_offset + new_width, 
            y_offset + new_height)

text

## 🐛 Known Issues & Workarounds

### Current Limitations
1. **No Batch Size Limit**: Users can theoretically send hundreds of images
   - **Impact**: Memory usage scales linearly with image count
   - **Mitigation**: Relies on Telegram's file size limits (20MB per image)
   
2. **No Image Validation**: Accepts any image format Telegram supports
   - **Impact**: Potential for processing failures with exotic formats
   - **Mitigation**: Try-catch blocks provide graceful error handling

3. **Sequential Processing**: Images processed one at a time
   - **Impact**: Large batches take longer to process
   - **Rationale**: Optimized for VPS resource constraints

### Planned Enhancements
- [ ] Maximum image count limit (e.g., 50 images per PDF)
- [ ] Image format validation (whitelist approach)
- [ ] File size pre-check before processing
- [ ] Compression options for large PDFs
- [ ] Custom page size options (A3, Letter, Legal)

## 📚 Dependencies

### Core Dependencies

python = ">=3.13"
python-telegram-bot = ">=22.5"
pymupdf = ">=1.26.5"
pillow = ">=12.0.0"
python-dotenv = ">=1.2.1"

text

### Why These Versions?
- **Python 3.13**: Latest performance improvements and type hints
- **python-telegram-bot 22.5**: Latest async API with improved error handling
- **PyMuPDF 1.26.5**: Significant PDF rendering performance gains
- **Pillow 12.0**: Enhanced image format support

## 📜 License

This project is for portfolio and demonstration purposes.

## 🙏 Acknowledgments

- **python-telegram-bot**: Comprehensive and well-documented bot framework
- **PyMuPDF**: Fast and reliable PDF manipulation library
- **Astral**: uv package manager for blazing-fast dependency management
- **AlmaLinux**: Enterprise-grade stability for production hosting

## 📈 Project Status

**Current Version**: 0.1.0  
**Status**: ✅ Production (Deployed on AlmaLinux VPS)  
**Uptime**: 24/7 with systemd process supervision  
**Last Updated**: November 2025  
**Active Development**: Yes (continuous improvements)

---

**🔗 Related Projects**
- [Background Remover Bot](../bg-remover-bot) - AI-powered background removal
- [YouTube Downloader Bot](../yt-downloader-bot) - Video/audio downloader *(if applicable)*

**🌟 Star this repository if you find it useful!**