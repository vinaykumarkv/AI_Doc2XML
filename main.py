import gradio as gr
import requests
import json
import pdfplumber



def test_ollama_connection(ollama_url):
    """Test connection to Ollama and get available models"""
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            return f"✅ Connected! Found {len(models)} model(s): {', '.join(models)}", gr.update(choices=models,
                                                                                                value=models[
                                                                                                    0] if models else None)
        return "❌ Cannot connect to Ollama", gr.update(choices=[], value=None)
    except Exception as e:
        return f"❌ Error: {str(e)}", gr.update(choices=[], value=None)


def convert_with_ollama(document_content, template_content, ollama_url, model_name):
    """Convert document to XML using Ollama"""
    prompt = f"""You are a data extraction expert. I have a document and an XML template. Your task is to extract relevant information from the document and fill in the XML template accurately.

DOCUMENT CONTENT:
{document_content}

XML TEMPLATE:
{template_content}

Instructions:
1. Analyze the document content carefully
2. Identify what information needs to go into each field in the XML template
3. Extract the relevant information from the document
4. Fill in the XML template with the extracted data
5. Maintain the exact XML structure and format
6. For fields where information is not available in the document, leave them empty or use appropriate placeholder values
7. Return ONLY the filled XML, no explanations or additional text

Please provide the filled XML template now:"""

    try:
        print(f"📤 Sending request to Ollama ({model_name})...")

        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 2000
                }
            },
            timeout=300
        )

        print(f"📥 Response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            xml_output = result.get('response', '')

            print(f"📝 Raw output length: {len(xml_output)} characters")

            # Clean up markdown formatting
            xml_output = xml_output.replace('```xml\n', '').replace('```\n', '').replace('```', '').strip()

            print(f"✨ Cleaned output length: {len(xml_output)} characters")
            print(f"📄 First 200 chars: {xml_output[:200]}")

            if xml_output:
                return xml_output, "✅ Conversion successful!"
            else:
                return None, "❌ Model returned empty response"
        else:
            return None, f"❌ Ollama API error: {response.status_code}"

    except requests.Timeout:
        return None, "❌ Request timed out. Try using a smaller/faster model or shorter documents."
    except Exception as e:
        print(f"❌ Exception: {type(e).__name__}: {str(e)}")
        return None, f"❌ Error calling Ollama: {str(e)}"


def convert_with_anthropic(document_content, template_content, model_name, api_key):
    """Convert document to XML using Anthropic Claude"""
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": model_name,
                "max_tokens": 4000,
                "messages": [
                    {
                        "role": "user",
                        "content": f"""You are a data extraction expert. I have a document and an XML template. Your task is to extract relevant information from the document and fill in the XML template accurately.

DOCUMENT CONTENT:
{document_content}

XML TEMPLATE:
{template_content}

Instructions:
1. Analyze the document content carefully
2. Identify what information needs to go into each field in the XML template
3. Extract the relevant information from the document
4. Fill in the XML template with the extracted data
5. Maintain the exact XML structure and format
6. For fields where information is not available in the document, leave them empty or use appropriate placeholder values
7. Return ONLY the filled XML, no explanations or additional text

Please provide the filled XML template now:"""
                    }
                ]
            },
            timeout=120
        )

        if response.status_code == 200:
            data = response.json()
            xml_output = data['content'][0]['text']
            xml_output = xml_output.replace('```xml\n', '').replace('```\n', '').replace('```', '').strip()
            return xml_output, "✅ Conversion successful!"
        else:
            return None, f"❌ Anthropic API error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"❌ Error calling Anthropic: {str(e)}"


