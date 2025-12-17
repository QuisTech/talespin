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










Based on your comprehensive project journey, here's a complete project story for your hackathon submission:

# **Talespin: The AI Storytelling Companion**

## **🎭 Inspiration**
The magic of storytelling is universal, but not everyone feels like a storyteller. As someone who believes in the power of narrative to connect, inspire, and entertain, I wanted to build a bridge between human imagination and AI creativity. The ElevenLabs hackathon presented the perfect challenge: to make this experience **conversational, accessible, and entirely voice-driven**. I envisioned more than just a text generator—I wanted to create a digital campfire companion that could perform stories with personality, adapting to any genre or mood the user desires. Talespin is that companion: an AI that doesn't just generate text, but brings stories to life through voice.

## **✨ What it does**
Talespin is a voice-driven AI storytelling companion that transforms creative prompts into narrated tales. Users simply speak a genre, theme, or story idea ("Tell me a sci-fi story about a robot learning to paint"), and Talespin responds with a unique, generated story performed through natural voice synthesis. The experience is entirely conversational—no typing, no buttons, just voice. 

The system intelligently adapts to user requests, maintaining narrative continuity across sessions if desired, and can shift tone from whimsical fairy tales to gritty noir mysteries based on the user's prompt. It's like having a creative collaborator who can spin yarns on demand, perfect for bedtime stories, creative brainstorming, or simply passing time with an engaging narrative.

## **⚙️ How we built it**
Talespin is built on a sophisticated serverless architecture that bridges two powerful but incompatible AI platforms:

```
User's Voice → [ElevenLabs Agent] → OpenAI-format Request → [Custom Proxy on Google Cloud Run]
                                                                         ↓
                   Request Translation & API Call → [Google Gemini Public API (generativelanguage.googleapis.com)]
                                                                         ↓
    Spoken Story ← [ElevenLabs TTS] ← OpenAI-format Response ← [Reformatted Response]
```

**Core Components:**

1. **ElevenLabs Conversational Agent**: Configured as "Talespin" to handle voice input/output and manage the conversational flow with our backend API.

2. **Voice-Optimized Cloud Run Proxy**: Deployed on Google Cloud Run, this Python Flask application (`main.py`) is the intelligent heart of the system. It:
   - Provides a perfect ElevenLabs-compatible `/v1/chat/completions` endpoint.
   - Translates user prompts into **voice-optimized requests** (with smart style detection: storyteller, adventure, mystery, comedy).
   - Calls the **Google Gemini API** (`generativelanguage.googleapis.com`) securely using an API key for story generation.
   - Manages conversation sessions for story continuity and streams responses for natural spoken delivery.

3. **Google Gemini API**: Served as the powerful, scalable language model that generates creative stories based on our voice-optimized prompts.

4. **Cloud Infrastructure**: All components are deployed on Google Cloud Platform with proper environment configuration, logging, and monitoring on Cloud Run.

**The path to this stable architecture was intensely iterative. Each component was refined through cycles of deployment, analyzing failure logs from Google Cloud, and fixing issues ranging from missing dependencies to API schema mismatches.**

##**🚧 Challenges we ran into**

The development journey was a masterclass in cloud-native debugging, defined by systematically overcoming a barrage of operational failures:

1.  **The Cascade of Container Crashes:** The initial proxy service **crashed over 250 times**. The root cause? A single, missing Python module (`requests`). This taught us a hard lesson about the absolute precision required in container dependency management for serverless deployments.
**2. Silent API Schema Warfare:** The core challenge was the fundamental incompatibility between ElevenLabs (OpenAI format) and **Google's Gemini API**. This wasn't a clean error but a silent killer, manifesting as over 352 generic Python exceptions in the logs. Days of methodical schema archaeology were needed to build a perfect translation layer between the two different API structures.
3.  **Security in Plain Sight:** During log analysis, we discovered **65 instances of API keys being inadvertently logged**. This critical security exposure was immediately rectified, leading to the implementation of a robust logging policy that redacts sensitive data, turning a major risk into a best practice.
4.  **The Health Check Deadlock:** Our service was stuck in a deployment loop, failing **18 consecutive startup health checks**. The logs revealed the container was dying (`exit(1)`) before it could even listen on port 8080, directly linking this infrastructure failure back to the missing `requests` dependency.
5.  **Solo Developer Triage:** Balancing this intense, data-driven firefight with hackathon timelines meant making constant triage decisions. The focus had to remain on stabilizing the core translation pipe before adding features.

