import streamlit as st
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import json
from deep_translator import GoogleTranslator
def translate_to_english(text):
    try:
        translated = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)

        if translated:
            return translated

        return text

    except Exception:
        return text

st.set_page_config(
    page_title="HealthInfo Guard",
    page_icon="🔎",
    layout="centered"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #123047;
    --teal: #0F8B83;
    --mint: #E5F5F0;
    --text: #253B4D;
    --muted: #6C7E8D;
    --border: #E2EBEF;
}

.stApp {
    background:
        radial-gradient(ellipse at 0% 0%, #E4F5F1 0%, transparent 32%),
        #F7FAFC;
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1050px;
    padding: 2.2rem 2rem 4rem 2rem;
}

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: var(--navy) !important;
    letter-spacing: -0.7px;
}

h1 {
    font-size: 3.1rem !important;
    line-height: 1.12 !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 1.8rem !important;
    font-weight: 750 !important;
}

h3 {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
}

p, label, .stMarkdown {
    font-family: 'DM Sans', sans-serif;
}

p {
    line-height: 1.75;
}

.stTextArea textarea {
    background: #FFFFFF !important;
    color: var(--text) !important;
    border: 1px solid #D6E4E9 !important;
    border-radius: 15px !important;
    padding: 16px !important;
    font-size: 1rem !important;
    box-shadow: 0 3px 12px rgba(18, 48, 71, 0.035);
}

.stTextArea textarea:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 3px rgba(15, 139, 131, 0.12) !important;
}

.stButton button {
    background: var(--teal) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.78rem 1.4rem !important;
    font-weight: 700 !important;
    min-height: 48px;
    transition: 0.2s ease;
    box-shadow: 0 5px 14px rgba(15, 139, 131, 0.15);
}

.stButton button:hover {
    background: #0B716B !important;
    transform: translateY(-1px);
    box-shadow: 0 7px 18px rgba(15, 139, 131, 0.22);
}

div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid var(--border);
    border-radius: 15px;
    margin: 12px 0;
    box-shadow: 0 4px 15px rgba(18, 48, 71, 0.035);
}

div[data-testid="stExpander"] summary {
    font-weight: 650;
    color: var(--navy);
}

div[data-testid="stAlert"] {
    border-radius: 13px;
}

