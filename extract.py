import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

# Load your logs
df = pd.read_csv("logs_dataset/logs_summary.csv")
errors = df["error_lines"]

# Vectorize errors (removing common words)
vectorizer = CountVectorizer(stop_words="english")
X = vectorizer.fit_transform(errors)

# Sum the counts of each word across all errors
word_counts = X.sum(axis=0).A1  # .A1 converts to a flat numpy array
keywords = vectorizer.get_feature_names_out()

# Create a dataframe for better sorting & plotting
word_freq = pd.DataFrame({"word": keywords, "count": word_counts})
word_freq = word_freq.sort_values(by="count", ascending=False).head(20)

# Plot the top 20 keywords
plt.figure(figsize=(10, 6))
plt.barh(word_freq["word"], word_freq["count"], color="skyblue")
plt.xlabel("Frequency")
plt.ylabel("Error Keywords")
plt.title("Top 20 Error Keywords in Logs")
plt.gca().invert_yaxis()  # Highest count at top
plt.show()
