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
    # Check if we've already done it to avoid duplicates
    if '.hero-content {' not in content.split('@media (max-width: 768px) {')[1]:
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
        content = content.replace("        @media (max-width: 768px) {", new_css, 1) # Only first occurrence

    # 3. Swap image with <picture> tag
    img_tag = r'<img src="https://cdn.shopify.com/s/files/1/0648/4826/5421/files/Freshly_Detailed_Ryft_McLaren_720s_on_HRE_Wheels_with_WIKD_Exhaust.jpg?v=1744062350" class="fade-image active" alt="Hero Background">'
    if img_tag in content:
        new_img_tag = """<picture>
                 <source media="(max-width: 768px)" srcset="https://cdn.shopify.com/s/files/1/0648/4826/5421/files/IMG_7141.jpg?v=1779221958">
                 <img src="https://cdn.shopify.com/s/files/1/0648/4826/5421/files/Freshly_Detailed_Ryft_McLaren_720s_on_HRE_Wheels_with_WIKD_Exhaust.jpg?v=1744062350" class="fade-image active" alt="Hero Background">
             </picture>"""
        content = content.replace(img_tag, new_img_tag)

    with open(filename, 'w') as f:
        f.write(content)

update_file('index.html')
update_file('ReactiveHeroHome')
