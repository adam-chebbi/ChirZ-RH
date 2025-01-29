from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

nlp = spacy.load('en_core_web_sm')

def extract_keywords(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return set(tokens)

def match_cv_with_jd(cv, jd):
    cv_text = extract_keywords(cv.filename)  # Simplified, should extract from PDF/Word content
    jd_text = extract_keywords(jd.text)

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([' '.join(cv_text), ' '.join(jd_text)])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    matched_skills = ', '.join(cv_text & jd_text)
    unmatched_skills = ', '.join(cv_text - jd_text)

    result = MatchResult(cv_id=cv.id, jd_id=jd.id, match_score=similarity,
                         matched_skills=matched_skills, unmatched_skills=unmatched_skills)
    return result