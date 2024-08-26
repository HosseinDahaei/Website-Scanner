


# 🌐 Website Link Scanner & HTML Tree Generator


## 🚀 Project Overview

**Website Link Scanner & HTML Tree Generator** is a Python-based tool designed to scan any given website, extract all the internal links , and output them in a structured HTML tree format. This is perfect for web crawlers, SEOs, and developers who need to analyze website structure or map out all available links within a webpage.

![Rec0012-ezgif com-speed](https://github.com/user-attachments/assets/56e1d2f3-710b-4a63-a76e-9c81d782b78d)


## ✨ Features

- **Website Scanning**: Scans any URL to find all the internal links .
- **HTML Tree Generation**: Generates a hierarchical HTML tree representing the structure of links.
- **Support for Any Website**: Works on any public website, provided it's accessible and follows standard HTML structures.
- **Output Flexibility**: Can save output as HTML files for easy viewing or processing.
- **Error Handling**: Gracefully handles errors like broken links, timeout issues, or unsupported HTML formats.
  


## 🔧 Installation

To run the Website Link Scanner, you'll need to have Python 3.10 or higher installed on your machine. Follow these steps:

1. Clone this repository:

```bash
git clone git@github.com:HosseinDahaei/Website-Scanner.git
cd Website-Scanner
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python main.py https://example.com
```

## 🎮 Usage

After running the script with the URL of your choice, the program will scan the provided website and output the results as an HTML tree. 

The program will generate an HTML file (or print to stdout if preferred) that contains the links in a tree format like this:

```html
<ul>
  <li>https://example.com/
    <ul>
      <li>https://example.com/page1</li>
      <li>https://example.com/page2</li>
    </ul>
  </li>
</ul>
```

## 🛠️ Built With

- **Python**: Core programming language used for link scanning and tree generation.
- **Requests**: For fetching the HTML content of web pages.
- **BeautifulSoup (bs4)**: For parsing the HTML and extracting links.
- **HTML/CSS**: For generating the visual output of the tree.

## 📚 Examples

Check out the [example_output](tree.html) file to see what the generated HTML tree might look like.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌍 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/my-new-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/my-new-feature`).
5. Create a new Pull Request.

## 💬 Contact

If you have any questions, suggestions, or issues, feel free to open an issue or contact me directly at [dahaeehossein@gmail.com](mailto:dahaeehossein@gmail.com).

Happy scanning! 🚀

