"""Build isolated Zola fixtures and check rendered HTML using only Python's stdlib.

Usage: python tests/smoke.py --zola /path/to/zola
"""

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import tempfile


class Document(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.text = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)

    def find(self, tag, **attrs):
        return [a for t, a in self.tags if t == tag and all(a.get(k) == v for k, v in attrs.items())]


def write(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run(zola, root, *args):
    result = subprocess.run([zola, "--root", str(root), *args], capture_output=True, text=True, encoding="utf-8")
    assert result.returncode == 0, result.stdout + result.stderr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zola", default="zola")
    args = parser.parse_args()
    theme = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="xuan-zola-smoke-") as directory:
        root = Path(directory)
        target = root / "themes/xuan"
        for folder in ("templates", "i18n"):
            shutil.copytree(theme / folder, target / folder)
        shutil.copy2(theme / "theme.toml", target / "theme.toml")
        config = '''base_url = "https://example.com"
title = "Fixture"
theme = "xuan"
default_language = "en"
generate_feeds = true
feed_filenames = ["atom.xml", "rss.xml"]
taxonomies = [{name = "tags", feed = true}]
[languages.zh-Hans]
title = "Fixture ZH"
taxonomies = [{name = "tags", feed = true}]
[languages.fr]
title = "Fixture FR"
taxonomies = [{name = "tags", feed = true}]
[markdown]
lazy_async_image = true
external_links_target_blank = true
external_links_no_follow = true
external_links_no_referrer = true
[markdown.highlighting]
style = "class"
theme = "github-dark"
'''
        body = '''
## Heading

{{ <image url="photo.png" alt="A & B" config={config} /> }}

{{ <image url="large.png" url_min="small.png" config={config} /> }}

{{ <video url="movie.webm" alt="Film" controls={true} loop={true} muted={true} /> }}

{{ <youtube id="example" autoplay={true} start={12} /> }}

{{ <mastodon id="123" host="example.social" user="tester" config={config} /> }}

{% <crt> %}
**CRT content**
{% </crt> %}

```rust,linenos
fn main() {}
```

{% raw %}Literal {{ example }}{% endraw %}

{{ <xuan.translate key="posts" lang="ar" number={2} language_strings={ {"two_posts": "TWO"} } /> }}
{{ <xuan.translate key="posts" lang="ru" number={22} language_strings={ {"few_posts": "FEW"} } /> }}
<span id="native-reading-time">{{ page.reading_time }}</span>
'''
        for suffix in ("", ".zh-Hans", ".fr"):
            write(root, f"content/_index{suffix}.md", '+++\ntitle = "Home"\n+++\nWelcome')
            write(root, f"content/blog/_index{suffix}.md", '''+++
title = "Blog"
template = "article_list.html"
page_template = "article.html"
sort_by = "date"
paginate_by = 1
+++
''')
            for i in (1, 2):
                write(root, f"content/blog/post{i}{suffix}.md", f'''+++
title = "Post {i}"
date = {2027 - i}-09-12
updated = 2026-09-13T12:00:00+08:00
authors = ["Alice", "Bob"]
[taxonomies]
tags = ["Test"]
+++
''' + body)
            write(root, f"content/archive/_index{suffix}.md", '+++\ntitle = "Archive"\ntemplate = "archive.html"\n+++')
        # First pass deliberately omits every optional extra configuration table.
        write(root, "zola.toml", config)
        run(args.zola, root, "build")
        for prefix, expected in (("", "September 12, 2026"), ("zh-Hans/", "2026 年 09 月 12 日"), ("fr/", "September 12, 2026")):
            doc = Document(root / f"public/{prefix}blog/post1/index.html")
            assert expected in "".join(doc.text), (prefix, "date or translation fallback")
            assert "TWO" in "".join(doc.text) and "FEW" in "".join(doc.text)
            assert "Literal {{ example }}" in "".join(doc.text)
            assert doc.find("img", src="photo.png", alt="A & B", loading="lazy")
            assert doc.find("img", src="small.png", loading="lazy")
            video = doc.find("video", src="movie.webm")[0]
            assert all(attribute in video for attribute in ("controls", "loop", "muted"))
            assert doc.find("video", **{"aria-label": "Film"})
            assert doc.find("iframe", src="https://www.youtube-nocookie.com/embed/example?autoplay=1&start=12")
            assert doc.find("iframe", src="https://example.social/@tester/123/embed")
            assert doc.find("strong") and "CRT content" in "".join(doc.text)
            assert doc.find("time", datetime="2026-09-13T12:00:00+08:00")
            assert (root / f"public/{prefix}blog/page/2/index.html").exists()
            assert (root / f"public/{prefix}tags/test/index.html").exists()
            archive = Document(root / f"public/{prefix}archive/index.html")
            assert archive.find("a", href=f"https://example.com/{prefix}blog/post1/")
            assert [tag["id"] for tag in archive.find("h2", **{"class": "timeline-year"})] == ["year-2026", "year-2025"]
            assert archive.find("a", href="#year-2025")
        assert (root / "public/giallo.css").exists()
        assert (root / "public/atom.xml").exists() and (root / "public/rss.xml").exists()
        assert (root / "public/404.html").exists()
        # Second pass covers nested optional tables, CSP, reading time, and dual CSS.
        config = config.replace('theme = "github-dark"', 'light_theme = "github-light"\ndark_theme = "github-dark"')
        config += '''
[extra]
show_reading_time = true
show_copy_button = true
csp = [{directive="script-src", domains=["https://scripts.example.com"]}, {directive="connect-src", domains=["https://api.example.com"]}]
[extra.nav]
links = [{url="https://external.example.com", name="External"}]
show_theme_switcher = true
[extra.footer]
show_powered_by = true
'''
        write(root, "zola.toml", config)
        run(args.zola, root, "build")
        doc = Document(root / "public/blog/post1/index.html")
        assert doc.find("a", href="https://external.example.com", rel="noopener nofollow noreferrer")
        assert doc.find("a", href="https://www.getzola.org", rel="noopener nofollow noreferrer")
        assert doc.find("a", href="https://xuan-theme.jhq223.workers.dev", rel="noopener nofollow noreferrer")
        csp = doc.find("meta", **{"http-equiv": "content-security-policy"})[0]["content"]
        assert "https://scripts.example.com" in csp and "https://api.example.com" in csp
        assert doc.find("link", id="giallo-light") and doc.find("link", id="giallo-dark")
        assert (root / "public/giallo-light.css").exists() and (root / "public/giallo-dark.css").exists()
        assert doc.find("span", id="copy-code-text")
        text = "".join(doc.text)
        native = re.search(r'<span id="native-reading-time">(\d+)</span>', (root / "public/blog/post1/index.html").read_text(encoding="utf-8"))[1]
        assert f"{native} minute" in " ".join(text.split())
        zh_path = root / "public/zh-Hans/blog/post1/index.html"
        zh_native = re.search(r'<span id="native-reading-time">(\d+)</span>', zh_path.read_text(encoding="utf-8"))[1]
        assert f"阅读需要 {zh_native} 分钟" in "".join(Document(zh_path).text)
        run(args.zola, root, "check", "--skip-external-links")
    print("PASS: multilingual pages, optional settings, components, dates, pagination, feeds, CSP, highlighting, reading time")


if __name__ == "__main__":
    main()
