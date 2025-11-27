## 🚀 安装指南

### 1. 获取主题

假设你已经安装了 Git 和 Zola。在你的博客根目录下运行：

```bash
git clone https://github.com/你的用户名/xuan.git themes/xuan
```

### 2. 配置主题

在 `config.toml` 中设置主题名称：

```toml
theme = "xuan"
```

### 3. 配置 Pagefind 搜索 (关键步骤)

Xuan 使用 Pagefind 进行搜索。你需要先在本地安装 Pagefind：

```bash
npm install -g pagefind_extended
```

**构建与索引流程：**

每次发布博客时，你需要执行以下两个步骤：

1.  **构建 Zola 站点**:
    ```bash
    zola build
    ```
2.  **生成搜索索引**:
    指向你的输出目录（通常是 `public`）：
    ```bash
    npx pagefind --site public
    ```

完成这两步后，搜索功能才会生效。

## ⚙️ 选项配置

你可以在 `config.toml` 的 `[extra]` 部分自定义 Xuan 的外观。

### 全局配置

```toml
[extra]
# 默认主题 (light/dark)
default_theme = "system"

# 主题色 (支持任意 CSS 颜色值)
accent_color = "#3584e4"
accent_color_dark = "#ff7800"

# 是否启用 KaTeX 公式渲染
katex = true

# 是否在文章页启用目录 (TOC)
toc = true
```

### 样式与脚本

如果你需要添加自定义 CSS 或 JS：

```toml
[extra]
styles = [ "custom.css" ]
scripts = [ "custom.js" ]
```

## 📖 新增页面指南

Xuan 新增了两个特殊页面，请按照以下方式创建。

### 1. 创建归档页 (Archives)

在 `content` 目录下创建一个名为 `archive` 的文件夹（或其他你喜欢的名字），并在其中创建 `_index.md`：

```toml
+++
title = "归档"
template = "archive.html"  # 关键：必须指定此模板
+++
```

### 2. 创建友情链接页 (Friends)

在 `content` 目录下创建一个名为 `links` 的文件夹，并在其中创建 `_index.md`：

```toml
+++
title = "友情链接"
template = "links.html"    # 关键：必须指定此模板
+++

<!-- 在这里使用 Markdown 列表或表格添加你的链接 -->
| 博客名称 | 地址 | 描述 |
| :--- | :--- | :--- |
| Zola | https://www.getzola.org | 静态网站生成器 |
```

## 🔧 常见问题

**Q: 为什么搜索框无法使用？**
A: 请确保你在运行 `zola build` 后执行了 `pagefind --site public`。本地调试时，如果使用 `zola serve`，Pagefind 可能无法通过浏览器安全策略加载索引，建议使用 `npx pagefind --serve` 来预览构建后的站点。

**Q: 如何修改代码高亮样式？**
A: 主题默认内置了 One Dark Pro 样式。如果需要修改，请检查 `static/css` 目录下的相关 CSS 文件，或者在 `config.toml` 中覆盖高亮设置。
