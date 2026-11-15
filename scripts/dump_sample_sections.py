with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def print_section(tag, length=1200):
    pos = html.find(f'id="{tag}"')
    if pos != -1:
        print(f"\n==================== {tag} ====================")
        print(html[pos:pos+length])

print_section('tab-research-missions', 1500)
print_section('tab-research-satellites', 1500)
print_section('tab-research-equipment', 1500)
print_section('tab-research-resources', 1500)
