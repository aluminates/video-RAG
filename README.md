# Videobot Instructions to Run: 

1) Install Python (3.10.11 or below).
2) Install ChromaDB:
   pip install chromadb // python client
   // for javascript: npm install chromadb
   // for client-server mode: chroma run --path /chroma_db_path
3) Install and set up Ollama from this link: https://ollama.com/download
4) Install llama2 by running this command: ollama run llama2 and then check http://localhost:11434/ for whether Ollama is running.
5) CD into the local directory and run: pip install -r requirements.txt for dependencies.
6) Edit the DB_PATH and DATA_PATH variables in the .env file accordingly.
7) Clone this git repository: https://github.com/Rudrabha/Wav2Lip and then replace the audio.py file.
8) Download the wav2lip_gan.pth file from this link into the checkpoints folder, if not already present: https://iiitaphyd-my.sharepoint.com/:u:/g/personal/radrabha_m_research_iiit_ac_in/EdjI7bZlgApMqsVoEUUXpLsBxqXbn5z8VTmoxp55YNDcIA?e=n9ljGW
9) Face detection pre-trained model (s3fd.pth) should be downloaded to face_detection/detection/sfd/ using this link, if not already present: https://iiitaphyd-my.sharepoint.com/:u:/g/personal/prajwal_k_research_iiit_ac_in/EZsy6qWuivtDnANIG73iHjIBjMSoojcIV0NULXV-yiuiIg?e=qTasa8
10) Edit image and Wav2Lip folder paths in front.py accordingly.
11) Once all changes are made, run the application using: streamlit run front.py

To avoid ChromaDB error ---> delete /vectorstore/ contents and run preprocess.py to vectorize your data.
