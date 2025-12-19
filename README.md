# Talespin – AI Storytelling Companion

**Talespin** is a voice-first, conversational AI system that transforms spoken creative prompts into fully narrated stories. Designed for natural, hands-free interaction, Talespin bridges modern voice AI with large language models to create an immersive storytelling experience that feels less like issuing commands and more like sitting around a digital campfire.

---

## 🎯 What Talespin Does

Users speak a genre, theme, or idea (e.g., *"Tell me a sci‑fi story about a robot learning to paint"*).

Talespin:

* Interprets the spoken prompt
* Generates a unique, context-aware story using a large language model
* Performs the story aloud using natural voice synthesis
* Maintains conversational continuity when desired

The experience is fully voice-driven — no keyboard, no UI friction.

---

## 🧠 Why This Project Exists

Most AI storytelling tools are text-based and transactional. Talespin was built to explore a different interaction model:

* **Voice-first UX** instead of text prompts
* **Conversational continuity** rather than one-off responses
* **Narrative performance**, not just text generation

The project was created during the ElevenLabs Hackathon to push the boundaries of voice-native AI systems.

---

## 🏗️ System Architecture

Talespin integrates two powerful but incompatible AI platforms using a custom translation layer.

```
User Voice
   ↓
ElevenLabs Conversational Agent
   ↓ (OpenAI-style request)
Cloud Run Proxy (Python / Flask)
   ↓ (Schema translation)
Google Gemini API
   ↓ (Generated story)
Cloud Run Proxy
   ↓ (OpenAI-style response)
ElevenLabs Text-to-Speech
   ↓
Spoken Story
```

### Core Components

#### 1. ElevenLabs Conversational Agent

* Handles voice input and output
* Manages conversational flow
* Expects OpenAI-compatible `/v1/chat/completions` responses

#### 2. Voice-Optimized Cloud Run Proxy

A Python Flask service deployed on **Google Cloud Run** that:

* Implements an ElevenLabs-compatible OpenAI-style API
* Translates requests to the Google Gemini API schema
* Applies voice-optimized prompting and style detection
* Streams responses for natural spoken delivery
* Manages session-based story continuity

#### 3. Google Gemini API

* Generates creative, long-form narrative content
* Provides scalable, high-quality language generation

---

## 🔧 Technical Stack

* **Language:** Python
* **Framework:** Flask
* **Cloud Platform:** Google Cloud Platform
* **Compute:** Cloud Run (serverless containers)
* **AI Models:** Google Gemini API
* **Voice AI:** ElevenLabs Conversational Agent + TTS
* **Logging & Monitoring:** Google Cloud Logging

---

## ⚙️ Key Engineering Decisions & Tradeoffs

* **Serverless Cloud Run vs Kubernetes**
  Chosen for rapid iteration and automatic scaling, accepting cold-start latency and reduced infrastructure control.

* **Custom Proxy vs Direct Integration**
  A translation layer was required due to incompatible API schemas, trading simplicity for interoperability and flexibility.

* **Stateless Services with External Session Tracking**
  Improves scalability but increases coordination complexity.

* **Voice-Optimized Prompting**
  Improves narrative flow at the cost of longer prompt engineering cycles.

---

## 🚧 Challenges & Debugging Journey

This project was defined by real-world cloud debugging rather than greenfield development.

### Major Challenges

* **Container Crash Loops**
  The proxy service initially crashed hundreds of times due to a missing Python dependency (`requests`), highlighting the precision required in container dependency management.

* **API Schema Incompatibility**
  ElevenLabs expects OpenAI-style schemas, while Gemini uses a fundamentally different structure. Silent failures required extensive log analysis to resolve.

* **Security Exposure**
  API keys were inadvertently logged during early iterations. Logging was redesigned to redact sensitive data, turning a vulnerability into a hardened best practice.

* **Health Check Failures**
  Containers failed startup probes when exiting before binding to port 8080, requiring careful tracing of lifecycle execution order.

---

## 🏆 What Was Accomplished

* Built a production-ready translation layer between ElevenLabs and Google Gemini
* Deployed a fully operational, voice-driven AI system
* Diagnosed and resolved over **1,200+ logged operational errors**
* Implemented secure configuration and logging practices
* Designed a narrative system optimized for spoken delivery

---

## 📚 What I Learned

* Logs are the single source of truth in distributed systems
* AI services are rarely plug-and-play; interoperability is an engineering problem
* Voice UX requires different design assumptions than text interfaces
* Serverless systems demand strict dependency and lifecycle discipline

---

## 🚀 Future Enhancements

* Web interface for browsing and sharing stories
* Multi-character narration using multiple voices
* Interactive, branching narratives
* Genre-specialized storytelling modes
* Long-term narrative memory across sessions
* Educational storytelling with age-appropriate controls

---

## 🔗 Live Deployment

* **Cloud Run Service:** [https://elevenlabs-proxy-549067698528.us-central1.run.app](https://elevenlabs-proxy-549067698528.us-central1.run.app)

---

## 🧪 Status

✅ Successfully deployed and operational

---

## 🧩 Innovation Highlight

**Custom API Translation Layer** enabling seamless interoperability between ElevenLabs (OpenAI-style API) and Google Gemini — two systems not designed to work together.

---

*Built as part of the ElevenLabs Hackathon.*
