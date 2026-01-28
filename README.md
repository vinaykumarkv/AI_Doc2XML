# 📄 Document to Standard XML Converter

A powerful AI-powered tool that automatically extracts information from documents and fills XML templates using either local Ollama models or cloud-based Anthropic Claude.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Gradio](https://img.shields.io/badge/gradio-latest-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🤖 **Dual AI Support**: Choose between local Ollama models or cloud-based Anthropic Claude
- 📑 **Multiple Formats**: Support for PDF, TXT, MD, JSON, and CSV documents
- 🎯 **Smart Extraction**: AI automatically identifies and extracts relevant information
- 📋 **Template-Based**: Use your own XML templates for standardized output
- 🖥️ **User-Friendly Interface**: Clean Gradio web interface
- ⬇️ **Easy Export**: Download filled XML files directly
- 🔒 **Privacy Options**: Use local models for sensitive data

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- (Optional) Ollama installed for local AI processing

### Installation

1. Clone the repository:
```bash
git clone https://github.com/vinaykumarkv/AI_Doc2XML.git
cd AI_Doc2XML
```

2. Install dependencies:
```bash
pip install gradio requests pdfplumber
```

3. (Optional) Install Ollama for local processing:
```bash
# Visit https://ollama.ai and download for your OS
# Then pull a model:
ollama pull llama3.1
```

### Running the Application

```bash
python main.py
```

The application will launch in your default browser at `http://localhost:7860`

## 📖 Usage Guide

### Basic Workflow

1. **Upload Files**
   - Upload your source document (PDF, TXT, MD, JSON, or CSV)
   - Upload your XML template file

2. **Choose AI Provider**
   - **Ollama (Local)**: For privacy and offline processing
   - **Anthropic (Cloud)**: For high-quality results with Claude

3. **Configure Settings**
   
   **For Ollama:**
   - Test connection to ensure Ollama is running
   - Select your preferred model (llama3.1, mistral, qwen2.5, etc.)
   
   **For Anthropic:**
   - Enter your API key from [console.anthropic.com](https://console.anthropic.com)
   - Choose between Claude Sonnet or Opus

4. **Convert**
   - Click "Convert to XML"
   - View the filled XML in the output panel
   - Download the completed file

### Example Use Cases

- **Healthcare**: Convert patient records to HL7 or FHIR XML standards
- **Finance**: Transform transaction data into standard XML formats
- **Legal**: Convert contracts to structured XML documents
- **Research**: Standardize research data into XML schemas
- **Integration**: Prepare data for system-to-system XML exchanges

## 🛠️ Configuration

### Ollama Setup

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull recommended models:
```bash
ollama pull llama3.1      # Recommended for balanced performance
ollama pull mistral       # Good for smaller documents
ollama pull qwen2.5       # Good for complex extraction
```

3. Ollama will automatically start on `http://localhost:11434`

### Anthropic Setup

1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Generate an API key
3. Enter the API key in the application

**Model Options:**
- `claude-sonnet-4-20250514` - Fast and efficient (recommended)
- `claude-opus-4-20250514` - Maximum accuracy for complex documents

## 📁 Project Structure

```
AI_Doc2XML/
│
├── main.py                    # Main application file
├── README.md                  # This file
├── LICENSE                    # License file
├── .gitignore                # Git ignore rules
│
├── pdf_documents/            # Sample PDF documents
├── tested_extraction/        # Example extraction results
└── xml_template_sample/      # Sample XML templates
```

## 🔧 API Reference

### Ollama API Endpoint
```
POST http://localhost:11434/api/generate
```

### Anthropic API Endpoint
```
POST https://api.anthropic.com/v1/messages
```

## ⚙️ Advanced Configuration

### Ollama Parameters

You can adjust these in the code for fine-tuning:
```python
"options": {
    "temperature": 0.1,    # Lower = more deterministic
    "top_p": 0.9,         # Nucleus sampling
    "num_predict": 2000   # Max tokens to generate
}
```

### Anthropic Parameters

```python
"max_tokens": 4000,       # Maximum response length
```

## 🐛 Troubleshooting

### Ollama Connection Issues

**Problem**: "Cannot connect to Ollama"
- **Solution**: Ensure Ollama is running with `ollama serve`
- Check if the URL is correct (default: `http://localhost:11434`)

### PDF Extraction Issues

**Problem**: "Error converting PDF to text"
- **Solution**: Ensure PDF is not image-based or encrypted
- Try converting the PDF to text first using another tool

### API Errors

**Problem**: "API error: 401"
- **Solution**: Check your Anthropic API key is valid and has sufficient credits

### Timeout Errors

**Problem**: "Request timed out"
- **Solution**: Use a faster model, reduce document size, or increase timeout in code

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Gradio](https://gradio.app/) - For the amazing UI framework
- [Ollama](https://ollama.ai/) - For local AI model hosting
- [Anthropic](https://anthropic.com/) - For Claude AI API
- [pdfplumber](https://github.com/jsvine/pdfplumber) - For PDF text extraction

## 📧 Contact

Email: [vinaykumar.kv@outlook.com](mailto:vinaykumar.kv@outlook.com)

Project Link: [https://github.com/vinaykumarkv/AI_Doc2XML](https://github.com/yourusername/Document2standardXML)

## 🔮 Future Enhancements

- [ ] Batch processing for multiple documents
- [ ] Custom prompt templates
- [ ] Support for more document formats (DOCX, XLSX)
- [ ] XML validation against schemas
- [ ] History and version tracking
- [ ] Multi-language support
- [ ] API endpoint for programmatic access
- [ ] Docker containerization

## 📊 Performance Tips

1. **For Large Documents**: Use Anthropic Claude for better accuracy
2. **For Speed**: Use smaller Ollama models like `mistral`
3. **For Privacy**: Always use local Ollama models
4. **For Complex XML**: Use Claude Opus for best results
5. **Batch Processing**: Process similar documents together for consistency

---

