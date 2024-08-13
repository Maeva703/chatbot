import nltk
import streamlit as st
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

# Télécharger les ressources nécessaires de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Charger le fichier texte et prétraiter les données
with open('livre.txt', 'r', encoding='utf-8') as f:
    data = f.read().replace('\n', ' ')

# Tokeniser le texte en phrases
sentences = sent_tokenize(data)

# Définir une fonction pour prétraiter chaque phrase
def preprocess(sentence):
    # Tokeniser la phrase en mots
    words = word_tokenize(sentence)
    # Supprimer les stopwords et la ponctuation
    words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation]
    # Lemmatiser les mots
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Prétraiter chaque phrase dans le texte
corpus = [preprocess(sentence) for sentence in sentences]

# Définir une fonction pour trouver la phrase la plus pertinente pour une requête donnée
def get_most_relevant_sentence(query):
    # Prétraiter la requête
    query = preprocess(query)
    # Calculer la similarité entre la requête et chaque phrase du texte
    max_similarity = 0
    most_relevant_sentence = ""
    for sentence in corpus:
        similarity = len(set(query).intersection(sentence)) / float(len(set(query).union(sentence)))
        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = " ".join(sentence)
    return most_relevant_sentence

# Fonction principale pour créer l'application Streamlit
def main():
    st.title("Chatbot")
    st.write("Hello! I'm a chatbot. Ask me anything about the topic in the text file.")
    
    # Obtenir la question de l'utilisateur
    question = st.text_input("You:")
    
    # Créer un bouton pour soumettre la question
    if st.button("Submit"):
        # Appeler la fonction pour trouver la réponse et l'afficher
        response = get_most_relevant_sentence(question)
        st.write("Chatbot: " + response)

if __name__ == "__main__":
    main()
