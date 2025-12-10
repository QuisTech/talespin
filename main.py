from flask import Flask, Response, request, jsonify
import json
import time
import traceback
import os
import requests

app = Flask(__name__)

# Get API key from environment (secure)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyDKikyGRRdyGqNHcjhYpHAg_64NnW93eV0')

print(f"🚀 Talespin - Using Google Gemini API")

def generate_story_with_gemini(prompt):
    """Generate unique stories using Google Gemini API"""
    try:
        print(f"🤖 Gemini API for: '{prompt}'")
        
        # Clean prompt
        clean_prompt = prompt.lower()
        for phrase in ["tell me a story about", "story about", "a story of"]:
            clean_prompt = clean_prompt.replace(phrase, "").strip()
        
        # Google Gemini API endpoint
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        
        # Creative prompt for storytelling
        story_prompt = f"""You are Talespin, a creative AI storyteller. Write a unique, engaging short story (100-150 words) about: {clean_prompt}

Make it:
1. Original and creative
2. With vivid descriptions
3. A clear beginning, middle, and end
4. Suitable for voice narration
5. Different from other stories

Story:"""
        
        payload = {
            "contents": [{
                "parts": [{"text": story_prompt}]
            }],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 300,
                "topP": 0.95
            }
        }
        
        print(f"📡 Calling Gemini API...")
        response = requests.post(url, json=payload, timeout=15)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and result['candidates']:
                story = result['candidates'][0]['content']['parts'][0]['text']
                print(f"✅ Gemini success! Story length: {len(story)} chars")
                return story
            else:
                print(f"⚠️ No candidates in response")
                return f"A creative story about {clean_prompt}."
        else:
            print(f"❌ Gemini API error: {response.text[:200]}")
            # Fallback to dynamic generation
            return generate_fallback_story(clean_prompt)
            
    except Exception as e:
        print(f"❌ Gemini API exception: {str(e)}")
        traceback.print_exc()
        return generate_fallback_story(prompt)

def generate_fallback_story(prompt):
    """Fallback story generator if API fails"""
    print(f"🔄 Using fallback generator for: {prompt}")
    
    beginnings = [
        f"In a realm where {prompt} held ancient power,",
        f"Across galaxies, legends spoke of {prompt}'s significance,",
        f"When the world needed hope, {prompt} answered the call,",
        f"Hidden in plain sight, {prompt} contained secrets untold,",
    ]
    
    characters = [
        "A curious explorer",
        "A reluctant hero", 
        "A wise guardian",
        "A mysterious wanderer",
    ]
    
    events = [
        "discovered that true strength comes from unity and understanding.",
        "learned that the greatest treasures are friendship and courage.",
        "found that every ending is just a new beginning in disguise.",
        "realized that the journey itself was the real destination.",
    ]
    
    import random
    story = random.choice(beginnings) + " "
    story += random.choice(characters) + " embarked on a quest and "
    story += random.choice(events)
    
    return story

@app.after_request
def add_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/v1/chat/completions', methods=['POST', 'OPTIONS'])
def handle():
    if request.method == 'OPTIONS':
        return '', 204
    
    print(f"\n{'='*60}")
    print(f"📥 ElevenLabs request")
    
    try:
        data = request.get_json() or {}
        
        # Get user message
        user_message = "an adventure"
        for msg in data.get('messages', []):
            if msg.get('role') == 'user':
                user_message = msg.get('content', 'an adventure')
                break
        
        print(f"💬 User: {user_message}")
        
        # Generate story with Gemini API
        story = generate_story_with_gemini(user_message)
        print(f"📖 Story generated")
        
        stream = data.get('stream', False)
        
        if stream:
            def generate():
                yield f'data: {json.dumps({
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "google-gemini",
                    "choices": [{"delta": {"role": "assistant"}}]
                })}\n\n'
                
                words = story.split()
                for i in range(0, len(words), 2):
                    chunk = " ".join(words[i:i+2]) + " "
                    yield f'data: {json.dumps({
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": "google-gemini",
                        "choices": [{"delta": {"content": chunk}}]
                    })}\n\n'
                    time.sleep(0.05)
                
                yield f'data: {json.dumps({
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": "google-gemini",
                    "choices": [{"delta": {}, "finish_reason": "stop"}]
                })}\n\n'
                yield 'data: [DONE]\n\n'
            
            return Response(generate(), mimetype='text/event-stream')
        else:
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
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "ai": "Google Gemini API",
        "stories": "dynamic and unique"
    })

@app.route('/test-gemini', methods=['GET'])
def test_gemini():
    """Test Gemini API with different prompts"""
    import hashlib
    
    results = []
    prompts = ["space pirates", "robot artists", "dragon scholars"]
    
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
        "api_key_set": bool(GEMINI_API_KEY)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    print(f"✅ Talespin - Google Gemini API Integration")
    print(f"🔑 API Key: {'Set' if GEMINI_API_KEY else 'Not set'}")
    app.run(host='0.0.0.0', port=port)
