from markdown_to_html import markdown_to_html_node
import os, shutil, re,sys 

def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]

    project_dir = os.path.dirname(os.path.abspath(__file__)).replace("/src", '')
    public_dir = os.path.join(project_dir, "docs")
    convert(project_dir, public_dir)

    content_path = os.path.join(project_dir, "content")
    template_path = os.path.join(project_dir, "template.html")

    
    for item in os.listdir(content_path):
        item_path = os.path.join(content_path, item)
        
        
        if os.path.isfile(item_path):
            if item.endswith('.md'):
                output_filename = item.replace('.md', '.html')
                output_path = os.path.join(public_dir, output_filename)
            else:
                output_path = os.path.join(public_dir, item)
            print(f"Copying content files from {item_path} to {output_path}")
            try_generate_page(item_path, template_path, output_path, basepath)
        else:
            generate_html_recursive(item_path, public_dir,template_path,basepath, item)
    content_path = os.path.join(project_dir, "content", "index.md")    



def generate_html_recursive(sub_dir, public_dir,template_path, basepath, relative_path="" ):
    for item in os.listdir(sub_dir):
        item_path = os.path.join(sub_dir, item)
        relative_item_path = os.path.join(relative_path, item)
        
        if os.path.isfile(item_path):
            relative_item_path = relative_item_path.replace(".md", ".html")
            dest_path = os.path.join(public_dir, relative_item_path)
            print(f"Copying content files from {item_path} to {dest_path}")
            try_generate_page(item_path, template_path, dest_path, basepath)
        else:
            generate_html_recursive(item_path, public_dir, template_path, basepath, relative_item_path)

def try_generate_page(content_path, template_path, output_path, basepath):
    try:
        generate_page(content_path, template_path, output_path, basepath)
        print("Site generation completed successfully!")
    except Exception as e:
        print(f"Error generating site: {e}")
        raise

def generate_page(from_path, template_path, dest_path, basepath):

    with open(from_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    title = extract_title(markdown_content)

    html_content = markdown_to_html_node(markdown_content)
    
    html_content = html_content.to_html()


    final_html = template_content.replace('{{ Title }}', title)
    final_html = final_html.replace('{{ Content }}', html_content)
    if basepath != "/":
        final_html = final_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(final_html)


def convert(project_dir, public_dir):
    
    
    static_dir = os.path.join(project_dir, "static")
    
    if os.path.exists(public_dir):
        print("Removing existing public directory contents.")
        shutil.rmtree(public_dir)
        
    os.makedirs(public_dir, exist_ok=True)
    
    if os.path.exists(static_dir):
        print(f"Copying static files from {static_dir} to {public_dir}")
        for item in os.listdir(static_dir):
            src_path = os.path.join(static_dir, item)
            dst_path = os.path.join(public_dir, item)
            
            if os.path.isfile(src_path):
                print(f"Copying files {src_path} to {dst_path}")
                shutil.copy2(src_path, dst_path)
            elif os.path.isdir(src_path):
                convert_helper(src_path, dst_path)
        print("Static files copied successfully!")
    else:
        print("No static directory found, skipping static file copying")

def convert_helper(sub_dir, public_dir, relative_path=""):

    for item in os.listdir(sub_dir):
        item_path = os.path.join(sub_dir, item)
        relative_item_path = os.path.join(relative_path, item)
        dest_path = os.path.join(public_dir, relative_item_path)
        
        if os.path.isfile(item_path):
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(item_path, dest_path)
            print(f"Copied: {item_path} -> {dest_path}")
        else:
            convert_helper(item_path, public_dir, relative_item_path)


def extract_title(markdown):

    lines = markdown.split('\n')    
    for line in lines:
        if re.match(r'^#\s+', line):
            title = line[1:].strip()
            if title:  
                return title
    

    raise Exception("No h1 header found in markdown content")

if __name__ == "__main__":
  main()