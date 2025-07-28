# modules/semantic_ranker.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_sections(sections, persona, job, top_k=None):
    texts = [f"{s['section_title']}" for s in sections]
    query = [f"{persona} {job}"]
    # Multilingual support: do not use English-only stopwords
    vectorizer = TfidfVectorizer(max_features=10000, stop_words=None)
    docs = vectorizer.fit_transform(texts + query)
    sims = cosine_similarity(docs[-1], docs[:-1])[0]
    ranked = sorted(
        [{"score": float(s), **sections[i]} for i, s in enumerate(sims)],
        key=lambda x: -x["score"]
    )
    for rank, item in enumerate(ranked, 1):
        item["importance_rank"] = rank
    return (ranked[:top_k] if top_k else ranked)
