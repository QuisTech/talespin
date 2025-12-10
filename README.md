# Talespin - AI Storytelling Companion

## Live Demo
**Click to talk to Talespin:** https://elevenlabs.io/app/talk-to?agent_id=agent_0301kc257s73ejxr3taxqgccddyt

## Architecture


User Voice → ElevenLabs Agent → Talespin Proxy → Google Gemini API → ElevenLabs TTS → User Hears Story




## Agent Configuration
- **Server URL:** https://elevenlabs-proxy-549067698528.us-central1.run.app/v1/chat/completions
- **Model ID:** google-gemini
- **Temperature:** 0.8

## Setup & Deployment
1. Deploy to Google Cloud Run:
```bash
gcloud run deploy talespin --source . --allow-unauthenticated




Configure ElevenLabs Agent with your deployed URL

Files
main.py - Flask proxy with streaming support

requirements.txt - Python dependencies

Procfile - Cloud Run configuration