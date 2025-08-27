# "G言 Y芍n"--GELAO DIGITAL MUSEUM -V1.0

The "Gelao Digital Museum" is a cutting-edge, AI-powered interactive web application. Its core mission is to preserve, inherit, and popularize the profound cultural heritage of the Gelao (崲檗逜) ethnic group of China in a modern way. We are dedicated to breaking the physical boundaries of traditional museums by transforming rich historical records and ethnic memories into a living "digital entity" named "G言 Y芍n"〞an AI you can engage in deep conversation with, anytime and anywhere.

## Key Features & Highlights
1.  **AI-Powered Conversational Guide ("G言 Y芍n")**
    * **Specialized Knowledge**: Every conversation with "G言 Y芍n" is a precise cultural exploration. Its knowledge base is strictly limited to the cultural domain of the Gelao people, enabling it to provide professional and detailed answers on topics like history, folklore, language, attire, architecture, mythology, and more.
    * **Engaging & Gentle Narration**: Through meticulous Prompt Engineering, we've endowed "G言 Y芍n" with a warm, enthusiastic, and gentle personality. It doesn't just answer questions; it narrates cultural stories in an engaging, conversational tone, as if sharing fascinating tales with a friend, aiming to spark the user's curiosity.
    * **Streaming "Typewriter" Output**: To simulate a natural conversation pace, the AI's responses are streamed character-by-character in a "typewriter" effect, significantly enhancing the sense of realism and immersion.

2.  **Immersive Experience with Text and Images**
    * **Intelligent Image Integration**: When a conversation touches upon visual subjects (e.g., clothing, food, architecture), "G言 Y芍n" automatically searches the web for relevant, high-quality images and seamlessly embeds them into the response, delivering a truly rich, multimedia experience.
    * **"Image Engine" Mode**: Users can directly ask the AI to display a picture (e.g., "Show me a picture of Gelao three-colored rice"). The AI will then prioritize the image as the main part of its response, accompanied by a concise caption, functioning as an intelligent ethnic culture image gallery.

3.  **Premium, Design-Driven UI/UX**
    * **Unified "Digital Art Gallery" Aesthetic**: From the homepage's interactive 3D elements and dynamic particle background to the feature page's 3D tilting exhibition boards and the chat page's "AI Workbench" layout, every interface adheres to a unified, minimalist, and premium dark-theme design language, creating a professional and immersive museum atmosphere.
    * **Modern Interactive Functions**: The chat interface is equipped with industry-standard features, including "New Chat," session history management, real-time search, and "Copy/Regenerate" buttons, providing users with a complete and efficient workflow.
    * **Stateless Session Mode**: To ensure privacy and simplicity, all chat logs are retained only for the current session. Closing or refreshing the page clears the history, making every visit a fresh start.


## Prerequisites
- [Anaconda / Miniconda](https://docs.conda.io/) installed
- Internet access to install Python packages
- `requirements.txt` present in the project root

## Setup (Linux / macOS / Windows with Conda)
1. Create a conda environment with Python 3.10 named `app`:
```bash
conda create -n app python=3.10 -y
```

2. Activate the environment:
```bash
conda activate app
```

3. Install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Run
Start the application with:
```bash
python app_main.py
```

After the server starts, open your browser and go to:
```
http://127.0.0.1:8000
```

## Troubleshooting
- If `conda` command is not found, ensure Anaconda/Miniconda is installed and added to your PATH, or open the Anaconda Prompt (Windows).
- If port `8000` is already in use, stop the other process or modify the application to use a different port.
- If a package fails to install, try upgrading `pip` first:
```bash
pip install --upgrade pip
```