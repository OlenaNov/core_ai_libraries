
# Con gemini-embedding-2 l'istruzione sul tipo di compito si scrive nel testo.
# Scrivi prepara_query(query, tipo="search result") che restituisce task: {tipo} | query: {query}.
# Provala su str1 con i tipi search result e question answering, e su str2 con fact checking.

from init import *

def prepara_query(query, tipo="search result"):
    return f"task: {tipo} | query: {query}"



str1 = "Come posso pagare?"
str2 = "Il reso è gratuito"

print(prepara_query(str1))
print(prepara_query(str1, "Question, answering"))
print(prepara_query(str2, "fact checking"))
