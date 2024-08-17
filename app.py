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
            #angle-display {{
                position: absolute;
                font-size: 20px;
                font-weight: bold;
                color: black;
                transform: translate(-50%, -50%);
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
        
        <div id="angle-display"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAbElEQVR42mL8//8/AwXgPZhxP2UaomISWNjY5YOKCjBFpsCsSRqWwyJBGoCaYoZwI2II2MlRgAUZKuMAIokZoZZRWQ0kV5AVxKoAKQxiQJAxslFkqKKTREooDmjAoVCkM8wFMEGaCVoAH0VApRQODhY8KQqVhJZANQkAYVtM53m9A0AAAAASUVORK5CYII=" style="vertical-align:middle;" /> <span id="angle-text">0°</span></div>
        
        <script>
            const bars = document.querySelectorAll('.bar');
            const angleDisplay = document.getElementById('angle-display');
            const angleText = document.getElementById('angle-text');

            function calculateDistance(x1, y1, x2, y2) {{
                return Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
            }}

            function calculateAngle(x1, y1, x2, y2) {{
                let angle = Math.atan2(y2 - y1, x2 - x1) * (180 / Math.PI);
                return angle < 0 ? angle + 360 : angle;
            }}

            function snapToHandle(handle1, handle2) {{
                const rect1 = handle1.getBoundingClientRect();
                const rect2 = handle2.getBoundingClientRect();
                const distance = calculateDistance(rect1.left + rect1.width / 2, rect1.top + rect1.height / 2,
                                                    rect2.left + rect2.width / 2, rect2.top + rect2.height / 2);

                if (distance < 30) {{
                    handle1.style.left = `${{rect2.left - rect1.width/2}}px`;
                    handle1.style.top = `${{rect2.top - rect1.height/2}}px`;
                    return true;
                }}
                return false;
            }}

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

                    // 자석처럼 달라붙기
                    const rect1b = document.getElementById('handle1b').getBoundingClientRect();
                    const rect2a = document.getElementById('handle2a').getBoundingClientRect();
                    const rect2b = document.getElementById('handle2b').getBoundingClientRect();
                    const rect3a = document.getElementById('handle3a').getBoundingClientRect();

                    let snapped = snapToHandle(document.getElementById('handle1b'), document.getElementById('handle2a'))
                                || snapToHandle(document.getElementById('handle1b'), document.getElementById('handle3a'))
                                || snapToHandle(document.getElementById('handle2b'), document.getElementById('handle3a'));

                    if (snapped) {{
                        const angle = calculateAngle(rect1b.left, rect1b.top, rect2a.left, rect2a.top);
                        angleText.textContent = `${{Math.round(angle)}}°`;

                        // 각도 표시 위치 조정
                        const middleX = (rect1b.left + rect2a.left) / 2;
                        const middleY = (rect1b.top + rect2a.top) / 2;
                        angleDisplay.style.left = `${{middleX}}px`;
                        angleDisplay.style.top = `${{middleY}}px`;
                    }} else {{
                        angleText.textContent = '0°';
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