hr {
    border-color: var(--border);
    margin-top: 2rem;
    margin-bottom: 2rem;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

.stSlider [data-baseweb="slider"] {
    margin-top: 0.4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEALTHINFO GUARD INTERFACE
# =========================

st.markdown("""
<style>
/* Main page */
.stApp {
    background: #F5F8FA;
}

.block-container {
    max-width: 1050px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Hide default Streamlit branding */
#MainMenu, footer {
    visibility: hidden;
}

/* Header */
.hg-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0 28px 0;
    border-bottom: 1px solid #E1E9EE;
    margin-bottom: 42px;
}

.hg-brand {
    color: #123047;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.7px;
}

.hg-badge {
    background: #E1F5EF;
    color: #087F72;
    border: 1px solid #C8E9E0;
    padding: 8px 13px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

/* Hero */
.hg-eyebrow {
    color: #0D9488;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 18px;
}

.hg-title {
    color: #123047;
    font-family: 'Arial', sans-serif;
    font-size: 52px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.12;
    margin: 0 0 18px 0;
}

.hg-title span {
    color: #0D9488;
}

.hg-description {
    color: #637687;
    font-size: 17px;
    line-height: 1.8;
    max-width: 690px;
    margin-bottom: 28px;
}

/* Search card */
.hg-search-heading {
    color: #17384B;
    font-size: 21px;
    font-weight: 750;
    margin-bottom: 8px;
}

.hg-search-description {
    color: #758694;
    font-size: 14px;
    margin-bottom: 18px;
}

/* Features */
.hg-section-title {
    color: #123047;
    font-size: 23px;
    font-weight: 800;
    margin-top: 42px;
    margin-bottom: 7px;
}

.hg-section-subtitle {
    color: #758694;
    font-size: 14px;
    margin-bottom: 20px;
}

.hg-feature {
    background: #FFFFFF;
    border: 1px solid #E1E9EE;
    border-radius: 17px;
    padding: 23px 20px;
    min-height: 170px;
    box-shadow: 0 5px 20px rgba(18, 48, 71, 0.035);
}

.hg-icon {
    font-size: 25px;
    margin-bottom: 15px;
}

.hg-feature-title {
    color: #17384B;
    font-size: 16px;
    font-weight: 750;
    margin-bottom: 9px;
}

.hg-feature-text {
    color: #718292;
    font-size: 13px;
    line-height: 1.7;
}

.hg-footer {
    color: #8A99A5;
    font-size: 12px;
    text-align: center;
    padding-top: 25px;
}

/* Inputs */
.stTextArea textarea {
    background: #FFFFFF !important;
    border: 1px solid #D6E3E9 !important;
    border-radius: 13px !important;
    padding: 13px !important;
}

.stButton button {
    background: #0D9488 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 11px !important;
    font-weight: 700 !important;
    min-height: 46px;
}

.stButton button:hover {
    background: #0B766E !important;
}

div[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E1E9EE;
    border-radius: 13px;
    margin-bottom: 10px;
}

@media (max-width: 650px) {
    .hg-title {
        font-size: 38px;
    }

    .hg-description {
        font-size: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# Top navigation
st.markdown("""
<div class="hg-header">
    <div class="hg-brand">⌕ HealthInfo Guard</div>
    <div class="hg-badge">RESEARCH PREVIEW</div>
</div>
""", unsafe_allow_html=True)


# Hero section
st.markdown("""
<div class="hg-eyebrow">HEALTH CLAIM EXPLORER</div>

<div class="hg-title">
    Look beyond<br>
    the <span>headline.</span>
</div>

<div class="hg-description">
    Explore the science behind health claims.
    Discover scientific publications, read their findings,
    and take a closer look at the available evidence.
</div>
""", unsafe_allow_html=True)


# Search card introduction
st.markdown("""
<div class="hg-search-heading">
    Explore a health claim
</div>

<div class="hg-search-description">
    Enter a statement or question to discover relevant
    scientific publications from PubMed.
</div>
""", unsafe_allow_html=True)


# Search inputs — keep these variable names unchanged
claim = st.text_area(
    "What health claim would you like to investigate?",
    placeholder="e.g. Does regular physical activity improve sleep?",
    height=110,
    key="health_claim_input"
)

max_results = st.slider(
    "Number of publications to retrieve",
    min_value=3,
    max_value=10,
    value=5
)


# Feature cards
st.markdown("""
<div class="hg-section-title">Designed for better questions.</div>

<div class="hg-section-subtitle">
    Explore scientific information with greater context and clarity.
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="hg-feature">
        <div class="hg-icon">⌕</div>
        <div class="hg-feature-title">Scientific sources</div>
        <div class="hg-feature-text">
            Discover relevant publications and follow links
            to the original research.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="hg-feature">
        <div class="hg-icon">◈</div>
        <div class="hg-feature-title">Evidence context</div>
        <div class="hg-feature-text">
            Explore study findings without confusing
            keyword matches with scientific proof.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="hg-feature">
        <div class="hg-icon">◎</div>
        <div class="hg-feature-title">Transparent research</div>
        <div class="hg-feature-text">
            Remember that studies have limitations
            and evidence can be uncertain.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("""
<div class="hg-footer">
    HEALTHINFO GUARD · STUDENT RESEARCH PROTOTYPE
    <br><br>
    For research and educational purposes only.
    Not intended for diagnosis or treatment decisions.
</div>
""", unsafe_allow_html=True)


st.divider()

def search_pubmed(query, max_results):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    search_params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance"
    })

    search_url = base_url + "esearch.fcgi?" + search_params

    request = urllib.request.Request(
        search_url,
        headers={"User-Agent": "HealthInfoGuardStudentProject/1.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        search_data = response.read()

    search_result = json.loads(search_data.decode("utf-8"))
    article_ids = search_result["esearchresult"]["idlist"]

    if not article_ids:
        return []

    fetch_params = urllib.parse.urlencode({
        "db": "pubmed",
        "id": ",".join(article_ids),
        "retmode": "xml"
    })

    fetch_url = base_url + "efetch.fcgi?" + fetch_params

    request = urllib.request.Request(
        fetch_url,
        headers={"User-Agent": "HealthInfoGuardStudentProject/1.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    articles = []

    for article in root.findall(".//PubmedArticle"):
        title_element = article.find(".//ArticleTitle")
        abstract_elements = article.findall(".//Abstract/AbstractText")
        pmid_element = article.find(".//PMID")

        title = (
            "".join(title_element.itertext()).strip()
            if title_element is not None
            else "Title unavailable"
        )

        abstract = " ".join(
            "".join(element.itertext()).strip()
            for element in abstract_elements
        )

        pmid = (
            pmid_element.text
            if pmid_element is not None
            else None
        )

        articles.append({
            "title": title,
            "abstract": abstract,
            "pmid": pmid
        })

    return articles


if st.button("Search scientific evidence", type="primary"):
    if not claim.strip():
        st.warning("Please enter a health claim first.")

    else:
        with st.spinner("Searching PubMed for relevant publications..."):
            try:
                translated_claim = translate_to_english(claim)

                st.caption(
                    f"English search query: {translated_claim}"
                )

                articles = search_pubmed(translated_claim, max_results)

                st.divider()
                st.subheader("Search results")

                if not articles:
                    st.info(
                        "No publications were found for this query. "
                        "Try using different keywords."
                    )

                for index, article in enumerate(articles, start=1):
                    with st.expander(
                        f"{index}. {article['title']}"
                    ):
                        if article["abstract"]:
                            st.write(article["abstract"])
                        else:
                            st.write(
                                "No abstract is available in the retrieved record."
                            )

                        if article["pmid"]:
                            st.markdown(
                                f"[View publication on PubMed]"
                                f"(https://pubmed.ncbi.nlm.nih.gov/"
                                f"{article['pmid']}/)"
                            )

                st.caption(
                    "Important: finding a related publication does not "
                    "mean that it supports or disproves the claim. "
                    "Read the study and consider its limitations."
                )

            except Exception as error:
                st.error(
                    "The search could not be completed. "
                    "Check your internet connection and try again."
                )
                st.caption(f"Technical details: {error}")


st.divider()

st.caption(
    "Student hackathon prototype | HealthInfo Guard | "
    "Not intended for medical diagnosis or treatment decisions."
)
