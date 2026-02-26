import os
import yaml

STATUS_MAP = {
    'proposed':  {'color': '#2196f3', 'label': 'PROPOSED'},
    'accepted':  {'color': '#4caf50', 'label': 'ACCEPTED'},
    'deprecated': {'color': '#f44336', 'label': 'DEPRECATED'},
    'superseded': {'color': '#ff9800', 'label': 'SUPERSEDED'}
}

def define_env(env):
    adr_dir = 'docs/adr'

    def get_tag_badge(tag):
        return f'<span style="border: 1px solid #757575; color: #757575; padding: 1px 6px; border-radius: 4px; font-size: 0.7em; margin-right: 4px;">#{tag}</span>'

    def get_all_data():
        adr_map, backlinks = {}, {}
        if not os.path.exists(adr_dir): return adr_map, backlinks
        files = [f for f in os.listdir(adr_dir) if f.endswith('.md')]
        
        for file in files:
            with open(os.path.join(adr_dir, file), 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    meta = yaml.safe_load(content.split('---')[1])
                    if 'id' in meta:
                        adr_map[meta['id']] = file
                        backlinks.setdefault(meta['id'], [])

        for file in files:
            with open(os.path.join(adr_dir, file), 'r', encoding='utf-8') as f:
                content = yaml.safe_load(f.read().split('---')[1])
                curr_id = content.get('id')
                for field, label in [('dependencies', 'Benötigt von'), ('references', 'Referenziert in')]:
                    for target in content.get(field) or []:
                        if target in backlinks:
                            backlinks[target].append(f"{label}: [{curr_id}](../{file})")
        
        return adr_map, backlinks

    @env.macro
    def generate_adr_index():
        adr_map, _ = get_all_data()
        files = sorted([f for f in os.listdir(adr_dir) if f.endswith('.md')])
        table = "| ID | Titel | Status | Tags | Datum |\n|----|-------|--------|------|-------|\n"
        
        for file in files:
            with open(os.path.join(adr_dir, file), 'r', encoding='utf-8') as f:
                meta = yaml.safe_load(f.read().split('---')[1])
                # Status-Badge
                st = meta.get('status', '').lower()
                cfg = STATUS_MAP.get(st, {'color': '#9e9e9e', 'label': st.upper()})
                badge = f'<span style="background-color: {cfg["color"]}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em;">{cfg["label"]}</span>'
                # Tags
                tags = "".join([get_tag_badge(t) for t in meta.get('tags', [])])
                
                table += f"| {meta.get('id')} | [{meta.get('title')}](adr/{file}) | {badge} | {tags} | {meta.get('date', '-')} |\n"
        return table

    @env.macro
    def render_adr_header():
        meta = env.page.meta
        adr_map, backlinks = get_all_data()
        
        st = meta.get('status', 'unknown').lower()
        cfg = STATUS_MAP.get(st, {'color': '#9e9e9e', 'label': st.upper()})
        badge = f'<span style="background-color: {cfg["color"]}; color: white; padding: 2px 10px; border-radius: 12px; font-weight: bold;">{cfg["label"]}</span>'
        tags = "".join([get_tag_badge(t) for t in meta.get('tags', [])])

        lines = [
            f"# {meta.get('id')}: {meta.get('title')}\n",
            f"{badge} {tags}\n",
            f"**Datum:** {meta.get('date', 'N/A')}\n"
        ]

        for field, label in [('dependencies', 'Abhängig von'), ('references', 'Referenzen')]:
            ids = meta.get(field) or []
            links = [f"[{i}](../{adr_map[i]})" if i in adr_map else i for i in ids]
            lines.append(f"**{label}:** {', '.join(links) if links else 'Keine'}\n")

        bl = list(set(backlinks.get(meta.get('id'), [])))
        if bl: lines.append(f"**Backlinks:** {', '.join(bl)}\n")

        return "\n".join(lines) + "\n\n---"
