import asyncio
import re

import streamlit as st
from langchain_cli import run_agent_stream  # Hỗ trợ stream từng chunk

st.set_page_config(page_title="DataMart Chatbot", layout="wide")
st.title("🤖 DataMart Assistant")


# Khởi tạo lịch sử hội thoại
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại toàn bộ lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# user_input = st.text_input(
#     "Ask something:", placeholder="e.g., Show total revenue by day"
# )


class StreamlitStreamHandler:
    def __init__(self):
        self.output = ""
        self.container = st.empty()
        self.in_text_generation = False
        self.last_was_tool = False

    def handle_chunk(self, chunk):
        event = chunk.get("event", "")
        if event == "on_chat_model_stream":
            data = chunk.get("data", {})
            chunk_data = data.get("chunk", {})
            if hasattr(chunk_data, "content"):
                content = chunk_data.content
                if isinstance(content, str) and not content.startswith('{"'):
                    if self.last_was_tool:
                        self.output += " "
                        self.last_was_tool = False
                    self.output += content
                    self.container.markdown(self.output)
                    self.in_text_generation = True
                elif isinstance(content, list):
                    for item in content:
                        if (
                            isinstance(item, dict)
                            and item.get("type") == "text"
                        ):
                            text = item.get("text", "")
                            if text and not text.startswith('{"'):
                                if self.last_was_tool:
                                    self.output += " "
                                    self.last_was_tool = False
                                self.output += text
                                self.container.markdown(self.output)
                                self.in_text_generation = True
        elif event == "on_tool_start":
            if self.in_text_generation:
                self.output += f"\n\n🔧 **{chunk.get('name', 'tool')}**"
                self.container.markdown(self.output)
                self.in_text_generation = False
        elif event == "on_tool_end":
            self.output += " ✅"
            self.last_was_tool = True
            self.container.markdown(self.output)

    def get_output(self):
        return self.output


def extract_and_execute_code(markdown_text):

    import altair as alt
    import matplotlib.pyplot as plt
    import plotly.graph_objs as go
    import seaborn as sns
    import streamlit as st

    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, markdown_text, re.DOTALL)

    for code in matches:
        code = code.strip()
        # Hiển thị code phía trên chart
        # st.code(code, language="python")
        # Chuẩn bị môi trường thực thi riêng cho mỗi đoạn code
        local_env = {}
        try:
            exec(code, globals(), local_env)
        except Exception as e:
            st.error(f"Error executing chart code: {e}")
            continue
        # Hiển thị chart nếu có
        chart_displayed = False
        # 1. Matplotlib/seaborn
        figs = []
        for obj in local_env.values():
            if isinstance(obj, plt.Figure):
                figs.append(obj)
        # Nếu không có figure nào trong local_env, thử lấy figure hiện tại
        if not figs:
            fig = plt.gcf()
            if fig and fig.get_axes():
                figs.append(fig)
        for fig in figs:
            st.pyplot(fig)
            chart_displayed = True
        plt.close("all")
        # 2. Plotly
        for obj in local_env.values():
            if isinstance(obj, go.Figure):
                st.plotly_chart(obj, use_container_width=True)
                chart_displayed = True
        # 3. Altair
        for obj in local_env.values():
            if isinstance(obj, alt.Chart):
                st.altair_chart(obj, use_container_width=True)
                chart_displayed = True
        # 4. Bokeh (không cần import Figure)
        for obj in local_env.values():
            if type(obj).__name__ == "Figure" and getattr(
                obj, "__module__", ""
            ).startswith("bokeh."):
                st.bokeh_chart(obj, use_container_width=True)
                chart_displayed = True
        if not chart_displayed:
            st.info("No chart detected in this code block.")


async def process_query_stream(prompt):
    handler = StreamlitStreamHandler()

    async for chunk in run_agent_stream(prompt):
        handler.handle_chunk(chunk)

    # Sau khi stream xong: kiểm tra và thực thi biểu đồ
    extract_and_execute_code(handler.get_output())
    return handler.get_output()


# User gửi câu hỏi
if prompt := st.chat_input("Nhập câu hỏi của bạn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            try:

                async def run_stream():
                    return await process_query_stream(prompt)

                try:
                    response = asyncio.run(run_stream())
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(run_stream())

                # ❌ KHÔNG cần st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                st.error(f"Lỗi: {e}")
