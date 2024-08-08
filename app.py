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
                cursor: pointer;
            }}
            #bar1 {{
                background-color: red;
                width: {a * 10}px;
            }}
            #bar2 {{
                background-color: green;
                width: {b * 10}px;
            }}
            #bar3 {{
                background-color: blue;
                width: {c * 10}px;
            }}
        </style>
    </head>
    <body>
        <div id="bar1" class="bar"></div>
        <div id="bar2" class="bar"></div>
        <div id="bar3" class="bar"></div>
        
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
                
                bar.addEventListener('wheel', (e) => {{
                    const currentAngle = parseInt(bar.getAttribute('data-angle')) || 0;
                    const newAngle = currentAngle + (e.deltaY > 0 ? 10 : -10);
                    bar.style.transform = 'rotate(' + newAngle + 'deg)';
                    bar.setAttribute('data-angle', newAngle);
                }});
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)