**🏆 Accomplishments that we're proud of**

*   **Conquering the Log Mountain:** Successfully diagnosing and categorizing **1,202 operational events** from raw, massive cloud logs to isolate and fix critical issues in dependency management, API design, and security.
*   **Successfully Bridging Incompatible Giants:** Creating a seamless translation layer between ElevenLabs and **Google's Gemini API**—two platforms never designed to work together.
*   **Designing a Voice-Optimized Architecture:** Engineering a system that smartly detects narrative style (storyteller, adventure, mystery, comedy) and adapts story tone, pacing, and structure for perfect spoken delivery.
*   **Full End-to-End Deployment:** Having a completely operational system following resolution of critical deployment challenges.
*   **Robust Error Handling and Logging:** Implementing comprehensive logging that helped debug issues in real-time across multiple cloud services.
*   **Creating a Truly Conversational Experience:** The system doesn't just generate text—it performs stories with personality, adapting to user input in real-time.

## **📚 What we learned**

This project was a masterclass in cloud-native AI integration and **evidence-based development**:

*   **Logs are the Single Source of Truth:** Systematic log analysis is non-negotiable. Manually sifting through 225,000 lines of JSON to categorize 1,200+ errors was the only way to move from generic failure messages to root causes like schema mismatches, missing dependencies, and health check misconfigurations.

*   **Technical Insights:**
    *   **Cloud Service Interoperability:** Cutting-edge AI services often have incompatible interfaces—success comes from building intelligent translation layers rather than expecting plug-and-play compatibility.
    *   **GCP IAM Mastery:** Proper service account and environment configuration is critical for serverless deployments on Cloud Run.
    *   **API Schema Archaeology:** Deep understanding of both **ElevenLabs' expected OpenAI schema and Google's Gemini API schema** was essential for building the translation layer.

*   **Development Lessons:**
    *   **The Power of Constraints:** Working within hackathon timelines forced elegant, minimal solutions rather than over-engineering.
    *   **Voice UX is Different:** Designing for voice interaction requires different considerations than text-based interfaces.

## **🚀 What's next for Talespin**
With the core architecture solidly built, Talespin could evolve in exciting directions:

1. **Web Interface**: A simple frontend where users can browse previous stories, save favorites, and share creations.

2. **Multi-Character Dialogues**: Different ElevenLabs voices for different characters within the same story.

3. **Interactive Storytelling**: Branching narratives where users can make choices that affect the plot.

4. **Genre Specialization**: Fine-tuned models for specific genres (fantasy, mystery, sci-fi) with genre-appropriate vocabulary and tropes.

5. **Educational Mode**: Stories that teach concepts through narrative, with age-appropriate content controls.

6. **Community Features**: A platform where users can share their favorite Talespin creations and even "remix" each other's story prompts.

7. **Advanced Continuity**: Long-form narrative memory that can maintain character development and plot arcs across multiple sessions.

The foundation is built—now the stories can truly begin. Talespin represents not just a hackathon project, but a new way for people to interact with AI: not through commands or queries, but through the timeless human tradition of storytelling.

---

**Technical Stack:** Google Cloud Platform (Cloud Run), Google Gemini API, ElevenLabs Voice AI, Python/Flask

**Deployment Status:** Successfully deployed and operational at `https://elevenlabs-proxy-549067698528.us-central1.run.app`

**Innovation:** Custom API translation layer enabling ElevenLabs ↔ Google Gemini AI integration
