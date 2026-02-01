# 🎭 Othello RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about Shakespeare's **Othello** using ChromaDB for vector storage and LM Studio (Mistral 7B / DeepSeek) for text generation.

## 📋 Features

- 💬 **Interactive Chat**: Ask questions about Othello in natural language
- 🔍 **Semantic Search**: Find relevant passages using ChromaDB vector search
- 🔄 **Query Rewriting**: Generates multiple query variants for better recall
- 🤖 **Model Choice**: Switch between Mistral 7B and DeepSeek models
- 📚 **Source Display**: See which passages were used to generate answers

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd othello_rag
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the Othello text

Create a `source` folder and add the Othello text:

```bash
mkdir source
```

Download the plain text version of Othello from Project Gutenberg:
- URL: https://www.gutenberg.org/ebooks/1531
- Save as `source/Othello.txt`

### 5. Create the vector database

```bash
python create_vector_db.py
```

### 6. Set up LM Studio

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Download models:
   - **Mistral 7B Instruct**: `mistralai/Mistral-7B-Instruct-v0.2`
   - **DeepSeek**: Your preferred DeepSeek model
3. Load a model in LM Studio
4. Start the local server (Developer tab → Start Server)

### 7. Run the application

```bash
streamlit run main.py
```

## 📁 Project Structure

```
othello_rag/
├── main.py                   # Main Streamlit entry point
├── create_vector_db.py       # Script to create ChromaDB database
├── chroma_manager.py         # ChromaDB operations module
├── source/
│   └── Othello.txt           # Othello text from Gutenberg
├── pages/
│   ├── 1_🏠_Home.py          # Home page with overview
│   ├── 2_💬_Chat.py          # Chat interface
│   └── 3_⚙️_Model.py         # Model selection & configuration
├── chroma_db/                # ChromaDB storage (auto-created)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Usage

### Home Page
- View application overview
- Check database status
- See example questions

### Chat Page
- Enter questions about Othello
- Toggle query rewriting
- View retrieved sources
- See conversation history

### Model Page
- **Select model**: Choose between Mistral 7B and DeepSeek
- **Configure connection**: Set LM Studio URL
- **Adjust parameters**: Temperature and max tokens
- **Test connection**: Verify LM Studio is working

## ⚙️ Configuration

### Default Settings

| Setting | Default Value |
|---------|---------------|
| LM Studio URL | `http://localhost:1234/v1` |
| Default Model | Mistral 7B Instruct |
| Temperature | `0.7` |
| Max Tokens | `800` |
| Query Rewriting | Enabled |

### Available Models

| Model | Description |
|-------|-------------|
| **Mistral 7B Instruct** | Fast, efficient for general Q&A |
| **DeepSeek** | Alternative for comparison |

## 📝 Example Questions

- "Who is Iago and what are his motivations?"
- "Describe the relationship between Othello and Desdemona"
- "What role does the handkerchief play in the story?"
- "How does jealousy drive the plot of Othello?"
- "What happens in the final scene of the play?"

## 🐛 Troubleshooting

### "Vector database not found"
```bash
python create_vector_db.py
```

### "Connection failed" to LM Studio
1. Ensure LM Studio is running
2. Verify a model is loaded
3. Check the local server is started
4. Verify the URL (default: `http://localhost:1234/v1`)

### Model not responding correctly
- Go to **Model** page
- Click "📋 List Models" to see available model IDs
- Update the model ID in Advanced settings if needed

## 📦 Dependencies

- `streamlit` - Web application framework
- `chromadb` - Vector database
- `sentence-transformers` - Embedding generation
- `openai` - LM Studio API client
- `numpy` - Numerical operations
- `requests` - HTTP requests

## 📄 License

MIT License