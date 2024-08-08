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
                height: 20px;
                position: absolute;
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
                transform-origin: left center;
            }}
            .handle {{
                width: 20px;
                height: 20px;
                background-color: black;
                border-radius: 50%;
                cursor: pointer;
            }}
            #bar1 {{
                background-color: red;
                width: {a * 30}px;
            }}
            #bar2 {{
                background-color: green;
                width: {b * 30}px;
            }}
            #bar3 {{
                background-color: blue;
                width: {c * 30}px;
            }}
        </style>
    </head>
    <body>
        <div id="bar1" class="bar" data-angle="0" style="left: 100px; top: 100px;">
            <div class="handle" id="handle1a"></div>
            <div class="handle" id="handle1b"></div>
        </div>
        <div id="bar2" class="bar" data-angle="0" style="left: 200px; top: 200px;">
            <div class="handle" id="handle2a"></div>
            <div class="handle" id="handle2b"></div>
        </div>
        <div id="bar3" class="bar" data-angle="0" style="left: 300px; top: 300px;">
            <div class="handle" id="handle3a"></div>
            <div class="handle" id="handle3b"></div>
        </div>
        
        <script>
            const bars = document.querySelectorAll('.bar');

            bars.forEach(bar => {{
                let isDragging = false;
                let isRotating = false;
                let startX, startY, initialAngle, handle, otherHandle, fixedHandleX, fixedHandleY;

                bar.addEventListener('mousedown', (e) => {{
                    if (e.target.classList.contains('handle')) {{
                        isRotating = true;
                        handle = e.target;
                        otherHandle = handle.id.endsWith('a') ? handle.nextElementSibling : handle.previousElementSibling;
                        const rect = otherHandle.getBoundingClientRect();
                        fixedHandleX = rect.left + rect.width / 2;
                        fixedHandleY = rect.top + rect.height / 2;
                        initialAngle = parseFloat(bar.getAttribute('data-angle')) || 0;
                        if (handle.id.endsWith('a')) {{
                            bar.style.transformOrigin = 'right center';
                        }} else {{
                            bar.style.transformOrigin = 'left center';
                        }}
                    }} else {{
                        isDragging = true;
                        startX = e.clientX - bar.getBoundingClientRect().left;
                        startY = e.clientY - bar.getBoundingClientRect().top;
                    }}
                }});

                document.addEventListener('mousemove', (e) => {{
                    if (isDragging) {{
                        bar.style.left = `${{e.clientX - startX}}px`;
                        bar.style.top = `${{e.clientY - startY}}px`;
                    }} else if (isRotating) {{
                        const dx = e.clientX - fixedHandleX;
                        const dy = e.clientY - fixedHandleY;
                        let angle = Math.atan2(dy, dx) * (180 / Math.PI);
                        if (handle.id.endsWith('a')) {{
                            angle += 180;
                        }}
                        bar.style.transform = `rotate(${{angle}}deg)`;
                        bar.setAttribute('data-angle', angle);
                    }}
                }});

                document.addEventListener('mouseup', () => {{
                    isDragging = false;
                    isRotating = false;
                }});
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)
