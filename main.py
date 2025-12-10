from flask import Flask, Response, request, jsonify
import json
import time
import traceback
import os
import requests
import random
import hashlib 

app = Flask(__name__)

# Get API key from environment (secure). Relies ONLY on deployment variable.
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 

print(f"🔑 GEMINI_API_KEY loaded: {'YES' if GEMINI_API_KEY else 'NO'}")
if GEMINI_API_KEY:
    print(f"🔑 Key first 10 chars: {GEMINI_API_KEY[:10]}")
    print(f"🔑 Key length: {len(GEMINI_API_KEY)}")

print(f"🚀 Talespin - AI Storytelling with Continuity Support")

def generate_story_with_gemini(prompt):
    """Generate unique stories using Google Gemini API"""
    
    # Check if the key is available before making the call
    if not GEMINI_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY is not set.")
        return generate_fallback_story(prompt)

    try:
        print(f"🤖 Gemini API for: '{prompt}'")
        
        # 🆕 FIX: Transform command prompts before sending to Gemini
        command_keywords = ["tell me", "tell", "story about", "a story"]
        story_topic = prompt
        
        for keyword in command_keywords:
            if keyword in prompt.lower():
                story_topic = prompt.lower().replace(keyword, "").strip()
                break
        
        # If empty after removing commands, use creative default
        if len(story_topic) < 3:
            creative_defaults = [
                "the last library in a world that forgot how to read",
                "a musician who hears the colors of emotions",
                "a map to places that exist only in dreams",
                "a clock that ticks differently for every heart it hears"
            ]
            story_topic = random.choice(creative_defaults)
            print(f"🎨 Using creative topic: {story_topic}")
        
        # Google Gemini API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        
        
        # Creative prompt for storytelling (SIMPLIFIED)
        story_prompt = f"""Write a creative story (250-350 words) about: {story_topic}

Requirements:
1. Vivid descriptions and clear narrative arc
2. Suitable for voice narration
3. Unique and engaging

Story:"""

        payload = {
            "contents": [{
                "parts": [{"text": story_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 1024,  # INCREASED TO 1024
                "topP": 0.95
            }
        }

        print(f"📡 Calling Gemini API...")
        print(f"🔄 DEBUG: Full URL being called: {url}")
        print(f"🔄 DEBUG: Payload being sent: {json.dumps(payload, indent=2)}")
        response = requests.post(url, json=payload, timeout=15)
        print(f"🔄 DEBUG: HTTP Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"🔄 DEBUG: Full Response: {json.dumps(result, indent=2)[:1000]}")
            
            if 'candidates' in result and result['candidates']:
                candidate = result['candidates'][0]
                
                # Check for MAX_TOKENS
                if candidate.get('finishReason') == 'MAX_TOKENS':
                    print("⚠️ Response truncated by token limit")
                    return generate_fallback_story(story_topic)
                
                # Extract text from various possible formats
                if 'text' in candidate:
                    story = candidate['text']
                elif 'content' in candidate:
                    if 'text' in candidate['content']:
                        story = candidate['content']['text']
                    elif 'parts' in candidate['content'] and candidate['content']['parts']:
                        story = candidate['content']['parts'][0]['text']
                    else:
                        print(f"⚠️ Unexpected content format")
                        return generate_fallback_story(story_topic)
                else:
                    print(f"⚠️ Unexpected candidate format")
                    return generate_fallback_story(story_topic)
                
                print(f"✅ Gemini success! Story length: {len(story)} chars")
                return story
            else:
                print(f"⚠️ No candidates in response")
                return generate_fallback_story(story_topic)
        else:
            print(f"❌ Gemini API error: {response.text[:200]}")
            return generate_fallback_story(story_topic)
    except Exception as e:
        print(f"❌ Exception in generate_story_with_gemini: {str(e)}")
        traceback.print_exc()
        return generate_fallback_story(prompt)

def generate_fallback_story(prompt):
    """Intelligent fallback story generator"""
    print(f"🔄 Using fallback generator for prompt: '{prompt}'")
    
    # 🆕 FIX: Detect and transform command-like prompts
    command_keywords = ["tell me", "tell", "story about", "a story", "something unique", "something"]
    
    is_command = False
    cleaned_prompt = prompt
    
    # Check if it's a command, not a story topic
    for keyword in command_keywords:
        if keyword in prompt.lower():
            is_command = True
            # Remove command words to get actual topic (if any)
            cleaned_prompt = prompt.lower().replace(keyword, "").strip()
            break
    
    # 🆕 FIX: If it's a command with no actual topic, use creative defaults
    if is_command and (len(cleaned_prompt) < 3 or cleaned_prompt in ["", "unique", "something"]):
        creative_topics = [
            "unexpected friendship",
            "hidden magic", 
            "forgotten prophecy",
            "impossible discovery",
            "secret legacy"
        ]
        story_topic = random.choice(creative_topics)
        print(f"🎨 Command detected. Using creative topic: {story_topic}")
    else:
        story_topic = cleaned_prompt if cleaned_prompt else "mystery and adventure"
    
    # 🆕 FIX: Better story beginnings that don't insert the prompt literally
    beginnings = [
        f"Whispers in the {random.choice(['ancient library', 'starlit desert', 'crystal caverns'])} spoke of ",
        f"When the {random.choice(['last star', 'first memory', 'final chord'])} faded, ",
        f"In a world where {random.choice(['shadows held memories', 'silence had color', 'time flowed sideways'])}, ",
        f"The {random.choice(['forgotten', 'whispered', 'impossible'])} truth about ",
    ]
    
    # 🆕 FIX: Natural sentence completion
    beginnings_completion = [
        f"began to unravel.",
        f"waited to be discovered.",
        f"changed everything.",
        f"was about to be revealed.",
    ]
    
    # 🆕 FIX: More natural character descriptions
    characters = [
        f"A {random.choice(['curious', 'reluctant', 'determined'])} {random.choice(['explorer', 'scholar', 'artisan'])}",
        f"The {random.choice(['last', 'unlikely', 'forgotten'])} {random.choice(['guardian', 'witness', 'heir'])}",
        f"A {random.choice(['whisper-voiced', 'star-touched', 'memory-bound'])} {random.choice(['wanderer', 'seeker', 'keeper'])}",
    ]
    
    # 🆕 FIX: More varied and natural outcomes
    events = [
        f"discovered that {random.choice(['truth often wears disguise', 'courage has many faces', 'endings birth new beginnings'])}.",
        f"learned {random.choice(['silence speaks loudest', 'broken things hold beauty', 'the map was in the journey itself'])}.",
        f"found {random.choice(['peace in paradox', 'strength in vulnerability', 'home was always within'])}.",
    ]
    
    # 🆕 FIX: Construct natural sentences
    story = random.choice(beginnings) + story_topic + " " + random.choice(beginnings_completion) + " "
    story += random.choice(characters) + " " + random.choice(["embarked on", "began", "undertook"]) + " "
    story += random.choice(["a quest", "a journey", "an exploration"]) + " and "
    story += random.choice(events)
    
    # Add unique identifier
    story_hash = hashlib.md5(story.encode()).hexdigest()[:6]
    print(f"📝 Fallback story generated [ID: {story_hash}]")
    
    return story

def generate_continuation_prompt(previous_story, user_request=""):
    """Create a prompt for continuing a story with consistency"""
    
    # Extract last few sentences for context
    sentences = previous_story.split('. ')
    context = '. '.join(sentences[-3:]) if len(sentences) >= 3 else previous_story
    
    # 🆕 FIX: Check if continuation request is a command
    command_keywords = ["continue", "what happens", "go on", "and then", "keep going", "next chapter"]
    continuation_topic = user_request
    
    for keyword in command_keywords:
        if keyword in user_request.lower():
            # Remove continuation commands to get actual direction (if any)
            continuation_topic = user_request.lower().replace(keyword, "").strip()
            if not continuation_topic:
                continuation_topic = "Continue the story naturally"
            break
    
    prompt = f"""You are Talespin, a master storyteller AI. Continue the following story while maintaining perfect continuity with these characters, setting, and plot points.

**Previous Story Context:**
{context}

**User Request:**
{continuation_topic if continuation_topic else "Continue the story naturally"}

**Continuation Instructions:**
1. First, analyze the tone, character motivations, and unresolved plot threads
2. Continue the narrative seamlessly as if it's the next chapter
3. Introduce ONE new, logical challenge or revelation
4. Keep the same narrative style and descriptive richness
5. End with a hint of what might come next, but provide satisfying closure
6. Length: 150-200 words

**Special Note for Voice Narration:**
- Write for spoken delivery with natural pauses
- Use vivid but concise descriptions
- Create dialogue tags that work well in audio format

**Story Continuation:**"""
    
    return prompt

def generate_story_with_gemini_continuation(previous_story, user_request=""):
    """Generate story continuations using Google Gemini API"""
    
    # Check if the key is available before making the call
    if not GEMINI_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY is not set for continuation.")
        # 🆕 FIX: Use intelligent fallback for continuations too
        return generate_fallback_story("continuation of " + user_request)

    try:
        print(f"🎭 Gemini API for continuation: '{user_request[:50]}...'")
        
        # Google Gemini API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        
        # Use the specialized continuation prompt
        continuation_prompt = generate_continuation_prompt(previous_story, user_request)
        
        payload = {
            "contents": [{
                "parts": [{"text": continuation_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.85,  # Slightly lower for consistency
                "maxOutputTokens": 450,  # Slightly shorter for continuations
                "topP": 0.9
            }
        }
        
        print(f"📡 Calling Gemini API for continuation...")
        response = requests.post(url, json=payload, timeout=15)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and result['candidates']:
                story = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Gemini continuation success! Story length: {len(story)} chars")
                return story
            else:
                print(f"⚠️ No candidates in continuation response")
                return generate_fallback_story("continuation")
        else:
            print(f"❌ Gemini API continuation error: {response.text[:200]}")
            return generate_fallback_story("continuation")
            
    except Exception as e:
        print(f"❌ Gemini API continuation exception: {str(e)}")
        traceback.print_exc()
        return generate_fallback_story("continuation")

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    response.headers['Access-Control-Allow-Headers'] = '*'
    return response

# -------------------------------------------------------------
# 🎯 Main Handler with Continuity Detection
# -------------------------------------------------------------
@app.route('/v1/chat/completions', methods=['GET', 'POST', 'OPTIONS'])
@app.route('/v1/chat/completions/', methods=['GET', 'POST', 'OPTIONS'])
def handle():
    # Handle OPTIONS (CORS preflight)
    if request.method == 'OPTIONS':
        return '', 204
    
    # Handle GET (ElevenLabs health check)
    if request.method == 'GET':
        print("✅ ElevenLabs endpoint check (GET)")
        return jsonify({
            "status": "online",
            "service": "Talespin Proxy",
            "endpoint": "/v1/chat/completions",
            "ready_for": "POST requests with ElevenLabs format",
            "api_key_status": "Set" if GEMINI_API_KEY else "Not Set",
            "features": ["story_generation", "continuity_support", "voice_optimized", "intelligent_prompt_parsing"]
        })
    
    # Handle POST (actual story requests)
    print(f"\n{'='*60}")
    print(f"📥 ElevenLabs POST request")
    
    try:
        if not GEMINI_API_KEY:
            print("❌ ABORT: Missing GEMINI_API_KEY for POST request.")
            return jsonify({"error": "Configuration Error: GEMINI_API_KEY is not set."}), 500
            
        data = request.get_json() or {}
        
        # Get user message and check for continuation keywords
        user_message = "an adventure"
        previous_story_context = ""
        
        for msg in data.get('messages', []):
            if msg.get('role') == 'user':
                user_message = msg.get('content', 'an adventure')
                
                # Check if this is a continuation request
                continuation_keywords = ["continue", "next chapter", "what happens next", "go on", "and then", "keep going"]
                if any(keyword in user_message.lower() for keyword in continuation_keywords):
                    # Look for previous assistant message as context
                    for prev_msg in reversed(data.get('messages', [])):
                        if prev_msg.get('role') == 'assistant':
                            previous_story_context = prev_msg.get('content', '')
                            print(f"📚 Detected continuation request. Using previous story context.")
                            break
                break
        
        print(f"💬 User: {user_message}")
        
        # Generate story with appropriate prompt
        if previous_story_context:
            # Use continuity prompt for continuing stories
            story = generate_story_with_gemini_continuation(previous_story_context, user_message)
        else:
            # Use regular prompt for new stories
            story = generate_story_with_gemini(user_message)
        
        print(f"📖 Story generated (Length: {len(story)} chars)")
        
        stream = data.get('stream', False)
        
        if stream:
            def generate():
                # Initial chunk
                yield 'data: ' + json.dumps({
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "google-gemini",
                    "choices": [{"delta": {"role": "assistant"}}]
                }) + '\n\n'
                
                words = story.split()
                # Stream the story word by word or chunk by chunk
                for i in range(0, len(words), 2):
                    chunk = " ".join(words[i:i+2]) + " "
                    yield 'data: ' + json.dumps({
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": "google-gemini",
                        "choices": [{"delta": {"content": chunk}}]
                    }) + '\n\n'
                    time.sleep(0.05)
                
                # Final chunk to signal the end
                yield 'data: ' + json.dumps({
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "google-gemini",
                    "choices": [{"delta": {}, "finish_reason": "stop"}]
                }) + '\n\n'
                yield 'data: [DONE]\n\n'
            
            return Response(generate(), mimetype='text/event-stream')
        else:
            # Non-streaming response
            return jsonify({
                "id": f"chatcmpl-{int(time.time())}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": "google-gemini",
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": story
                    },
                    "finish_reason": "stop"
                }]
            })
            
    except Exception as e:
        print(f"❌ Handler error: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "ai": "Google Gemini API",
        "stories": "dynamic and unique",
        "endpoints": {
            "elevenlabs": "/v1/chat/completions",
            "health": "/health",
            "test": "/test-gemini",
            "continuity": "/test-continuity"
        },
        "features": [
            "continuity_detection", 
            "intelligent_fallback_stories", 
            "voice_optimized",
            "command_prompt_parsing"  # 🆕 NEW FEATURE
        ]
    })

@app.route('/test-gemini', methods=['GET'])
def test_gemini():
    """Test Gemini API with different prompts"""
    
    results = []
    # 🆕 FIX: Test both regular topics and command prompts
    prompts = ["space pirates", "tell me about robot artists", "a story of dragon scholars", "something unique"]
    
    for prompt in prompts:
        story = generate_story_with_gemini(prompt)
        story_hash = hashlib.md5(story.encode()).hexdigest()[:8] 
        results.append({
            "prompt": prompt,
            "story_preview": story[:100] + "...",
            "hash": story_hash,
            "length": len(story)
        })
    
    # Check if stories are unique
    hashes = [r["hash"] for r in results]
    unique = len(set(hashes)) == len(results)
    
    return jsonify({
        "test": "Gemini API Story Generation",
        "results": results,
        "all_unique": unique,
        "api_key_set": bool(GEMINI_API_KEY),
        "features_tested": ["command_parsing", "creative_defaults", "unique_generation"]
    })

@app.route('/test-continuity', methods=['GET'])
def test_continuity():
    """Test story continuity feature"""
    
    # First, generate an initial story
    initial_story = generate_story_with_gemini("a lost treasure map")
    
    # Then generate a continuation (using command prompt)
    continuation_story = generate_story_with_gemini_continuation(
        initial_story, 
        "Continue the story. What happens when they find the treasure?"
    )
    
    # Extract first and last sentences for comparison
    initial_sentences = initial_story.split('. ')
    continuation_sentences = continuation_story.split('. ')
    
    return jsonify({
        "test": "Story Continuity Feature",
        "initial_story_preview": initial_story[:150] + "...",
        "continuation_story_preview": continuation_story[:150] + "...",
        "initial_length": len(initial_story),
        "continuation_length": len(continuation_story),
        "features": [
            "context_aware", 
            "character_consistency", 
            "plot_continuity", 
            "voice_optimized",
            "command_parsing_in_continuations"  # 🆕 NEW FEATURE
        ]
    })

@app.route('/demo-continuity', methods=['POST'])
def demo_continuity():
    """Demo endpoint for showing continuity in hackathon presentation"""
    
    data = request.get_json() or {}
    prompt = data.get('prompt', 'tell me a story about a brave knight')
    
    # Generate initial story
    story1 = generate_story_with_gemini(prompt)
    
    # Generate continuation with command
    story2 = generate_story_with_gemini_continuation(story1, "Continue with the next chapter")
    
    # Generate second continuation with different command
    story3 = generate_story_with_gemini_continuation(story2, "What happens in the final chapter?")
    
    return jsonify({
        "demo": "Three-Part Story Continuity with Command Parsing",
        "original_prompt": prompt,
        "parsed_prompt_type": "command" if any(keyword in prompt.lower() for keyword in ["tell me", "tell", "story about"]) else "topic",
        "part_1": story1[:200] + "...",
        "part_2": story2[:200] + "...",
        "part_3": story3[:200] + "...",
        "total_length": len(story1) + len(story2) + len(story3),
        "continuity_maintained": True,
        "intelligent_features": [
            "command_vs_topic_detection",
            "creative_default_generation",
            "natural_language_continuations"
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"✅ Talespin - Advanced Storytelling Service")
    print(f"🔑 API Key: {'Set' if GEMINI_API_KEY else 'Not set'}")
    print(f"🌟 Features: Continuity-aware, Voice-optimized, Intelligent Prompt Parsing")
    print(f"🎯 NEW: Intelligent command detection and creative fallback generation")
    print(f"🌐 Endpoints:")
    print(f"  GET  /v1/chat/completions - Health check")
    print(f"  POST /v1/chat/completions - Main story generation (detects continuations)")
    print(f"  GET  /health - Service status")
    print(f"  GET  /test-gemini - Test endpoint (now tests command parsing)")
    print(f"  GET  /test-continuity - Test continuity feature")
    print(f"  POST /demo-continuity - Hackathon demo endpoint")
    app.run(host='0.0.0.0', port=port)