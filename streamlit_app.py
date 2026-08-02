import streamlit as st

st.set_page_config(
    page_title="知识图谱系统",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# 自定义 CSS 样式
# ============================================================
st.markdown("""
<style>
    /* ========== 设计变量 ========== */
    :root {
        --bg: #f5f5f7;
        --surface: #ffffff;
        --surface-hover: #fafafa;
        --border: #e5e5ea;
        --text: #1d1d1f;
        --text-2: #6e6e73;
        --text-3: #8e8e93;
        --text-4: #aeaeb2;
        --primary: #0071e3;
        --primary-hover: #0077ed;
        --primary-bg: #eaf4ff;
        --success: #30b36c;
        --danger: #e5484d;
        --warning: #ff9f0a;
        --r-1: 8px;
        --r-2: 12px;
        --r-3: 16px;
        --r-4: 20px;
        --shadow-s: 0 1px 3px rgba(0,0,0,0.04);
        --shadow-m: 0 4px 16px rgba(0,0,0,0.06);
        --shadow-l: 0 12px 40px rgba(0,0,0,0.08);
        --ease: cubic-bezier(0.25, 0.1, 0.25, 1);
    }

    /* ========== 基础 ========== */
    .stApp {
        background: var(--bg);
        color: var(--text);
    }
    .main .block-container {
        padding: 2.5rem 3rem 4rem;
        max-width: 1180px;
    }
    h1, h2, h3, h4 {
        font-weight: 600 !important;
        letter-spacing: -0.02em;
        color: var(--text) !important;
    }
    h1 { font-size: 1.6rem !important; }
    h2 { font-size: 1.25rem !important; }
    h3 { font-size: 1.05rem !important; margin-bottom: 0.6rem !important; }
    p { color: var(--text-2); line-height: 1.6; }

    /* ========== 侧边栏 ========== */
    [data-testid="stSidebar"] {
        background: #1c1c1e;
        border-right: 1px solid #2c2c2e;
    }
    [data-testid="stSidebar"] > div {
        padding-top: 0;
    }
    [data-testid="stSidebar"] * {
        color: #f5f5f7 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #2c2c2e !important;
        margin: 0.8rem 0;
    }
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
        background: transparent;
        border-radius: var(--r-1);
        padding: 0.55rem 0.85rem;
        margin-bottom: 0.15rem;
        transition: background 0.18s var(--ease), color 0.18s var(--ease);
        border: none;
        font-size: 0.88rem;
        color: #aeaeb2 !important;
        cursor: pointer;
    }
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
        background: rgba(255,255,255,0.05);
        color: #f5f5f7 !important;
    }
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
        background: rgba(0,113,227,0.2);
        color: #ffffff !important;
        font-weight: 500;
    }

    /* ========== 按钮 ========== */
    .stButton > button {
        border-radius: 100px !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        padding: 0.48rem 1.4rem !important;
        transition: all 0.2s var(--ease) !important;
        border: none !important;
        height: auto !important;
        min-height: 0 !important;
        line-height: 1.4 !important;
    }
    .stButton > button[kind="primary"] {
        background: var(--primary) !important;
        color: #fff !important;
        box-shadow: 0 1px 3px rgba(0,113,227,0.3);
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--primary-hover) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,113,227,0.35);
    }
    .stButton > button[kind="secondary"] {
        background: var(--surface) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: var(--surface-hover) !important;
    }

    /* ========== 卡片 ========== */
    .stat-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--r-2);
        padding: 1.1rem 1.2rem;
        text-align: center;
        transition: all 0.2s var(--ease);
    }
    .stat-card:hover {
        box-shadow: var(--shadow-m);
        transform: translateY(-2px);
    }
    .stat-card .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 0.35rem;
        opacity: 0.85;
    }
    .stat-card .stat-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--text);
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    .stat-card .stat-label {
        font-size: 0.75rem;
        color: var(--text-3);
        font-weight: 500;
        margin-top: 0.2rem;
    }

    /* ========== 上传区 ========== */
    [data-testid="stFileUploaderDropzone"] {
        border: 2px dashed var(--border) !important;
        border-radius: var(--r-3) !important;
        background: var(--surface) !important;
        padding: 2rem !important;
        transition: all 0.2s var(--ease) !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: var(--primary) !important;
        background: var(--primary-bg) !important;
    }
    [data-testid="stFileUploaderDropzone"] small {
        color: var(--text-2) !important;
    }

    /* ========== 输入框 ========== */
    .stTextInput > div > div > input {
        border-radius: var(--r-1) !important;
        border: 1px solid var(--border) !important;
        padding: 0.65rem 1rem !important;
        font-size: 0.92rem !important;
        background: var(--surface) !important;
        transition: all 0.2s var(--ease) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(0,113,227,0.12) !important;
    }

    /* ========== 对话 ========== */
    .msg-q {
        background: var(--primary-bg);
        border-radius: var(--r-2);
        padding: 0.85rem 1.05rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        line-height: 1.65;
        animation: fadeIn 0.25s ease;
    }
    .msg-q .role { color: var(--primary); font-weight: 600; font-size: 0.78rem; margin-bottom: 0.25rem; }
    .msg-a {
        background: #f0fdf4;
        border-radius: var(--r-2);
        padding: 0.85rem 1.05rem;
        margin-bottom: 0.6rem;
        font-size: 0.9rem;
        line-height: 1.65;
        animation: fadeIn 0.25s ease;
    }
    .msg-a .role { color: var(--success); font-weight: 600; font-size: 0.78rem; margin-bottom: 0.25rem; }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* ========== 展开面板 ========== */
    .streamlit-expanderHeader {
        border-radius: var(--r-1) !important;
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
    }
    .streamlit-expanderContent {
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 var(--r-1) var(--r-1) !important;
    }

    /* ========== 进度条 ========== */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary), var(--success)) !important;
        border-radius: 100px !important;
    }

    /* ========== 多选标签 ========== */
    .stMultiSelect [data-baseweb="tag"] {
        border-radius: 100px !important;
        background: var(--primary-bg) !important;
        color: var(--primary) !important;
        font-weight: 500 !important;
    }

    /* ========== 选择框/滑块 ========== */
    .stSelectbox > div > div {
        border-radius: var(--r-1) !important;
    }
    .stSlider > div > div > div > div {
        background: var(--primary) !important;
    }

    /* ========== 空状态 ========== */
    .empty-state {
        text-align: center;
        padding: 3.5rem 1rem 2rem;
        color: var(--text-3);
    }
    .empty-state-icon {
        width: 64px;
        height: 64px;
        margin: 0 auto 1rem;
        border-radius: 50%;
        background: var(--surface);
        border: 1px solid var(--border);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        opacity: 0.8;
    }
    .empty-state-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 0.4rem;
    }
    .empty-state-desc {
        font-size: 0.85rem;
        color: var(--text-3);
    }

    /* ========== 通知 ========== */
    .notice {
        border-radius: var(--r-1);
        padding: 0.7rem 1rem;
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.85rem;
        margin-bottom: 0.9rem;
    }
    .notice-ok {
        background: #eafaf1;
        border: 1px solid #c7ecd4;
        color: #1a6e3e;
    }

    /* ========== 隐藏 Streamlit 默认元素 ========== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 侧边栏
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:0.3rem 0 1rem;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#0071e3,#30b36c);
                        display:flex;align-items:center;justify-content:center;font-size:1.2rem;">
                🧠
            </div>
            <div>
                <div style="font-size:1.05rem;font-weight:600;color:#ffffff;line-height:1.2;">知识图谱</div>
                <div style="font-size:0.68rem;color:#8e8e93;letter-spacing:0.03em;">Knowledge Graph</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "",
        ["上传文档", "智能问答", "查看图谱"],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div style="font-size:0.68rem;color:#636366;text-transform:uppercase;letter-spacing:0.08em;
                margin:0.5rem 0 0.4rem;font-weight:600;">
        系统状态
    </div>
    """, unsafe_allow_html=True)

    try:
        from graph_retriever import execute_cypher
        node_count = execute_cypher("MATCH (n) RETURN count(n) AS count")
        rel_count = execute_cypher("MATCH ()-[r]->() RETURN count(r) AS count")

        if node_count:
            n = node_count[0] if not isinstance(node_count[0], dict) else node_count[0].get('count', 0)
            r = rel_count[0] if rel_count and not isinstance(rel_count[0], dict) else (rel_count[0].get('count', 0) if rel_count else 0)
            st.markdown(f"""
            <div style="background:rgba(48,179,108,0.1);border:1px solid rgba(48,179,108,0.2);border-radius:8px;padding:0.6rem 0.8rem;">
                <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
                    <span style="width:6px;height:6px;border-radius:50%;background:#30b36c;display:inline-block;"></span>
                    <span style="font-weight:500;font-size:0.8rem;color:#30b36c;">已连接</span>
                </div>
                <div style="color:#8e8e93;font-size:0.75rem;">{n} 实体 · {r} 关系</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,159,10,0.1);border:1px solid rgba(255,159,10,0.2);border-radius:8px;padding:0.6rem 0.8rem;">
                <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
                    <span style="width:6px;height:6px;border-radius:50%;background:#ff9f0a;display:inline-block;"></span>
                    <span style="font-weight:500;font-size:0.8rem;color:#ff9f0a;">数据库为空</span>
                </div>
                <div style="color:#8e8e93;font-size:0.75rem;">请先上传文档</div>
            </div>
            """, unsafe_allow_html=True)
    except Exception:
        st.markdown("""
        <div style="background:rgba(229,72,77,0.1);border:1px solid rgba(229,72,77,0.2);border-radius:8px;padding:0.6rem 0.8rem;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
                <span style="width:6px;height:6px;border-radius:50%;background:#e5484d;display:inline-block;"></span>
                <span style="font-weight:500;font-size:0.8rem;color:#e5484d;">未连接</span>
            </div>
            <div style="color:#8e8e93;font-size:0.75rem;">检查 Neo4j 服务</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="position:fixed;bottom:1.2rem;font-size:0.68rem;color:#48484a;">
        DeepSeek · Neo4j
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 页面头部
# ============================================================
if mode == "上传文档":
    st.markdown('<h1>上传文档</h1>', unsafe_allow_html=True)
    st.markdown('<p>上传 TXT 或 PDF 文件，AI 自动提取实体与关系构建知识图谱</p>', unsafe_allow_html=True)
elif mode == "智能问答":
    st.markdown('<h1>智能问答</h1>', unsafe_allow_html=True)
    st.markdown('<p>基于知识图谱的自然语言检索与问答</p>', unsafe_allow_html=True)
else:
    st.markdown('<h1>查看图谱</h1>', unsafe_allow_html=True)
    st.markdown('<p>可视化展示知识图谱实体与关系网络</p>', unsafe_allow_html=True)

# ============================================================
# 功能 1：文档上传
# ============================================================
if mode == "上传文档":
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 选择文件")
        uploaded_files = st.file_uploader(
            "支持 TXT / PDF 格式，可多选",
            type=["txt", "pdf"],
            accept_multiple_files=True,
            help="拖拽或点击选择文件",
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("### 处理选项")
        clear_first = st.checkbox("清空旧数据后再处理", value=False, help="勾选后，处理前会先清空知识库中的所有数据")

    if uploaded_files:
        all_text = ""
        file_info = []

        for uploaded_file in uploaded_files:
            file_type = uploaded_file.type
            text = ""

            if file_type == "text/plain":
                text = uploaded_file.read().decode("utf-8")
            elif file_type == "application/pdf":
                try:
                    import pdfplumber
                    with pdfplumber.open(uploaded_file) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                except ImportError:
                    st.error("请先安装 pdfplumber：`pip install pdfplumber`")
                except Exception as e:
                    st.error(f"PDF 解析失败：{e}")

            if text:
                all_text += text + "\n\n"
                file_info.append({"name": uploaded_file.name, "size": len(text), "status": "success"})
            else:
                file_info.append({"name": uploaded_file.name, "size": 0, "status": "failed"})

        st.markdown("### 文件加载情况")
        cols = st.columns(min(len(file_info), 3))
        for idx, fi in enumerate(file_info):
            with cols[idx % 3]:
                ok = fi["status"] == "success"
                st.markdown(f"""
                <div class="stat-card" style="border-left:3px solid {'#30b36c' if ok else '#e5484d'};">
                    <div class="stat-icon">{'✓' if ok else '✕'}</div>
                    <div style="font-weight:500;color:var(--text);font-size:0.85rem;word-break:break-all;margin-bottom:0.2rem;">{fi['name']}</div>
                    <div style="color:{'#30b36c' if ok else '#e5484d'};font-size:0.75rem;">
                        {fi['size']:,} 字符
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if all_text:
            with st.expander("内容预览", expanded=False):
                preview = all_text[:1000] + ("..." if len(all_text) > 1000 else "")
                st.text_area("预览", preview, height=180, label_visibility="collapsed")

            st.markdown("<br>", unsafe_allow_html=True)
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("开始智能处理", type="primary", width="stretch"):
                    progress_bar = st.progress(0, text="正在初始化...")

                    try:
                        from graph_builder import build_graph_from_text, clear_graph

                        if clear_first:
                            progress_bar.progress(10, text="正在清空旧数据...")
                            clear_graph()

                        progress_bar.progress(30, text="正在调用 AI 提取实体和关系...")
                        build_graph_from_text(all_text)

                        progress_bar.progress(80, text="正在写入知识图谱...")

                        from graph_retriever import execute_cypher
                        count_result = execute_cypher("MATCH (n) RETURN count(n) AS count")
                        rel_result = execute_cypher("MATCH ()-[r]->() RETURN count(r) AS count")

                        progress_bar.progress(100, text="处理完成")

                        n_count = count_result[0] if count_result and not isinstance(count_result[0], dict) else (count_result[0].get('count', 0) if count_result else 0)
                        r_count = rel_result[0] if rel_result and not isinstance(rel_result[0], dict) else (rel_result[0].get('count', 0) if rel_result else 0)

                        st.balloons()
                        st.success(f"处理完成！共提取 {n_count} 个实体，{r_count} 条关系")

                        metric_col1, metric_col2, metric_col3 = st.columns(3)
                        with metric_col1:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div class="stat-icon">📄</div>
                                <div class="stat-value">{len(uploaded_files)}</div>
                                <div class="stat-label">处理文件数</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with metric_col2:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div class="stat-icon">◈</div>
                                <div class="stat-value">{n_count}</div>
                                <div class="stat-label">知识实体</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with metric_col3:
                            st.markdown(f"""
                            <div class="stat-card">
                                <div class="stat-icon">⇄</div>
                                <div class="stat-value">{r_count}</div>
                                <div class="stat-label">关系连接</div>
                            </div>
                            """, unsafe_allow_html=True)

                    except Exception as e:
                        progress_bar.empty()
                        st.error(f"处理失败：{e}")
                        st.info("请确认 Neo4j 数据库连接是否正常，以及 DeepSeek API Key 是否有效。")
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📂</div>
            <div class="empty-state-title">拖拽文件到此处</div>
            <div class="empty-state-desc">支持 TXT 和 PDF 格式，可一次上传多个文件</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("使用说明", expanded=True):
            st.markdown("""
            **三步构建知识图谱：**

            1. **上传文档** — 拖拽或点击上传 TXT/PDF 文件
            2. **确认预览** — 检查文件内容是否正确加载
            3. **点击处理** — AI 自动提取实体和关系

            支持的实体类型：人物 · 组织 · 地点 · 产品 · 技术 · 日期 · 事件 · 概念
            """)

# ============================================================
# 功能 2：智能问答
# ============================================================
elif mode == "智能问答":
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    n_count = 0
    try:
        from graph_retriever import execute_cypher
        count_result = execute_cypher("MATCH (n) RETURN count(n) AS count")
        n_count = count_result[0] if count_result and not isinstance(count_result[0], dict) else (count_result[0].get('count', 0) if count_result else 0)

        if n_count > 0:
            type_result = execute_cypher("MATCH (n) RETURN DISTINCT n.type AS type")
            types = []
            if type_result:
                for t in type_result:
                    val = t if isinstance(t, str) else t.get('type', '')
                    if val:
                        types.append(val)

            st.markdown(f"""
            <div class="notice notice-ok">
                <span>📚</span>
                <div>
                    <span style="font-weight:600;">知识库就绪</span>
                    <span style="color:var(--text-2);font-size:0.82rem;"> · {n_count} 个实体 · {', '.join(types[:5])}{'...' if len(types) > 5 else ''}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("知识库中还没有数据，请先前往「上传文档」页面上传文件。")
    except Exception:
        st.error("无法连接数据库，请确认 Neo4j 服务是否正常运行。")

    if st.session_state.chat_history:
        st.markdown("### 对话记录")
        for idx, chat in enumerate(st.session_state.chat_history):
            st.markdown(f"""
            <div class="msg-q">
                <div class="role">你</div>
                <div>{chat['question']}</div>
            </div>
            <div class="msg-a">
                <div class="role">AI</div>
                <div>{chat['answer']}</div>
            </div>
            """, unsafe_allow_html=True)

    prompt = st.chat_input("输入你的问题，例如：DeepSeek 的总部在哪里？")
    if prompt:
        with st.spinner("AI 正在分析问题..."):
            try:
                from graph_qa import graph_qa
                answer = graph_qa(prompt)
                st.session_state.chat_history.append({
                    "question": prompt,
                    "answer": answer
                })
                st.rerun()
            except Exception as e:
                st.error(f"查询失败：{e}")

    if st.session_state.chat_history:
        if st.button("清空对话", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

    if n_count > 0 and not st.session_state.chat_history:
        with st.expander("试试这些问题", expanded=False):
            sample_questions = [
                "知识库中包含哪些人物？",
                "有哪些组织或公司？",
                "涉及哪些地点？",
                "有什么产品或技术？",
                "展示实体之间的关系",
            ]
            cols = st.columns(len(sample_questions))
            for i, sq in enumerate(sample_questions):
                with cols[i]:
                    if st.button(sq, key=f"sample_{i}", width="stretch"):
                        st.session_state.chat_history.append({
                            "question": sq,
                            "answer": "正在生成..."
                        })
                        try:
                            from graph_qa import graph_qa
                            st.session_state.chat_history[-1]["answer"] = graph_qa(sq)
                        except Exception as e:
                            st.session_state.chat_history[-1]["answer"] = f"查询失败：{e}"
                        st.rerun()

# ============================================================
# 功能 3：查看图谱
# ============================================================
else:
    try:
        from graph_retriever import execute_cypher

        nodes_result_all = execute_cypher("MATCH (n) RETURN n.name AS name, n.type AS type")
        rels_result_all = execute_cypher("MATCH (n)-[r]->(m) RETURN n.name AS source, r.type AS relation, m.name AS target")

        if not nodes_result_all:
            st.warning("知识库中还没有数据，请先前往「上传文档」页面上传文件。")
        else:
            type_result = execute_cypher("MATCH (n) RETURN DISTINCT n.type AS type")
            all_types = []
            type_counts = {}
            if type_result:
                for t in type_result:
                    val = t if isinstance(t, str) else t.get('type', '')
                    if val:
                        all_types.append(val)
                        count_r = execute_cypher(f"MATCH (n:Entity) WHERE n.type = '{val}' RETURN count(n) AS c")
                        if count_r:
                            c = count_r[0] if not isinstance(count_r[0], dict) else count_r[0].get('c', 0)
                            type_counts[val] = c

            total_nodes = len(nodes_result_all)
            total_rels = len(rels_result_all) if rels_result_all else 0

            metric_cols = st.columns(4)
            with metric_cols[0]:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">◈</div>
                    <div class="stat-value">{total_nodes}</div>
                    <div class="stat-label">实体总数</div>
                </div>
                """, unsafe_allow_html=True)
            with metric_cols[1]:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">⇄</div>
                    <div class="stat-value">{total_rels}</div>
                    <div class="stat-label">关系总数</div>
                </div>
                """, unsafe_allow_html=True)
            with metric_cols[2]:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">◎</div>
                    <div class="stat-value">{len(all_types)}</div>
                    <div class="stat-label">实体类型</div>
                </div>
                """, unsafe_allow_html=True)
            with metric_cols[3]:
                density = f"{total_rels / max(total_nodes, 1):.2f}"
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-icon">◇</div>
                    <div class="stat-value">{density}</div>
                    <div class="stat-label">平均连接度</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            if type_counts:
                st.markdown("### 实体类型分布")
                type_cols = st.columns(len(type_counts))
                type_colors_map = {
                    '人物': ('#FF6B6B', '◉'),
                    '组织': ('#4ECDC4', '▣'),
                    '地点': ('#45B7D1', '◈'),
                    '产品': ('#96CEB4', '▢'),
                    '技术': ('#FFEAA7', '⬡'),
                    '日期': ('#DDA0DD', '▤'),
                    '事件': ('#FF8A5C', '◆'),
                    '概念': ('#A29BFE', '◇'),
                }
                for i, (tname, tcount) in enumerate(type_counts.items()):
                    color, icon = type_colors_map.get(tname, ('#95A5A6', '○'))
                    with type_cols[i]:
                        st.markdown(f"""
                        <div class="stat-card" style="border-left:3px solid {color};">
                            <div style="font-size:1.4rem;color:{color};">{icon}</div>
                            <div class="stat-value" style="color:{color};">{tcount}</div>
                            <div class="stat-label">{tname}</div>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("### 图谱筛选")
            filter_col1, filter_col2, filter_col3 = st.columns([2, 2, 1])
            with filter_col1:
                selected_types = st.multiselect(
                    "按实体类型筛选",
                    all_types,
                    default=all_types,
                    help="选择要显示的实体类型"
                )
            with filter_col2:
                layout_choice = st.selectbox(
                    "图谱布局",
                    ["弹簧布局", "圆形布局", "分层布局"],
                    index=0
                )
            with filter_col3:
                node_size_slider = st.slider("节点大小", 800, 5000, 2000, step=200)

            if selected_types:
                import networkx as nx
                import matplotlib.pyplot as plt
                import matplotlib.patches as mpatches

                G = nx.DiGraph()

                for node in nodes_result_all:
                    if isinstance(node, dict):
                        node_name = node.get('name', '')
                        node_type = node.get('type', '未知')
                        if node_name and node_type in selected_types:
                            G.add_node(node_name, type=node_type)

                triples = []
                if rels_result_all and isinstance(rels_result_all, list):
                    if all(isinstance(item, str) for item in rels_result_all):
                        for i in range(0, len(rels_result_all) - 2, 3):
                            if i + 2 < len(rels_result_all):
                                triples.append({
                                    'source': rels_result_all[i],
                                    'relation': rels_result_all[i + 1],
                                    'target': rels_result_all[i + 2]
                                })
                    else:
                        for rel in rels_result_all:
                            if isinstance(rel, dict):
                                triples.append(rel)

                for triple in triples:
                    source = triple.get('source', '')
                    target = triple.get('target', '')
                    label = triple.get('relation', '')
                    if source and target and G.has_node(source) and G.has_node(target):
                        G.add_edge(source, target, label=label)

                if G.number_of_nodes() == 0:
                    st.info("当前筛选条件下没有数据，请调整筛选条件。")
                else:
                    plt.rcParams['font.family'] = 'sans-serif'
                    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']

                    fig, ax = plt.subplots(figsize=(16, 13), facecolor='#f5f5f7')
                    ax.set_facecolor('#f5f5f7')

                    if layout_choice == "弹簧布局":
                        pos = nx.spring_layout(G, seed=42, k=3, iterations=50)
                    elif layout_choice == "圆形布局":
                        pos = nx.circular_layout(G)
                    else:
                        pos = nx.kamada_kawai_layout(G)

                    type_colors = {
                        '人物': '#FF6B6B',
                        '组织': '#4ECDC4',
                        '地点': '#45B7D1',
                        '产品': '#96CEB4',
                        '技术': '#FFEAA7',
                        '日期': '#DDA0DD',
                        '事件': '#FF8A5C',
                        '概念': '#A29BFE',
                    }

                    node_colors = []
                    for node in G.nodes():
                        node_type = G.nodes[node].get('type', '未知')
                        node_colors.append(type_colors.get(node_type, '#95A5A6'))

                    nx.draw_networkx_edges(
                        G, pos, ax=ax,
                        edge_color='#c7c7cc',
                        width=2.0,
                        arrows=True,
                        arrowsize=18,
                        arrowstyle='->',
                        alpha=0.6,
                        connectionstyle='arc3,rad=0.12'
                    )

                    nx.draw_networkx_nodes(
                        G, pos, ax=ax,
                        node_color=node_colors,
                        node_size=node_size_slider,
                        alpha=0.92,
                        edgecolors='white',
                        linewidths=2.5
                    )

                    nx.draw_networkx_labels(
                        G, pos, ax=ax,
                        font_size=9,
                        font_weight='bold',
                        font_color='#1d1d1f'
                    )

                    edge_labels = {(u, v): d.get('label', '') for u, v, d in G.edges(data=True)}
                    nx.draw_networkx_edge_labels(
                        G, pos,
                        edge_labels=edge_labels, ax=ax,
                        font_size=7,
                        font_color='#86868b',
                        label_pos=0.5
                    )

                    ax.set_title("知识图谱可视化", fontsize=16, fontweight='600', color='#1d1d1f', pad=20, family='sans-serif')
                    ax.axis('off')

                    legend_patches = []
                    for tname, color in type_colors.items():
                        if tname in selected_types:
                            legend_patches.append(mpatches.Patch(color=color, label=tname))
                    if legend_patches:
                        legend = ax.legend(
                            handles=legend_patches,
                            loc='upper right',
                            fontsize=9,
                            frameon=True,
                            facecolor='white',
                            edgecolor='#e5e5ea',
                            framealpha=0.95,
                            title='实体类型',
                            title_fontsize=10
                        )

                    st.pyplot(fig)

                    st.markdown(f"""
                    <div style="text-align:center;color:var(--text-2);font-size:0.82rem;margin-top:0.5rem;">
                        当前显示 <strong>{G.number_of_nodes()}</strong> 个实体 · <strong>{G.number_of_edges()}</strong> 条关系 · 布局：{layout_choice}
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("查看所有关系详情", expanded=False):
                        if G.number_of_edges() > 0:
                            relation_data = []
                            for u, v, d in G.edges(data=True):
                                rel_type = d.get('label', '')
                                source_type = G.nodes[u].get('type', '')
                                target_type = G.nodes[v].get('type', '')
                                relation_data.append({
                                    "源实体": u,
                                    "源类型": source_type,
                                    "关系": rel_type,
                                    "目标实体": v,
                                    "目标类型": target_type
                                })
                            import pandas as pd
                            df = pd.DataFrame(relation_data)
                            st.dataframe(
                                df,
                                width="stretch",
                                hide_index=True,
                                column_config={
                                    "源实体": st.column_config.TextColumn("源实体", width="medium"),
                                    "源类型": st.column_config.TextColumn("源类型", width="small"),
                                    "关系": st.column_config.TextColumn("关系", width="small"),
                                    "目标实体": st.column_config.TextColumn("目标实体", width="medium"),
                                    "目标类型": st.column_config.TextColumn("目标类型", width="small"),
                                }
                            )

    except Exception as e:
        st.error(f"加载图谱失败：{e}")
        st.info("请确认 Neo4j 数据库连接是否正常。")

# ============================================================
# 页脚
# ============================================================
st.markdown("<div style='margin-top:2.5rem;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:var(--text-4);font-size:0.75rem;padding:1rem 0;">
    Knowledge Graph System · DeepSeek & Neo4j
</div>
""", unsafe_allow_html=True)