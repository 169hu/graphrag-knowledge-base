import streamlit as st

st.set_page_config(
    page_title="知识库",
    page_icon="📚",
    layout="wide"
)

st.sidebar.title("知识库")
st.sidebar.markdown("上传文档，提问，查看关联")

mode = st.sidebar.radio(
    "导航",
    ["上传文档", "提问", "查看图谱"]
)

st.markdown("# 知识库")
st.markdown("把文档变成结构化知识，方便查阅和提问")
st.markdown("---")

# ============================================================
# 功能 1：文档上传
# ============================================================
if mode == "上传文档":
    st.header("上传文档")
    st.markdown("把 TXT 或 PDF 文件拖进来，系统会自动梳理其中的关键信息。")

    uploaded_files = st.file_uploader(
        "选择文件（支持 TXT、PDF，可多选）",
        type=["txt", "pdf"],
        accept_multiple_files=True,
        help="支持 TXT 和 PDF 格式，可以一次选多个文件"
    )

    if uploaded_files:
        all_text = ""
        file_status = []

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
                    st.error("请先安装 pdfplumber：pip install pdfplumber")
                except Exception as e:
                    st.error(f"PDF 解析失败：{e}")
            else:
                st.error(f"不支持的文件类型：{file_type}")

            if text:
                all_text += text + "\n\n"
                file_status.append(f"已加载 {uploaded_file.name}（{len(text)} 字符）")
            else:
                file_status.append(f"未能解析 {uploaded_file.name}")

        st.subheader("文件加载情况")
        for status in file_status:
            st.write(status)

        if all_text:
            st.subheader("内容预览")
            preview = all_text[:800] + ("..." if len(all_text) > 800 else "")
            st.text_area("预览", preview, height=150)

            if st.button("开始处理", type="primary"):
                with st.spinner(f"正在从 {len(uploaded_files)} 个文件中提取关键信息..."):
                    try:
                        from graph_builder import build_graph_from_text, clear_graph

                        if st.checkbox("先清空旧数据再处理", value=False):
                            clear_graph()
                            st.info("旧数据已清空")

                        build_graph_from_text(all_text)
                        st.success("处理完成！")

                        try:
                            from graph_retriever import execute_cypher

                            count_result = execute_cypher("MATCH (n) RETURN count(n) AS count")
                            rel_result = execute_cypher("MATCH ()-[r]->() RETURN count(r) AS count")
                            if count_result:
                                st.info(
                                    f"当前共有 {count_result[0]} 个条目，{rel_result[0] if rel_result else 0} 条关联")
                        except Exception:
                            pass

                    except Exception as e:
                        st.error(f"处理失败：{e}")
                        st.info("请确认数据库连接是否正常。")
    else:
        st.info("请上传一个或多个 TXT/PDF 文件，然后点击「开始处理」。")

# ============================================================
# 功能 2：提问
# ============================================================
elif mode == "提问":
    st.header("提问")
    st.markdown("输入你想了解的内容，系统会从已上传的文档中查找答案。")

    try:
        from graph_retriever import execute_cypher

        count_result = execute_cypher("MATCH (n) RETURN count(n) AS count")
        if count_result and count_result[0] > 0:
            st.success(f"当前知识库中有 {count_result[0]} 条信息可供查询")
        else:
            st.warning("知识库中还没有数据，请先上传文档。")
    except Exception:
        st.warning("无法连接数据库，请确认服务是否在运行。")

    question = st.text_input(
        "你的问题",
        placeholder="例如：DeepSeek 的总部在哪里？"
    )

    if st.button("查询", type="primary") and question:
        with st.spinner("正在查找..."):
            try:
                from graph_qa import graph_qa

                answer = graph_qa(question)
                st.markdown("### 回答")
                st.markdown(f"> {answer}")
            except Exception as e:
                st.error(f"查询失败：{e}")

