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
    # Safely replace the img with picture.
    old_img_block = """<div id="hero-bg-container" class="hero-bg-wrapper">
             <img src="https://cdn.shopify.com/s/files/1/0648/4826/5421/files/Freshly_Detailed_Ryft_McLaren_720s_on_HRE_Wheels_with_WIKD_Exhaust.jpg?v=1744062350" class="fade-image active" alt="Hero Background">
        </div>"""

    new_img_block = """<div id="hero-bg-container" class="hero-bg-wrapper">
             <picture>
                 <source media="(max-width: 768px)" srcset="https://cdn.shopify.com/s/files/1/0648/4826/5421/files/IMG_7141.jpg?v=1779221958">
                 <img src="https://cdn.shopify.com/s/files/1/0648/4826/5421/files/Freshly_Detailed_Ryft_McLaren_720s_on_HRE_Wheels_with_WIKD_Exhaust.jpg?v=1744062350" class="fade-image active" alt="Hero Background">
             </picture>
        </div>"""

    content = content.replace(old_img_block, new_img_block)

    with open(filename, 'w') as f:
        f.write(content)

update_file('index.html')
update_file('ReactiveHeroHome')
