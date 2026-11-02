BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&display=swap');

:root {
    --ivory: #F5F0E7;
    --cream: #E9DFD2;
    --charcoal: #302621;
    --burgundy: #6D2638;
    --rose: #B58A8D;
    --taupe: #8A7B70;
}

h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--charcoal) !important;
}

h1 {
    font-size: 3rem !important;
}

h2 {
    border-bottom: 1px solid var(--rose);
    padding-bottom: 0.4rem;
}

[data-testid="stCaptionContainer"] {
    color: var(--taupe) !important;
}

.stButton > button {
    border-radius: 10px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(109, 38, 56, 0.18);
}

@media (prefers-reduced-motion: reduce) {
    .stButton > button { transition: none; }
    .stButton > button:hover { transform: none; }
}
</style>
"""