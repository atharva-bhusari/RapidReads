# import the required libraries
import nltk
nltk.download('punkt') # punkt tokenizer for sentence tokenization
nltk.download('stopwords') # list of stop words, such as 'a', 'an', 'the', 'in', etc, which would be dropped
from collections import Counter # Imports the Counter class from the collections module, used for counting the frequency of words in a text.
from nltk.corpus import stopwords # Imports the stop words list from the NLTK corpus
# corpus is a large collection of text or speech data used for statistical analysis

from nltk.tokenize import sent_tokenize, word_tokenize # Imports the sentence tokenizer and word tokenizer from the NLTK tokenizer module. 
# Sentence tokenizer is for splitting text into sentences
# word tokenizer is for splitting sentences into words

# this function would take 2 inputs, one being the text, and the other being the summary which would contain the number of lines
def generate_summary(text, n):
    # Tokenize the text into individual sentences
    sentences = sent_tokenize(text)

    # Tokenize each sentence into individual words and remove stopwords
    stop_words = set(stopwords.words('english'))
    # the following line would tokenize each sentence from sentences into individual words using the word_tokenize function of nltk.tokenize module
    # Then removes any stop words and non-alphanumeric characters from the resulting list of words and converts them all to lowercase
    words = [word.lower() for word in word_tokenize(text) if word.lower() not in stop_words and word.isalnum()]

    # Compute the frequency of each word
    word_freq = Counter(words)

    # Compute the score for each sentence based on the frequency of its words
    # After this block of code is executed, sentence_scores will contain the scores of each sentence in the given text, 
    # where each score is a sum of the frequency counts of its constituent words

    # empty dictionary to store the scores for each sentence
    sentence_scores = {}

    for sentence in sentences:
        sentence_words = [word.lower() for word in word_tokenize(sentence) if word.lower() not in stop_words and word.isalnum()]
        sentence_score = sum([word_freq[word] for word in sentence_words])
        if len(sentence_words) < 20:
            sentence_scores[sentence] = sentence_score

    # checks if the length of the sentence_words list is less than 20 (parameter can be adjusted based on the desired length of summary sentences)
    # If condition -> true, score of the current sentence is added to the sentence_scores dictionary with the sentence itself as the key
    # This is to filter out very short sentences that may not provide meaningful information for summary generation

    # Select the top n sentences with the highest scores
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:n]
    summary = ' '.join(summary_sentences)

    return summary

text = """Recently, my fiance (20 m) and I (19f) moved into a new apartment with a mutual friend (20m) and 
somehow contracted scabies (don't know how). We've both been itchy af and have been to the doctor who confirmed 
that it was scabies for the both of us. Our room mate (20m) has not had symptoms of scabies bites appear yet but 
I have asked him to get treated as well and to treat his clothes and linen so that our apartment does not get 
reinfested after treatment.My room mate refuses to buy the lotion needed to kill the mites on his skin 
(if there are any on him) and refuses to rewash and dry his linen and clothes. I'm scared that if he does not get 
treated the infestation of our apartment will not go away. I'm almost there to asking him to move out if he refuses 
treatment. He is not on the lease."""


summary = generate_summary(text, 5)
summary_sentences = summary.split('. ')
formatted_summary = '.\n'.join(summary_sentences)

print(formatted_summary)

from rouge import Rouge

def evaluate_rouge(reference_text, summary_text):
    rouge = Rouge()
    scores = rouge.get_scores(reference_text, summary_text)
    return scores[0]['rouge-1']['f']

reference_summary = """Fiance and I recently got infected with scabies. Room mate refuses to get treated and our 
apartment will not go away. I'm afraid he will leave if he doesn't. Should I ask him to leave?"""

rouge_score = evaluate_rouge(reference_summary, formatted_summary)
print(rouge_score)