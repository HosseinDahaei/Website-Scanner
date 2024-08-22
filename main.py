
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from treelib import Node, Tree
from colorama import Fore,init
from time import sleep
init(autoreset = True)

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that are found on `url` in which it belongs to the same website
    """
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    try:
        soup = BeautifulSoup(requests.get(url, timeout=5).content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                # href empty tag
                continue
            # Join the URL if it's relative (not absolute link)
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            # remove URL GET parameters, URL fragments, etc.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                # not a valid URL
                continue
            if domain_name not in href:
                # external link
                continue
            urls.add(href)
    except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
        print(Fore.RED+f"Could not fetch {url}: {e}"+Fore.RESET)
    return urls

def parse_tree(tree):
    def get_subtree(nid):
        node = tree[nid]
        node_dict = {"name": node.tag, "children": []}
        for child in tree.children(nid):
            node_dict["children"].append(get_subtree(child.identifier))
        return node_dict

    root = tree.root
    return get_subtree(root)

def generate_html(tree):
    def count_subgroups(node):
        return len(node['children'])

    def generate_html_recursive(node):
        num_subgroups = count_subgroups(node)
        if not node['children']:
            return f"<li class='leaf'>{node['name']} ({num_subgroups})</li>"
        children_html = ''.join(generate_html_recursive(child) for child in node['children'])
        return f"""
        <li>
            <span class="caret node-with-children">{node['name']} ({num_subgroups})</span>
            <ul class="nested">{children_html}</ul>
        </li>"""

    html = f"""
    <html>
    <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }}
        ul {{
            list-style-type: none;
            padding-left: 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        .caret {{
            cursor: pointer;
            user-select: none;
            padding: 5px 10px;
            background-color: #f9f9f9;
            border-radius: 4px;
            display: inline-block;
            transition: background-color 0.3s, color 0.3s;
        }}
        .caret:hover {{
            background-color: #e6e6e6;
        }}
        .caret::before {{
            content: "\\25B6";  /* Right arrow */
            color: #555;
            display: inline-block;
            margin-right: 6px;
            transition: transform 0.3s;
        }}
        .caret-down::before {{
            transform: rotate(90deg);  /* Down arrow */
        }}
        .nested {{
            display: none;
            margin-left: 20px;
            border-left: 1px dashed #ddd;
            padding-left: 15px;
        }}
        .active {{
            display: block;
        }}
        .leaf {{
            color: green;
        }}
        .node-with-children {{
            color: blue;
        }}
        </style>
    </head>
    <body>
        <h2>Tree Structure</h2>
        <ul class="tree">
            {generate_html_recursive(tree)}
        </ul>
        <script>
        document.addEventListener('DOMContentLoaded', (event) => {{
            var togglers = document.getElementsByClassName("caret");
            for (var i = 0; i < togglers.length; i++) {{
                togglers[i].addEventListener("click", function() {{
                    this.parentElement.querySelector(".nested").classList.toggle("active");
                    this.classList.toggle("caret-down");
                }});
            }}
        }});
        </script>
    </body>
    </html>"""
    return html

def save_html_to_file(html, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html)

def convert_tree_to_html(tree, output_file_path):
    parsed_tree = parse_tree(tree)
    html = generate_html(parsed_tree)
    save_html_to_file(html, output_file_path)

def save_tree(tree, filename="tree"):
    """
    Save the tree to a file.
    """
    with open(f"{filename}.txt", "w") as f:
        pass
    tree.save2file(f"{filename}.txt",sorting=True,reverse=True)
    convert_tree_to_html(tree, f'{filename}.html')

def crawl(url, max_iter=30):
    """
    Crawl a web page and create a Tree of URLs.
    """
    def url_wrapper(url):
        url = url.strip()
        if url[-1] != "/":
            url += "/"
        output = url.split("/")[-2]
        # print(f"{url} --> {output}")
        return output
    tree = Tree()
    visited = set()   # To keep track of all visited URLs
    Queue = [(url,None)]
    iterr = 0
    pbar = tqdm(total = max_iter)

    while Queue and iterr < max_iter:
        
        current_url,parent = Queue.pop(0)
        if current_url not in visited:
            visited.add(current_url)
            if parent:
                tree.create_node(url_wrapper(current_url),current_url ,parent=parent)
            else:
                tree.create_node(current_url,current_url)
            links = get_all_website_links(current_url)
            for link in links:
                if link not in visited and is_valid(link):
                    Queue.append((link,current_url))
            iterr += 1
            if iterr % 50 == 0:
                save_tree(tree)
            pbar.update(1)
            sleep(0.1)
    pbar.close()
    return tree



start_url = input(Fore.GREEN+"Enter Your Target Website URL: "+Fore.RESET)
max_iter = int(input(Fore.CYAN+"Enter Max Iterations : "+Fore.RESET))
tree = crawl(start_url, max_iter=max_iter)
save_tree(tree)
print(Fore.GREEN+"Website Scanning completed successfully!!"+Fore.RESET)
