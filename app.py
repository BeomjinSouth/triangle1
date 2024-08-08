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
                transform-origin: center;
                background-color: transparent;
            }}
            .handle {{
                width: 20px;
                height: 20px;
                background-color: black;
                border-radius: 50%;
                position: absolute;
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
        <div id="bar1" class="bar">
            <div class="handle" id="handle1a" style="left: -10px; top: -10px;"></div>
            <div class="handle" id="handle1b" style="right: -10px; top: -10px;"></div>
        </div>
        <div id="bar2" class="bar">
            <div class="handle" id="handle2a" style="left: -10px; top: -10px;"></div>
            <div class="handle" id="handle2b" style="right: -10px; top: -10px;"></div>
        </div>
        <div id="bar3" class="bar">
            <div class="handle" id="handle3a" style="left: -10px; top: -10px;"></div>
            <div class="handle" id="handle3b" style="right: -10px; top: -10px;"></div>
        </div>
        
        <script>
            const bars = document.querySelectorAll('.bar');
            const handles = document.querySelectorAll('.handle');
            const SNAP_DISTANCE = 30;  // 자석 효과 거리 (픽셀 단위)

            bars.forEach(bar => {{
                bar.style.left = '100px';
                bar.style.top = '100px';
                let isDragging = false;
                let isRotating = false;
                let startX, startY, initialAngle, handle, centerX, centerY;

                bar.addEventListener('mousedown', (e) => {{
                    if (e.target.classList.contains('handle')) {{
                        isRotating = true;
                        handle = e.target;
                        const rect = bar.getBoundingClientRect();
                        centerX = rect.left + rect.width / 2;
                        centerY = rect.top + rect.height / 2;
                        startX = e.clientX;
                        startY = e.clientY;
                        initialAngle = parseInt(bar.getAttribute('data-angle')) || 0;
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
                        const dx = e.clientX - centerX;
                        const dy = e.clientY - centerY;
                        const angle = Math.atan2(dy, dx) * (180 / Math.PI);
                        bar.style.transform = `rotate(${{angle}}deg)`;
                        bar.setAttribute('data-angle', angle);
                    }}
                }});

                document.addEventListener('mouseup', () => {{
                    isDragging = false;
                    isRotating = false;
                }});
            }});

            handles.forEach(handle => {{
                handle.addEventListener('mousedown', (e) => {{
                    handle.isDragging = true;
                    handle.startX = e.clientX - handle.getBoundingClientRect().left;
                    handle.startY = e.clientY - handle.getBoundingClientRect().top;
                }});

                document.addEventListener('mousemove', (e) => {{
                    if (handle.isDragging) {{
                        const handleRect = handle.getBoundingClientRect();
                        const handleCenterX = handleRect.left + handleRect.width / 2;
                        const handleCenterY = handleRect.top + handleRect.height / 2;
                        
                        handle.style.left = `${{e.clientX - handle.startX - handleRect.width / 2}}px`;
                        handle.style.top = `${{e.clientY - handle.startY - handleRect.height / 2}}px`;

                        handles.forEach(otherHandle => {{
                            if (handle !== otherHandle) {{
                                const rect1 = handle.getBoundingClientRect();
                                const rect2 = otherHandle.getBoundingClientRect();
                                const dx = rect1.left - rect2.left;
                                const dy = rect1.top - rect2.top;
                                const distance = Math.sqrt(dx * dx + dy * dy);

                                if (distance < SNAP_DISTANCE) {{
                                    handle.style.left = `${{rect2.left + window.scrollX}}px`;
                                    handle.style.top = `${{rect2.top + window.scrollY}}px`;
                                }}
                            }}
                        }});
                    }}
                }});

                document.addEventListener('mouseup', () => {{
                    handle.isDragging = false;
                }});
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)
