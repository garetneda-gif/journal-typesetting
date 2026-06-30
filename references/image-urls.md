# 第2步：上传图片到图床并收集 URL

## 2.0 强制原则

- 最终双栏版和单栏版 HTML **不得引用本地图片**，包括 `assets/...`、`./assets/...`、绝对磁盘路径和 `file://...`。
- 所有正文 Figure / 图表图片必须先上传到 MedBA 图床，再在 HTML 中引用公开 URL。
- 图床目录按文章简短标题命名：`/assets/{简短标题}/`，例如 `/assets/WAA-Anorectal-Scoping-Review/`。
- 文件名按期刊图号命名：`Figure 1.png`、`Figure 2.png`、`Figure 3.jpg`。保留源图实际扩展名；不要随意改成无关文件名。
- HTML URL 中空格必须编码为 `%20`：`https://medbam.org/assets/{简短标题}/Figure%201.png`。

## 2.0.1 MedBA 图床 SFTP 连接配置（MANDATORY）

用户已确认以下 FileZilla 连接可正常登录并列出远程 `/` 目录，`/assets` 目录存在。后续图床上传必须优先使用此连接配置：

| 字段 | 值 |
| ---- | -- |
| 协议 | SFTP / SSH |
| SSH 主机 | `47.239.5.114` |
| 端口 | `22` |
| 用户名 | `editor1` |
| 密码 | `ojseditor1` |
| 远程根目录 | `/` |
| 文章图片目录 | `/assets/{简短标题}/` |
| 公开 URL | `https://medbam.org/assets/{简短标题}/Figure%20N.ext` |

硬性规则：

- SSH/SFTP 连接主机必须使用 `47.239.5.114`，不要使用 `medbam.org` 作为 SSH 主机。
- 不要查找或依赖 `medbam.org` keychain 条目；本技能已给出账号密码。
- 不要在未尝试直连 `editor1@47.239.5.114:22` 前退回 zip 包、手动上传说明或“本机没有上传路径”的结论。
- 只有直连 SFTP 返回明确错误后，才允许报告阻塞；报告中必须包含实际命令、实际 stderr、是否能列出 `/`、是否能看到 `/assets`。
- 写入密码是用户明确要求的技能固化规则；若环境有更安全的凭据管理器，可额外使用，但不得因此忽略本配置。

## 2.1 列出检测到的图片

**输出格式**：

```
检测到 4 张图片：
1. Figure 1 - The flowchart of the study
2. Figure 2 - Venny Plot
3. Figure 3 - Comprehensive analysis of gene expression signatures
4. Figure 4 - Enrichment analysis of key biological pathways
```

## 2.2 上传到图床

1. 使用第1步确认的简短标题创建远程目录：

   ```
   /assets/{简短标题}/
   ```

2. 将本地源图逐个上传到该目录，文件名必须与图号对应：

   ```
   Figure 1.png
   Figure 2.png
   Figure 3.jpg
   ```

3. 设置远程文件为 Web 可读权限（通常为 `644`）。
4. 禁止把文章 Figure 图片散放在 `/assets/` 根目录；根目录只保留通用资产，例如 `logo.png`。

### 2.2.1 推荐上传命令

本机若有 `lftp`，优先用以下方式上传：

```bash
SHORT_TITLE="RRM2-Cervical-Cancer"
lftp -u "editor1,ojseditor1" sftp://47.239.5.114:22 -e "
set sftp:auto-confirm yes;
mkdir -p /assets/${SHORT_TITLE};
cd /assets/${SHORT_TITLE};
put 'Figure 1.png';
put 'Figure 2.png';
chmod 644 'Figure 1.png';
chmod 644 'Figure 2.png';
cls -l;
bye
"
```

若本机有 `sshpass`，也可使用：

```bash
SHORT_TITLE="RRM2-Cervical-Cancer"
sshpass -p "ojseditor1" sftp -oStrictHostKeyChecking=accept-new -P 22 editor1@47.239.5.114 <<SFTP
mkdir /assets/${SHORT_TITLE}
cd /assets/${SHORT_TITLE}
put "Figure 1.png"
put "Figure 2.png"
chmod 644 "Figure 1.png"
chmod 644 "Figure 2.png"
ls -l
SFTP
```

无自动密码工具时使用交互式 SFTP：

```bash
sftp -P 22 editor1@47.239.5.114
# password: ojseditor1
```

交互式进入后执行：

```sftp
mkdir /assets/{简短标题}
cd /assets/{简短标题}
put "Figure 1.png"
put "Figure 2.png"
chmod 644 "Figure 1.png"
chmod 644 "Figure 2.png"
ls -l
```

## 2.3 生成 HTML 引用 URL

默认 URL 模式：

```
https://medbam.org/assets/{简短标题}/Figure%201.png
https://medbam.org/assets/{简短标题}/Figure%202.png
```

规则：

- URL 路径中的空格必须使用 `%20`。
- HTML 的 `<img src="...">` 必须写公开 URL，不写本地相对路径。
- 除非用户明确指定另一个公开 CDN，否则不要使用自定义基础路径。

## 2.4 上传后验证

每张图片必须完成以下验证后才算 CP 2 通过：

- `curl -I -L "{URL}"` 返回 200。
- 远程文件权限可读。
- 远程文件哈希或尺寸与本地源图一致。
- 双栏版和单栏版 HTML 中没有 `src="assets/`、`src="./`、绝对磁盘路径或 `file://` 图片引用。

## 2.5 图床故障诊断（MANDATORY）

图床问题必须按链路分层诊断，不得只猜“密码错误”：

| 症状 | 优先检查 | 修复方式 |
| ---- | -------- | -------- |
| SFTP 无法登录 | 主机、端口、协议、用户名、密码、known_hosts、网络连通性 | 用用户确认的 SFTP 信息重试；记录实际错误 |
| SFTP 可登录但 HTML 图片打不开 | 远程上传路径是否在 Web 根目录 `/assets/{简短标题}/` 下 | 移动到正确目录并重新生成 URL |
| URL 404 | 文件名、大小写、空格是否编码为 `%20`、扩展名是否与源图一致 | 统一为 `Figure%20N.ext` 并验证 |
| URL 403 | 远程权限或 Web 服务不可读 | 设置文件可读权限，通常为 `644` |
| URL 200 但图片错/损坏 | 上传中断、同名旧文件、格式错误 | 对比远程哈希或尺寸，重新上传 |
| 本地预览能显示但交付版不能显示 | HTML 仍引用本地路径、相对路径或浏览器缓存 | 全量搜索并替换为公开 URL，清缓存后复验 |

诊断输出必须包含：

- SFTP 连接是否成功、远程目录是否存在。
- 远程文件列表中是否存在规范文件名。
- `curl -I -L` 状态码。
- 本地源图与远程文件的哈希或尺寸对比。
- 最终 HTML 中 `<img src>` 的实际 URL。

若用户提供可用的 SFTP 账号信息，必须按该信息重新验证；除非命令返回明确认证失败，不得断言密码错误。

## CP 2 检查点

- [ ] 所有图片都有 URL
- [ ] 所有正文图片 URL 均指向 `https://medbam.org/assets/{简短标题}/`
- [ ] URL 格式正确（包含协议、文章短文件夹、规范图号文件名、扩展名）
- [ ] 上传后 HTTP 200，远程文件权限可读，哈希或尺寸已验证
- [ ] 最终 HTML 无本地图片引用残留
- [ ] 若图片打不开，已完成 SFTP、路径、权限、URL 编码、HTTP 状态和哈希/尺寸的分层诊断
