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
            }}
            .handle {{
                width: 20px;
                height: 20px;
                background-color: black;
                border-radius: 50%;
                cursor: pointer;
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
            <div class="handle" id="handle1a" data-bar="bar1"></div>
            <div class="handle" id="handle1b" data-bar="bar1"></div>
        </div>
        <div id="bar2" class="bar">
            <div class="handle" id="handle2a" data-bar="bar2"></div>
            <div class="handle" id="handle2b" data-bar="bar2"></div>
        </div>
        <div id="bar3" class="bar">
            <div class="handle" id="handle3a" data-bar="bar3"></div>
            <div class="handle" id="handle3b" data-bar="bar3"></div>
        </div>
        
        <script>
            const bars = document.querySelectorAll('.bar');
            const handles = document.querySelectorAll('.handle');
            const snapDistance = 20;  // Adjust snap distance as needed
            
            function getDistance(x1, y1, x2, y2) {{
                return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
            }}
            
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
                    let selectedHandle = handle;
                    document.addEventListener('mousemove', onMouseMove);

                    document.addEventListener('mouseup', () => {{
                        document.removeEventListener('mousemove', onMouseMove);
                    }});

                    function onMouseMove(e) {{
                        const handleRect = selectedHandle.getBoundingClientRect();
                        const handleCenterX = handleRect.left + handleRect.width / 2;
                        const handleCenterY = handleRect.top + handleRect.height / 2;

                        handles.forEach(otherHandle => {{
                            if (otherHandle !== selectedHandle) {{
                                const otherRect = otherHandle.getBoundingClientRect();
                                const otherCenterX = otherRect.left + otherRect.width / 2;
                                const otherCenterY = otherRect.top + otherRect.height / 2;

                                const distance = getDistance(handleCenterX, handleCenterY, otherCenterX, otherCenterY);

                                if (distance < snapDistance) {{
                                    const bar1 = document.getElementById(selectedHandle.dataset.bar);
                                    const bar2 = document.getElementById(otherHandle.dataset.bar);
                                    
                                    const bar1Rect = bar1.getBoundingClientRect();
                                    const bar2Rect = bar2.getBoundingClientRect();

                                    const offsetX = otherCenterX - handleCenterX;
                                    const offsetY = otherCenterY - handleCenterY;

                                    bar1.style.left = `${{parseInt(bar1.style.left) + offsetX}}px`;
                                    bar1.style.top = `${{parseInt(bar1.style.top) + offsetY}}px`;

                                    bar1.style.transform = `rotate(${{
                                        Math.atan2(offsetY, offsetX) * (180 / Math.PI)
                                    }}deg)`;

                                    bar2.style.transform = `rotate(${{
                                        Math.atan2(offsetY, offsetX) * (180 / Math.PI)
                                    }}deg)`;

                                    selectedHandle.style.left = `${{otherHandle.offsetLeft}}px`;
                                    selectedHandle.style.top = `${{otherHandle.offsetTop}}px`;
                                }
                            }
                        }});
                    }
                }});
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)
