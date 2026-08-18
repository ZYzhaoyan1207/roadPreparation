import pandas as pd
import os


def alter(road, readDir, WriteDir):
    # 读取 CSV 文件（不是 Excel）
    roadfile = readDir + '/' + road + '/' + road + '_Edgelist.csv'
    df = pd.read_csv(roadfile)

    # 查看字段名
    print("字段名：", df.columns.tolist())
    print("\n前5行：")
    print(df.head())

    # ===== 请根据实际列名修改下面三行 =====
    FROM_COL = 'START_NODE'  # 起点列名
    TO_COL = 'END_NODE'  # 终点列名
    DIST_COL = 'LENGTH'  # 距离列名
    # ====================================

    # 1. 收集所有节点
    original_nodes = set(df[FROM_COL]).union(set(df[TO_COL]))

    # 2. 映射为连续序号
    node_list = sorted(original_nodes)
    old_to_new = {old: new for new, old in enumerate(node_list)}

    # 3. 生成边（四舍五入）
    new_edges = []
    for idx, row in df.iterrows():
        f = row[FROM_COL]
        t = row[TO_COL]
        d = float(row[DIST_COL])
        new_f = old_to_new[f]
        new_t = old_to_new[t]
        rounded_d = int(round(d))
        new_edges.append((new_f, new_t, rounded_d))

    # 4. 输出 GR 文件
    node_count = len(node_list)
    edge_count = len(new_edges)

    output_path = WriteDir + '/' + road + '_road.gr'
    with open(output_path, "w") as f:
        f.write(f"{node_count} {edge_count}\n")
        for frm, to, dist in new_edges:
            f.write(f"{frm} {to} {dist}\n")

    print(f"\n✅ 转换完成！")
    print(f"   节点数：{node_count}")
    print(f"   边数：{edge_count}")
    print(f"   输出：{output_path}")


readDir = os.getcwd() + '/sourceData'
WriteDir = os.getcwd() + '/roadOut'
roads = ['Dongguan', 'Fuzhou', 'Dalian', 'Qingdao', 'Tianjin', 'Shenzhen', 'Beijing', 'Dhaka', 'Medellin', 'Karachi',
         'Mumbai', 'Delhi']
for road in roads:
    print(f"{road} 开始转换:\n")
    alter(road, readDir, WriteDir)