def process_conversion(document_file, template_file, provider, ollama_url, ollama_model, anthropic_api_key,
                       anthropic_model):
    """Main conversion function"""
    if not document_file or not template_file:
        return None, "❌ Please upload both document and XML template"

    try:
        print(f"📂 Reading files...")
        print(f"   Document: {document_file.name}")
        print(f"   Template: {template_file.name}")
        if document_file.endswith('.pdf'):
            try:
                # Extract text using pdfplumber
                with pdfplumber.open(document_file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
                    document_content = text
            except Exception as e:
                return "", f"Error converting PDF to text: {str(e)}", None
        else:# Read files
            with open(document_file.name, 'r', encoding='utf-8') as f:
                document_content = f.read()

        with open(template_file.name, 'r', encoding='utf-8') as f:
            template_content = f.read()

        print(f"📊 Document size: {len(document_content)} characters")
        print(f"📊 Template size: {len(template_content)} characters")

        # Convert based on provider
        if provider == "Ollama (Local)":
            if not ollama_model:
                return None, "❌ Please select an Ollama model"
            print(f"🔄 Using Ollama with model: {ollama_model}")
            return convert_with_ollama(document_content, template_content, ollama_url, ollama_model)
        else:  # Anthropic
            if not anthropic_api_key:
                return None, "❌ Please enter your Anthropic API key"
            print(f"🔄 Using Anthropic with model: {anthropic_model}")
            return convert_with_anthropic(document_content, template_content, anthropic_model, anthropic_api_key)

    except Exception as e:
        print(f"❌ Exception in process_conversion: {type(e).__name__}: {str(e)}")
        return None, f"❌ Error processing files: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="RAG XML Converter", theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 📄 Document to Standard XML Converter
    Upload your document and XML template to automatically extract and fill data using AI
    """)

    with gr.Row():
        with gr.Column(scale=2):
            # File uploads
            with gr.Row():
                document_file = gr.File(
                    label="📄 Upload Document",
                    file_types=['.pdf','.txt', '.md', '.json', '.csv'],
                    type='filepath'
                )
                template_file = gr.File(
                    label="📋 Upload XML Template",
                    file_types=['.xml'],
                    type='filepath'
                )

            # Provider selection
            provider = gr.Radio(
                choices=["Ollama (Local)", "Anthropic (Cloud)"],
                value="Ollama (Local)",
                label="AI Provider",
                info="Choose between local Ollama or cloud-based Anthropic"
            )

            # Ollama settings
            with gr.Group(visible=True) as ollama_settings:
                gr.Markdown("### Ollama Configuration")
                ollama_url = gr.Textbox(
                    value="http://localhost:11434",
                    label="Ollama URL",
                    info="URL where Ollama is running"
                )

                with gr.Row():
                    test_btn = gr.Button("🔍 Test Connection", size="sm")
                    connection_status = gr.Textbox(label="Status", interactive=False, scale=2)

                ollama_model = gr.Dropdown(
                    choices=[],
                    label="Select Model",
                    info="Choose from available local models",
                    allow_custom_value=True,
                    value="llama3.1"
                )

                gr.Markdown("""
                **Setup Ollama:**
                1. Install from [ollama.ai](https://ollama.ai)
                2. Run: `ollama pull llama3.1`
                3. Ollama starts automatically on port 11434

                **Recommended Models:** llama3.1, mistral, qwen2.5
                """)

            # Anthropic settings
            with gr.Group(visible=False) as anthropic_settings:
                gr.Markdown("### Anthropic Configuration")
                anthropic_api_key = gr.Textbox(
                    label="API Key",
                    type="password",
                    info="Enter your Anthropic API key"
                )
                anthropic_model = gr.Dropdown(
                    choices=["claude-sonnet-4-20250514", "claude-opus-4-20250514"],
                    value="claude-sonnet-4-20250514",
                    label="Select Model"
                )
                gr.Markdown("💡 Get your API key from [console.anthropic.com](https://console.anthropic.com)")

            # Convert button
            convert_btn = gr.Button("🚀 Convert to XML", variant="primary", size="lg")
            status_msg = gr.Textbox(label="Status", interactive=False)

        with gr.Column(scale=3):
            # Output
            gr.Markdown("### ✨ Filled XML Result")
            output_xml = gr.Code(
                label="Generated XML",
                language="html",
                lines=25
            )

            with gr.Row():
                download_btn = gr.File(label="⬇️ Download XML", interactive=False)
                clear_btn = gr.Button("🔄 Clear All", size="sm")


    # Event handlers
    def toggle_provider(provider):
        if provider == "Ollama (Local)":
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)


    provider.change(
        fn=toggle_provider,
        inputs=[provider],
        outputs=[ollama_settings, anthropic_settings]
    )

    test_btn.click(
        fn=test_ollama_connection,
        inputs=[ollama_url],
        outputs=[connection_status, ollama_model]
    )


    def convert_and_save(document_file, template_file, provider, ollama_url, ollama_model, anthropic_api_key,
                         anthropic_model):
        xml_output, status = process_conversion(
            document_file, template_file, provider,
            ollama_url, ollama_model,
            anthropic_api_key, anthropic_model
        )

        if xml_output:
            # Save to file for download
            output_path = "filled_template.xml"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(xml_output)

            print(f"✅ XML Output ({len(xml_output)} chars):")
            print(xml_output[:500])  # Print first 500 chars for debugging

            return xml_output, status, output_path
        else:
            print(f"❌ No output. Status: {status}")
            return "", status, None


    convert_btn.click(
        fn=convert_and_save,
        inputs=[
            document_file, template_file, provider,
            ollama_url, ollama_model,
            anthropic_api_key, anthropic_model
        ],
        outputs=[output_xml, status_msg, download_btn]
    )


    def clear_all():
        return None, None, None, "", None


    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[document_file, template_file, output_xml, status_msg, download_btn]
    )

    gr.Markdown("""
    ---
    ### 📖 How It Works
    1. **Upload** your source document and XML template
    2. **Configure** your AI provider (local Ollama or cloud Anthropic)
    3. **Convert** - The AI analyzes your document and fills the XML template
    4. **Download** your completed XML file
    """)

# Launch the app
if __name__ == "__main__":
    app.launch(share=False)