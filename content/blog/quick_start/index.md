+++
title = "快速开始"
description = "使用本主题"
date = 2025-11-27

[taxonomies]
tags = ["theme"]

[extra]
go_to_top = true
toc = true
toc_inline = true
+++

## 下载和安装

在你的博客目录

```bash
git submodule init
git submodule add https://github.com/jhq223/xuan.git themes/xuan
```

在`config.toml`中启用

```toml
theme = "xuan"
```

## 更新

```bash
git submodule update --remote --merge
```

## 配置页面

### 1. 创建归档页 (Archives)

在 `content` 目录下创建一个名为 `archive` 的文件夹（或其他你喜欢的名字），并在其中创建 `_index.md`：

```toml
+++
title = "归档"
template = "archive.html"
sort_by = "date"
+++
```

### 2. 创建友情链接页 (Friends)

在 `content` 目录下创建一个名为 `links` 的文件夹，并在其中创建 `_index.md`：

```toml
+++
title = "友链"
template = "links.html"
+++

这里可以写一些关于申请友链的说明，支持 **Markdown**。
```

## 个性化

### 使用图片背景

在`config.toml`中添加自定义css

```toml
[extra]
styles = ["mods.css"]
```

输入内容

```css
body {
    background-image: var(--bg-overlay), url("https://images.unsplash.com/photo-1523712999610-f77fbcfc3843");
    background-position: center;
    background-size: cover;
    background-attachment: fixed;
}
```

修改透明度

```scss
@import "../themes/xuan/sass/_variables.scss";

@include theme-variables using ($theme) {
    @if $theme == "dark" {
        --bg-overlay: linear-gradient(rgb(0 0 0 / 0.9), rgb(0 0 0 / 0.9));
    }

    @else {
        --bg-overlay: linear-gradient(rgb(255 255 255 / 0.8), rgb(255 255 255 / 0.8));
    }
}
```
