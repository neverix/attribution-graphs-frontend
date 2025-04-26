from pathlib import Path
import json

q_p = {
    "linkType": "both",
    # node IDs
    "pinnedIds": [],
    # some node ID
    "clickedId": "",
    # supernode name + node list
    "supernodes": [],
    # x/y position pairs for supernodes, separated by spaces
    "sg_pos": "",
}
md = {
            "slug": "a-slug",
            "scan": "some-scan",
            "prompt_tokens": [
                "\u003CEOT\u003E",
                "↑",
                "Something"
            ],
            "prompt": "Something",
            "title_prefix": ""
        }

og_path = Path("og_data")
metadatas = []
for f in og_path.glob("*.json"):
    out_path = "graph_data" / f.relative_to(og_path)
    json_data = json.loads(f.read_text())
    links = []
    for edge in json_data["edges"]:
        # print(edge)
        # 1/0
        links.append({
            "source": edge["source"]["id"],
            "target": edge["target"]["id"],
            "weight": edge["weight"],
        })
    tokens = {}
    for node in json_data["nodes"]:
        if node["layer_index"] != -1:
            continue
        tokens[node["token_position"]] = node["token_str"]
    nodes = []
    for node in json_data["nodes"]:
        node["feature_type"] = node["node_type"]
        node["layer"] = node["layer_index"]
        node["jsNodeId"] = node["id"]
        try:
            node["feature"] = node["feature_index"]
        except KeyError:
            # TODO attention
            continue
            print(node)
        nodes.append(node)
    json_data["nodes"] = nodes
    json_data["links"] = links
    md["prompt_tokens"] = [tokens[i] for i in range(len(tokens))]
    md["prompt"] = "".join(md["prompt_tokens"])
    md["slug"] = f.stem
    json_data["metadata"] = md
    q_p["clickedId"] = nodes[0]["id"]
    json_data["qParams"] = q_p
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(json_data))
    metadatas.append({k: v for k, v in md.items()})

open("data/graph-metadata.json", "w").write(json.dumps(dict(graphs=metadatas)))