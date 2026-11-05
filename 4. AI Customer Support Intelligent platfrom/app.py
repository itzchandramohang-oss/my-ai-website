from __future__ import annotations

import os
import re
from datetime import datetime, timezone

from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

submissions = []

KNOWLEDGE_BASE = {
    'about': 'We are building an AI-powered customer support platform to help teams make everyday support tasks easier and more enjoyable. The assistant can answer common customer questions and help support teams respond faster.',
    'services': 'Our services include AI-powered answers to common support questions, ticket summarization, routing high-priority issues, and integrations with support and business tools. The exact service details and availability can be discussed through the contact form.',
    'pricing': 'Our starter plan begins at $49/month, the growth plan is $149/month, and enterprise pricing is custom for larger teams.',
    'plan': 'We offer a starter, growth, and enterprise plan. The starter plan is ideal for small teams, while enterprise includes custom onboarding and priority support.',
    'cost': 'Costs depend on the number of support agents and AI workflows you need. Most small businesses start with the starter plan at $49/month.',
    'support': 'We provide email support for all plans and live chat support for growth and enterprise customers. Enterprise clients also receive a dedicated success manager.',
    'hours': 'Support is available Monday through Friday from 8 AM to 8 PM EST. Enterprise clients receive extended coverage and faster response times.',
    'integration': 'Our platform connects with popular tools like Slack, Zendesk, HubSpot, Salesforce, Shopify, and custom REST APIs.',
    'onboarding': 'Typical onboarding takes 1 to 2 weeks depending on your data source and team setup. We offer guided implementation for faster launch.',
    'setup': 'Setup usually includes connecting your knowledge base, support channels, and team workflows. We can start with a pilot in under a week.',
    'demo': 'You can request a personalized demo by using the contact form or emailing hello@example.com.',
    'ai': 'Our AI customer support assistant helps answer common questions, summarize tickets, route issues, and improve response quality across your support team.',
}


@app.get('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Website backend is running',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    })


@app.get('/api/messages')
def list_messages():
    return jsonify({
        'count': len(submissions),
        'submissions': submissions,
    })


@app.post('/api/contact')
def contact():
    data = request.get_json(silent=True) or {}
    name = str(data.get('name', '')).strip()
    email = str(data.get('email', '')).strip()
    message = str(data.get('message', '')).strip()

    if not name or not email or not message:
        return jsonify({
            'success': False,
            'message': 'Name, email, and message are required.',
        }), 400

    submission = {
        'id': len(submissions) + 1,
        'name': name,
        'email': email,
        'message': message,
        'createdAt': datetime.now(timezone.utc).isoformat(),
    }
    submissions.append(submission)

    return jsonify({
        'success': True,
        'message': 'Thanks! Your message has been received.',
        'submission': submission,
    })


@app.post('/api/ai/chat')
def ai_chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get('message', '')).strip()

    if not user_message:
        return jsonify({
            'success': False,
            'answer': 'Please ask a question about pricing, setup, integrations, or support.',
        }), 400

    normalized = re.sub(r'[^a-z0-9\s]', ' ', user_message.lower())
    matched_key = None

    intent_phrases = {
        'about': [
            'about us', 'about your company', 'your company', 'your story',
            'who are you', 'what do you do',
        ],
        'services': [
            'service', 'services', 'what do you offer', 'what can you do',
            'features', 'your product',
        ],
        'pricing': ['price', 'cost', 'plan', 'monthly', 'pricing'],
        'support': ['support', 'help', 'ticket', 'customer service'],
        'integration': ['integration', 'connect', 'slack', 'zendesk', 'salesforce', 'shopify'],
        'onboarding': ['setup', 'onboard', 'implementation', 'launch'],
        'ai': ['ai', 'assistant', 'automation', 'chatbot'],
    }

    words = set(normalized.split())
    for key, phrases in intent_phrases.items():
        if any(
            phrase in normalized if ' ' in phrase else phrase in words
            for phrase in phrases
        ):
            matched_key = key
            break

    answer = KNOWLEDGE_BASE.get(matched_key, 'Our AI support assistant can help with pricing, onboarding, integrations, and customer support. Please ask a specific question or use the contact form for a detailed conversation.')

    return jsonify({
        'success': True,
        'answer': answer,
        'intent': matched_key or 'general',
        'timestamp': datetime.now(timezone.utc).isoformat(),
    })


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_site(path):
    full_path = os.path.join(app.static_folder, path)

    if os.path.isdir(full_path):
        return send_from_directory(app.static_folder, os.path.join(path, 'index.html'))

    if os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)

    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