# ============================================================
# 功能 3：图谱查看
# ============================================================
else:
    st.header("查看图谱")
    st.markdown("以图形方式展示知识库中的条目及它们之间的关联。")

    try:
        from graph_retriever import execute_cypher

        type_result = execute_cypher("MATCH (n) RETURN DISTINCT n.type AS type")
        all_types = []
        if type_result:
            for t in type_result:
                if isinstance(t, dict) and t.get('type'):
                    all_types.append(t['type'])

        selected_types = []
        if all_types:
            st.subheader("按类型筛选")
            selected_types = st.multiselect(
                "选择要显示的类型",
                all_types,
                default=all_types
            )

        if selected_types:
            nodes_query = f"MATCH (n:Entity) WHERE n.type IN {selected_types} RETURN n.name AS name, n.type AS type"
            rels_query = f"""
            MATCH (n:Entity)-[r:RELATION]->(m:Entity)
            WHERE n.type IN {selected_types} AND m.type IN {selected_types}
            RETURN n.name AS source, r.type AS relation, m.name AS target
            """
        else:
            nodes_query = "MATCH (n) RETURN n.name AS name, n.type AS type"
            rels_query = "MATCH (n)-[r]->(m) RETURN n.name AS source, r.type AS relation, m.name AS target"

        nodes_result = execute_cypher(nodes_query)
        rels_result = execute_cypher(rels_query)

        if not nodes_result:
            st.warning("知识库中还没有数据，请先上传文档。")
        else:
            import networkx as nx
            import matplotlib.pyplot as plt

            G = nx.DiGraph()

            for node in nodes_result:
                if isinstance(node, dict):
                    node_name = node.get('name', '')
                    node_type = node.get('type', '未知')
                    if node_name:
                        G.add_node(node_name, type=node_type)
                else:
                    G.add_node(str(node))

            triples = []
            if rels_result and isinstance(rels_result, list):
                if all(isinstance(item, str) for item in rels_result):
                    for i in range(0, len(rels_result) - 2, 3):
                        if i + 2 < len(rels_result):
                            triples.append({
                                'source': rels_result[i],
                                'relation': rels_result[i + 1],
                                'target': rels_result[i + 2]
                            })
                else:
                    for rel in rels_result:
                        if isinstance(rel, dict):
                            triples.append(rel)

            for triple in triples:
                source = triple.get('source', '')
                target = triple.get('target', '')
                label = triple.get('relation', '')
                if source and target and G.has_node(source) and G.has_node(target):
                    G.add_edge(source, target, label=label)

            if G.number_of_edges() == 0:
                st.info("当前筛选条件下没有关联数据，请调整筛选条件。")
                with st.expander("查看原始数据"):
                    st.write(rels_result)
            else:
                fig, ax = plt.subplots(figsize=(14, 12))
                pos = nx.spring_layout(G, seed=42, k=2)

                node_colors = []
                type_colors = {
                    '人物': '#FF6B6B',
                    '组织': '#4ECDC4',
                    '地点': '#45B7D1',
                    '产品': '#96CEB4',
                    '技术': '#FFEAA7',
                    '日期': '#DDA0DD',
                    '事件': '#FF8A5C',
                    '概念': '#A29BFE',
                    '未知': '#95A5A6'
                }

                for node in G.nodes():
                    node_type = G.nodes[node].get('type', '未知')
                    node_colors.append(type_colors.get(node_type, '#95A5A6'))

                nx.draw_networkx_nodes(G, pos, ax=ax,
                                       node_color=node_colors,
                                       node_size=2000,
                                       alpha=0.9)

                nx.draw_networkx_edges(G, pos, ax=ax,
                                       edge_color='#94a3b8',
                                       width=1.5,
                                       arrows=True,
                                       arrowsize=15)

                nx.draw_networkx_labels(G, pos, ax=ax,
                                        font_size=10,
                                        font_weight='bold')

                edge_labels = {(u, v): d.get('label', '') for u, v, d in G.edges(data=True)}
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax,
                                             font_size=8)

                ax.set_title("知识图谱", fontsize=16)
                ax.axis('off')

                st.pyplot(fig)

                st.markdown("**图例**")
                legend_cols = st.columns(len(type_colors))
                for idx, (type_name, color) in enumerate(type_colors.items()):
                    col_idx = idx % len(legend_cols)
                    with legend_cols[col_idx]:
                        st.markdown(f"<span style='color:{color};'>●</span> {type_name}", unsafe_allow_html=True)

                with st.expander("查看所有关联"):
                    for u, v, d in G.edges(data=True):
                        st.write(f"**{u}** → **{v}**（{d.get('label', '')}）")

                st.caption(f"共 {G.number_of_nodes()} 个条目，{G.number_of_edges()} 条关联")

    except Exception as e:
        st.error(f"加载失败：{e}")
        st.info("请确认数据库连接是否正常。")