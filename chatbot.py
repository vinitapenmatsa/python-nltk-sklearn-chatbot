import pdb
import nltk
import random
import string   # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

f = open('test.txt', 'r')
raw = f.read()
raw = raw.lower()

nltk.download('punkt')  # download libraries on first time use
nltk.download('wordnet')

sent_tokens = nltk.sent_tokenize(raw)  # converts data to list of sentences
word_tokens = nltk.word_tokenize(raw)  # converts to list of word_tokens

# WordNet is a semantically-oriented dictionary of English included in nltk
lemmer = nltk.stem.WordNetLemmatizer()


def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]


remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)


def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up",
                   "hey", "hola", "whatsup")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello",
                      "I am glad! You are talking to me",
                      "Hello , what do you want to ask me?"]


# checking if GREETING
def greeting(sentence):
    """If user's input is a greeting , return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# generating a response
def response(user_response):
    robo_response = ''
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    print 'Executing print transforms'
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf == 0):
        robo_response = robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag = True
print("VIN: Hi, I'm Vinita Penmetsa. Im glad you are interested in my profile, Ask me anything regarding my work experience. If you want to exit, type Bye!")


while(flag == True):
    user_response = raw_input()
    user_response = user_response.lower()
    if(user_response != 'bye'):
        if(user_response == 'thanks' or user_response == 'thank you'):
            flag = False
            print("ROBO: You are welcome..")
        else:
            if(greeting(user_response) != None):
                print("ROBO: "+greeting(user_response))
            else:
                sent_tokens.append(user_response)
                word_tokens = word_tokens + nltk.word_tokenize(user_response)
                final_words = list(set(word_tokens))
                print("ROBO: ")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag = False
        print("ROBO: Bye! take care..")
