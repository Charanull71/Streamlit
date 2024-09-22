# tag.py
import streamlit as st

# Define custom CSS for the animated tag
css = """
<style>
.tag {
    margin: -20px 0px 0px 0px;
    display: inline-block;
    padding: 5px 10px;
    border-radius: 10px;
    background: linear-gradient(134deg, rgb(241, 241, 188) 5.23%, rgb(228, 189, 52) 49.24%, rgb(218, 163, 5) 94.24%);
    position: relative;
    overflow: hidden;
    color: Black;
    font-weight: bold;
    font-size: 10px;  /* Adjust font size as needed */
    z-index: 1;  /* Ensure text is above sliding layer */
}

.tag::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    height: 100%;
    width: 100%;
    background: inherit;
    opacity: 0.2;  /* Make the sliding background lighter */
    animation: slide 3s linear infinite;
    z-index: 0;  /* Place the sliding background below the text */
}

@keyframes slide {
    0% {
        left: -100%;
    }
    50% {
        left: 100%;
    }
    100% {
        left: -100%;
    }
}
</style>
"""

# Render the page
def main():
    st.markdown(css, unsafe_allow_html=True)

    # Display a single tag
    tag_label = "Premium"
    st.markdown(f'<div class="tag">{tag_label}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
