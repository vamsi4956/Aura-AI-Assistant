import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import os

# Set cache folder to avoid permission errors on Render
os.environ['SENTENCE_TRANSFORMERS_HOME'] = './.cache'

# Load the model (We keep your same high-accuracy model!)
model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

knowledge_base = {
    "What is the time?": "The system clock is currently being synchronized.",
    "Who created you?": "I was created by Vamsi as a personal Home AI assistant.",
    "Tell me about ANITS": "ANITS is a top engineering college in Visakhapatnam where I was born!",
    "What is Python?": "Python is the high-level language used to build my brain.",
    "Turn on the lights": "Smart lighting system activated.",
    "Is the house secure?": "Perimeter scan complete. All locks are engaged."
}

questions = list(knowledge_base.keys())
# We pre-calculate these so the app starts faster
question_embeddings = model.encode(questions)

def get_response(user_input):
    # 1. Vectorize user input
    user_embedding = model.encode([user_input])
    
    # 2. Compute Cosine Similarity using NumPy (lighter than Torch)
    similarities = cosine_similarity(user_embedding, question_embeddings).flatten()
    
    # 3. Find the best match
    best_match_idx = np.argmax(similarities)
    max_score = similarities[best_match_idx]

    # Threshold for accuracy
    if max_score > 0.5:
        return knowledge_base[questions[best_match_idx]]
    
    return "I'm analyzing that home command. Can you rephrase it?"
