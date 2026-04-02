from sentence_transformers import SentenceTransformer, util
import torch

# Load a tiny but powerful model (Only ~80MB)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Your "Brain" - The more examples you add, the smarter it gets
knowledge_base = {
    "What is the time?": "The current time is available in the system tray.",
    "Who created you?": "I was created by Vamsi as a personal AI assistant.",
    "Tell me about ANITS": "ANITS is a top engineering college in Visakhapatnam.",
    "What is Python?": "Python is a high-level programming language for AI."
}

questions = list(knowledge_base.keys())
question_embeddings = model.encode(questions, convert_to_tensor=True)

def get_response(user_input):
    # Encode user input
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    
    # Compute similarity scores
    cos_scores = util.cos_sim(user_embedding, question_embeddings)[0]
    
    # Find the best match
    best_match_idx = torch.argmax(cos_scores).item()
    max_score = cos_scores[best_match_idx].item()

    # Accuracy Threshold: If the match is better than 50%
    if max_score > 0.5:
        return knowledge_base[questions[best_match_idx]]
    
    return "I'm not 100% sure, but I'm learning more every day!"
