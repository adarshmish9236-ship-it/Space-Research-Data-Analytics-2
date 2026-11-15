with open('frontend/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Locate body tag and JS core script tag
pos_body = html.find('<body')
pos_js_start = html.find('<!-- JAVASCRIPT APPLICATION CORE -->')

print(f"Body starts at char: {pos_body} (line {html[:pos_body].count(chr(10))+1})")
print(f"JS core starts at char: {pos_js_start} (line {html[:pos_js_start].count(chr(10))+1})")
print(f"Length of HTML body markup: {pos_js_start - pos_body} characters")
