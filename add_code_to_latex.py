"""
Add code examples from Appendix C to LaTeX file
"""
import re

# Read the markdown file to get code examples
with open(r'C:\Users\Asus\.gemini\antigravity\brain\f806917d-127a-4604-a958-b6b6d5564b0c\assignment_report.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Extract Appendix C section
appendix_c_start = md_content.find('## Appendix C: Code Examples')
appendix_c_end = md_content.find('## Appendix B: References')  # Appendix B comes after C in the file
if appendix_c_end == -1:
    appendix_c_end = len(md_content)

appendix_c_text = md_content[appendix_c_start:appendix_c_end]

# Read the LaTeX file
with open(r'c:\Users\Asus\Desktop\PAI Solo Assignment\PAI-A1FT-Solo-Assignment\assignment_report.tex', 'r', encoding='utf-8') as f:
    latex_content = f.read()

# Find where to insert code examples (after "\\section{Appendix C: Code Examples}")
insert_marker = "\\section{Appendix C: Code Examples}"
insert_pos = latex_content.find(insert_marker)

if insert_pos == -1:
    print("❌ Could not find Appendix C section in LaTeX file")
    exit(1)

# Move past the section header and existing content
insert_pos = latex_content.find("\\textbf{Note:}", insert_pos)
insert_pos = latex_content.find("\\end{document}", insert_pos)

# Build LaTeX code examples
latex_code_examples = "\n\n"

# Extract each code example
code_example_pattern = r'### Code Example (\d+): (.+?)\n\n```(\w+)?\n(.*?)```'
matches = re.findall(code_example_pattern, appendix_c_text, re.DOTALL)

for match in matches:
    example_num, title, language, code = match
    
    # Clean up title
    title = title.replace('**', '').strip()
    
    # Add to LaTeX
    latex_code_examples += f"\\subsection*{{Code Example {example_num}: {title}}}\n\n"
    latex_code_examples += "\\begin{lstlisting}[language=Python]\n"
    latex_code_examples += code.strip() + "\n"
    latex_code_examples += "\\end{lstlisting}\n\n"

# Replace the placeholder in LaTeX
latex_before = latex_content[:insert_pos]
latex_after = latex_content[insert_pos:]

new_latex = latex_before + latex_code_examples + latex_after

# Save updated LaTeX file
with open(r'c:\Users\Asus\Desktop\PAI Solo Assignment\PAI-A1FT-Solo-Assignment\assignment_report.tex', 'w', encoding='utf-8') as f:
    f.write(new_latex)

print(f"✅ Added {len(matches)} code examples to LaTeX file!")
print(f"📄 File updated: assignment_report.tex")
print(f"\n📋 Code examples added:")
for match in matches:
    print(f"   • Code Example {match[0]}: {match[1].replace('**', '').strip()}")
