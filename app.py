import streamlit as st
import streamlit.components.v1 as components

st.title('삼각형 만들기 웹앱')

st.write('나무막대의 길이를 입력하세요 (cm)')

a = st.number_input('막대 1 길이', min_value=1, max_value=100)
b = st.number_input('막대 2 길이', min_value=1, max_value=100)
c = st.number_input('막대 3 길이', min_value=1, max_value=100)

if st.button('생성하기'):
    html_code = f"""
    <html>
    <head>
        <style>
            .bar {{
                width: 10px;
                height: 10px;
                position: absolute;
                background-color: black;
                cursor: pointer;
            }}
        </style>
    </head>
    <body>
        <div id="bar1" class="bar" style="width: {a * 10}px;"></div>
        <div id="bar2" class="bar" style="width: {b * 10}px;"></div>
        <div id="bar3" class="bar" style="width: {c * 10}px;"></div>
        
        <script>
            const bars = document.querySelectorAll('.bar');
            
            bars.forEach(bar => {{
                bar.addEventListener('mousedown', (e) => {{
                    const bar = e.target;
                    const offsetX = e.clientX - bar.getBoundingClientRect().left;
                    const offsetY = e.clientY - bar.getBoundingClientRect().top;

                    const onMouseMove = (e) => {{
                        bar.style.left = `${{e.clientX - offsetX}}px`;
                        bar.style.top = `${{e.clientY - offsetY}}px`;
                    }};

                    document.addEventListener('mousemove', onMouseMove);

                    document.addEventListener('mouseup', () => {{
                        document.removeEventListener('mousemove', onMouseMove);
                    }}, {{ once: true }});
                }});
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=400)
