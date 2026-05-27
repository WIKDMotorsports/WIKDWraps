import re

def update_file(filename):
    with open(filename, 'r') as f:
        content = f.read()

    # 1. Update .hero in media query
    content = re.sub(
        r'(\@media\s*\(\s*max-width:\s*768px\s*\)\s*\{[^{}]*?\.hero\s*\{[^}]*?)min-height:\s*max\(70vh,\s*500px\);',
        r'\1min-height: 100vh;',
        content,
        flags=re.DOTALL
    )

    # 2. Add hero mobile layout rules
    new_css = """        @media (max-width: 768px) {
            .hero-content {
                height: 100%;
                justify-content: flex-start;
                padding-top: 15vh; /* Push title up but leave some space from top */
                padding-bottom: 5vh;
            }
            .hero-text-wrapper {
                display: flex;
                flex-direction: column;
                height: 100%;
            }
            .cta-buttons {
                margin-top: auto; /* Push buttons to the bottom */
            }"""
    if ".hero-content {" not in content:
        content = content.replace("        @media (max-width: 768px) {", new_css)

    # 3. Swap image with <picture> tag
    img_tag_start = '<div id="hero-bg-container" class="hero-bg-wrapper">'
    if 'source media="(max-width: 768px)"' not in content:
        content = re.sub(
            r'<div id="hero-bg-container" class="hero-bg-wrapper">\s*<img src="([^"]+)" class="fade-image active" alt="Hero Background">\s*</div>',
            r'<div id="hero-bg-container" class="hero-bg-wrapper">\n             <picture>\n                 <source media="(max-width: 768px)" srcset="https://cdn.shopify.com/s/files/1/0648/4826/5421/files/IMG_7141.jpg?v=1779221958">\n                 <img src="\1" class="fade-image active" alt="Hero Background">\n             </picture>\n        </div>',
            content
        )

    with open(filename, 'w') as f:
        f.write(content)

update_file('index.html')
update_file('ReactiveHeroHome')
