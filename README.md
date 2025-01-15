# VisionFlow

VisionFlow is a PDF-to-Mindmap converter, a Streamlit-based application designed to enhance how you understand and visualize document content. By utilizing Google Generative AI and Markmap, VisionFlow transforms PDF content into dynamic, interactive mindmaps for clear and efficient information processing.

<img src="assets\VisionFlow.png">

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/PARTHIBAN-007/VisionFlow.git
   cd VisionFlow
   ```

2. **Install dependencies**:
   Make sure you have Python installed. Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Set your Google API key as an environment variable:
   ```bash
   export GOOGLE_API_KEY='your-api-key'
   ```

4. **Run the application**:
   Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Functionality

VisionFlow provides the following functionalities:

- **PDF Text Extraction**: Upload a PDF file, and VisionFlow will extract the text content from it.
- **AI-Powered Mindmap Generation**: Utilize Google Generative AI to transform the extracted text into a hierarchical Markdown mindmap.
- **Interactive Visualization**: Visualize the generated mindmap as an interactive HTML component using D3 and Markmap libraries.
- **Markdown Editor**: Edit the generated Markdown mindmap directly within the application to refine and customize the mindmap structure.
- **Real-time Updates**: Changes made in the Markdown editor are instantly reflected in the interactive mindmap.



