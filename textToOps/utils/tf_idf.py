from sklearn.feature_extraction.text import TfidfVectorizer

X = ["the cat in the hat",
     "the cat wearing a hat",
     "the cat's moving"
     "the cat is moving"
     ]
X_val = ["the cat is my hat"]
y = [1, 0]
y_val = [1]
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(X)
X_val = vectorizer.transform(X_val)

print(vectorizer.get_feature_names_out())
print(X_val)
