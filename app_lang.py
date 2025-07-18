import streamlit as st
from deep_translator import GoogleTranslator
import time

# Page configuration
st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .translation-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #28a745;
        margin: 10px 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #dc3545;
        margin: 10px 0;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 16px;
        line-height: 1.5;
    }
    
    .language-info {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Language codes mapping
LANGUAGES = {
    'English': 'en',
    'Urdu': 'ur',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-cn',
    'Chinese (Traditional)': 'zh-tw',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Turkish': 'tr',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Norwegian': 'no',
    'Danish': 'da',
    'Finnish': 'fi',
    'Greek': 'el',
    'Hebrew': 'he',
    'Thai': 'th',
    'Vietnamese': 'vi',
    'Indonesian': 'id',
    'Malay': 'ms',
    'Bengali': 'bn',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Gujarati': 'gu',
    'Punjabi': 'pa'
}

def translate_text(text, source_lang, target_lang):
    """Translate text using GoogleTranslator"""
    try:
        if source_lang == 'auto':
            translator = GoogleTranslator(target=target_lang)
        else:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        translated = translator.translate(text)
        return translated, None
    except Exception as e:
        return None, str(e)

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Language Translator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Translate text between multiple languages instantly</p>', unsafe_allow_html=True)
    
    # Sidebar for language selection
    with st.sidebar:
        st.header("🔧 Settings")
        
        # Source language selection
        source_lang_name = st.selectbox(
            "📥 From Language",
            ['Auto Detect'] + list(LANGUAGES.keys()),
            index=1  # Default to English
        )
        
        # Target language selection
        target_lang_name = st.selectbox(
            "📤 To Language",
            list(LANGUAGES.keys()),
            index=1  # Default to Urdu
        )
        
        # Get language codes
        source_lang = 'auto' if source_lang_name == 'Auto Detect' else LANGUAGES[source_lang_name]
        target_lang = LANGUAGES[target_lang_name]
        
        st.markdown("---")
        
        # Language info
        st.markdown("### 📊 Translation Info")
        if source_lang_name != 'Auto Detect':
            st.markdown(f'<div class="language-info"><strong>Source:</strong> {source_lang_name} ({source_lang})</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="language-info"><strong>Source:</strong> Auto Detect</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="language-info"><strong>Target:</strong> {target_lang_name} ({target_lang})</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick swap button
        if st.button("🔄 Swap Languages"):
            if source_lang_name != 'Auto Detect':
                st.session_state.temp_source = target_lang_name
                st.session_state.temp_target = source_lang_name
                st.experimental_rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(f"📝 Input Text ({source_lang_name})")
        input_text = st.text_area(
            "Enter text to translate:",
            height=200,
            placeholder="Type or paste your text here...",
            key="input_text"
        )
        
        # Character count
        char_count = len(input_text)
        st.caption(f"Characters: {char_count}")
        
        # Clear button
        if st.button("🗑️ Clear Text"):
            st.session_state.input_text = ""
            st.experimental_rerun()
    
    with col2:
        st.subheader(f"✨ Translation ({target_lang_name})")
        
        if input_text.strip():
            # Show loading spinner
            with st.spinner("Translating..."):
                translated_text, error = translate_text(input_text, source_lang, target_lang)
            
            if translated_text:
                # Display translation
                st.text_area(
                    "Translation:",
                    value=translated_text,
                    height=200,
                    key="output_text"
                )
                
                # Success message
                st.markdown(f'<div class="success-box">✅ Translation completed successfully!</div>', unsafe_allow_html=True)
                
                # Copy button
                if st.button("📋 Copy Translation"):
                    st.success("Translation copied! (Note: Actual copying requires browser interaction)")
                
            else:
                # Error message
                st.markdown(f'<div class="error-box">❌ Translation failed: {error}</div>', unsafe_allow_html=True)
                st.text_area(
                    "Translation:",
                    value="Translation failed. Please try again.",
                    height=200,
                    disabled=True
                )
        else:
            st.text_area(
                "Translation:",
                value="Enter text to see translation...",
                height=200,
                disabled=True
            )
    
    # Additional features
    st.markdown("---")
    
    # Quick translate section
    with st.expander("🚀 Quick Translate"):
        st.write("Common phrases for quick translation:")
        
        quick_phrases = [
            "Hello, how are you?",
            "Thank you very much",
            "What is your name?",
            "Where is the bathroom?",
            "How much does this cost?",
            "I need help",
            "Good morning",
            "Good night"
        ]
        
        cols = st.columns(4)
        for i, phrase in enumerate(quick_phrases):
            with cols[i % 4]:
                if st.button(phrase, key=f"quick_{i}"):
                    st.session_state.input_text = phrase
                    st.experimental_rerun()
    
    # Statistics
    if 'translation_count' not in st.session_state:
        st.session_state.translation_count = 0
    
    if input_text.strip() and translated_text:
        st.session_state.translation_count += 1
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <div style="text-align: center; color: #666; font-size: 14px;">
                <p>🌟 Powered by Google Translate API</p>
                <p>Translations performed: {}</p>
            </div>
            """.format(st.session_state.translation_count),
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()