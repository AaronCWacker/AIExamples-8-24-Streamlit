# Import necessary libraries
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk import FreqDist
import re
import os
import base64
from graphviz import Digraph
from io import BytesIO
import networkx as nx
import matplotlib.pyplot as plt

# Set page configuration with a title and favicon
st.set_page_config(
    page_title="📺Transcript📜EDA🔍NLTK",
    page_icon="🌠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://huggingface.co/awacke1',
        'Report a bug': "https://huggingface.co/awacke1",
        'About': "https://huggingface.co/awacke1"
    }
)

st.markdown('''
1. 🔍 **Transcript Insights Using Exploratory Data Analysis (EDA)** 📊 - Unveil hidden patterns 🕵️‍♂️ and insights 🧠 in your transcripts. 🏆.
2. 📜 **Natural Language Toolkit (NLTK)** 🛠️:- your compass 🧭 in the vast landscape of NLP.
3. 📺 **Transcript Analysis** 📈:Speech recognition 🎙️ and thematic extraction 🌐, audiovisual content to actionable insights 🔑.
''')

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def remove_timestamps(text):
    return re.sub(r'\d{1,2}:\d{2}\n.*\n', '', text)

def extract_high_information_words(text, top_n=10):
    words = nltk.word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    freq_dist = FreqDist(filtered_words)
    return [word for word, _ in freq_dist.most_common(top_n)]

def create_relationship_graph(words):
    graph = Digraph()
    for index, word in enumerate(words):
        graph.node(str(index), word)
        if index > 0:
            graph.edge(str(index - 1), str(index), label=word)  # Add word as edge label
    return graph

def display_relationship_graph(words):
    graph = create_relationship_graph(words)
    st.graphviz_chart(graph)

def extract_context_words(text, high_information_words):
    words = nltk.word_tokenize(text)
    context_words = []
    for index, word in enumerate(words):
        if word.lower() in high_information_words:
            before_word = words[index - 1] if index > 0 else None
            after_word = words[index + 1] if index < len(words) - 1 else None
            context_words.append((before_word, word, after_word))
    return context_words

def create_context_graph(context_words):
    graph = Digraph()
    for index, (before_word, high_info_word, after_word) in enumerate(context_words):
        if before_word:
            graph.node(f'before{index}', before_word, shape='box')
        graph.node(f'high{index}', high_info_word, shape='ellipse')
        if after_word:
            graph.node(f'after{index}', after_word, shape='diamond')
        if before_word:
            graph.edge(f'before{index}', f'high{index}', label=before_word)  # Add before_word as edge label
        if after_word:
            graph.edge(f'high{index}', f'after{index}', label=after_word)  # Add after_word as edge label
    return graph

def display_context_graph(context_words):
    graph = create_context_graph(context_words)
    st.graphviz_chart(graph)

def display_context_table(context_words):
    table = "| Before | High Info Word | After |\n|--------|----------------|-------|\n"
    for before, high, after in context_words:
        table += f"| {before if before else ''} | {high} | {after if after else ''} |\n"
    st.markdown(table)

def load_example_files():
    # Exclude specific files
    excluded_files = {'freeze.txt', 'requirements.txt', 'packages.txt', 'pre-requirements.txt'}
    
    # List all .txt files excluding the ones in excluded_files
    example_files = [f for f in os.listdir() if f.endswith('.txt') and f not in excluded_files]
    
    # Check if there are any files to select from
    if example_files:
        selected_file = st.selectbox("📄 Select an example file:", example_files)
        if st.button(f"📂 Load {selected_file}"):
            with open(selected_file, 'r', encoding="utf-8") as file:
                return file.read()
    else:
        st.write("No suitable example files found.")
    
    return None

def cluster_sentences(sentences, num_clusters):
    # Filter sentences with length over 10 characters
    sentences = [sentence for sentence in sentences if len(sentence) > 10]

    # Check if the number of sentences is less than the desired number of clusters
    if len(sentences) < num_clusters:
        # If so, adjust the number of clusters to match the number of sentences
        num_clusters = len(sentences)

    # Vectorize the sentences
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)

    # Perform k-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)

    # Calculate the centroid of each cluster
    cluster_centers = kmeans.cluster_centers_

    # Group sentences by cluster and calculate similarity to centroid
    clustered_sentences = [[] for _ in range(num_clusters)]
    for i, label in enumerate(kmeans.labels_):
        similarity = linear_kernel(cluster_centers[label:label+1], X[i:i+1]).flatten()[0]
        clustered_sentences[label].append((similarity, sentences[i]))

    # Order sentences within each cluster based on their similarity to the centroid
    for cluster in clustered_sentences:
        cluster.sort(reverse=True)  # Sort based on similarity (descending order)

    # Return the ordered clustered sentences without similarity scores for display
    return [[sentence for _, sentence in cluster] for cluster in clustered_sentences]

def get_text_file_download_link(text_to_download, filename='Output.txt', button_label="💾 Save"):
    buffer = BytesIO()
    buffer.write(text_to_download.encode())
    buffer.seek(0)
    b64 = base64.b64encode(buffer.read()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="margin-top:20px;">{button_label}</a>'
    return href

def get_high_info_words_per_cluster(cluster_sentences, num_words=5):
    cluster_high_info_words = []
    for cluster in cluster_sentences:
        cluster_text = " ".join(cluster)
        high_info_words = extract_high_information_words(cluster_text, num_words)
        cluster_high_info_words.append(high_info_words)
    return cluster_high_info_words

def plot_cluster_words(cluster_sentences):
    for i, cluster in enumerate(cluster_sentences):
        cluster_text = " ".join(cluster)
        words = re.findall(r'\b[a-z]{4,}\b', cluster_text)
        word_freq = FreqDist(words)
        top_words = [word for word, _ in word_freq.most_common(20)]
        
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(top_words)
        word_vectors = X.toarray()
        
        similarity_matrix = cosine_similarity(word_vectors)
        
        G = nx.from_numpy_array(similarity_matrix)
        pos = nx.spring_layout(G, k=0.5)
        
        plt.figure(figsize=(8, 6))
        nx.draw_networkx(G, pos, node_size=500, font_size=12, font_weight='bold', with_labels=True, labels={i: word for i, word in enumerate(top_words)}, node_color='skyblue', edge_color='gray')  # Add word labels to nodes
        plt.axis('off')
        plt.title(f"Cluster {i+1} Word Arrangement")
        
        st.pyplot(plt)
        
        st.markdown(f"**Cluster {i+1} Details:**")
        st.markdown(f"Top Words: {', '.join(top_words)}")
        st.markdown(f"Number of Sentences: {len(cluster)}")
        st.markdown("---")

# Main code for UI
uploaded_file = st.file_uploader("📁 Choose a .txt file", type=['txt'])

example_text = load_example_files()

if example_text:
    file_text = example_text
elif uploaded_file:
    file_text = uploaded_file.read().decode("utf-8")
else:
    file_text = ""

if file_text:
    text_without_timestamps = remove_timestamps(file_text)
    top_words = extract_high_information_words(text_without_timestamps, 10)

    with st.expander("📊 Top 10 High Information Words"):
        st.write(top_words)

    with st.expander("📈 Relationship Graph"):
        display_relationship_graph(top_words)

    context_words = extract_context_words(text_without_timestamps, top_words)

    with st.expander("🔗 Context Graph"):
        display_context_graph(context_words)

    with st.expander("📑 Context Table"):
        display_context_table(context_words)

    #with st.expander("📝 Sentence Clustering", expanded=True):
    sentences = [line.strip() for line in file_text.split('\n') if len(line.strip()) > 10]

    num_sentences = len(sentences)
    st.write(f"Total Sentences: {num_sentences}")

    num_clusters = st.slider("Number of Clusters", min_value=2, max_value=10, value=5)
    clustered_sentences = cluster_sentences(sentences, num_clusters)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Text")
        original_text = "\n".join(sentences)
        st.text_area("Original Sentences", value=original_text, height=400)

    with col2:
        st.subheader("Clustered Text")
        clusters = ""
        clustered_text = ""
        cluster_high_info_words = get_high_info_words_per_cluster(clustered_sentences)

        for i, cluster in enumerate(clustered_sentences):
            cluster_text = "\n".join(cluster)
            high_info_words = ", ".join(cluster_high_info_words[i])
            clusters += f"Cluster {i+1} (High Info Words: {high_info_words})\n"
            clustered_text += f"Cluster {i+1} (High Info Words: {high_info_words}):\n{cluster_text}\n\n"

        st.text_area("Clusters", value=clusters, height=200)
        st.text_area("Clustered Sentences", value=clustered_text, height=200)

        # Verify that all sentences are accounted for in the clustered output
        clustered_sentences_flat = [sentence for cluster in clustered_sentences for sentence in cluster]
        if set(sentences) == set(clustered_sentences_flat):
            st.write("✅ All sentences are accounted for in the clustered output.")
        else:
            st.write("❌ Some sentences are missing in the clustered output.")
    
    plot_cluster_words(clustered_sentences)

st.markdown("For more information and updates, visit our [help page](https://huggingface.co/awacke1).")