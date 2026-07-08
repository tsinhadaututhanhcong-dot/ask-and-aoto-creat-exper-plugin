# Blender Mcp — 通过 socket 连接 blender-mcp 插件，直接从 Hermes 控制 Blender | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/creative/creative-blender-mcp](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/creative/creative-blender-mcp)

本页总览

通过 socket 连接 blender-mcp 插件，直接从 Hermes 控制 Blender。可创建 3D 对象、材质、动画，并运行任意 Blender Python（bpy）代码。当用户需要在 Blender 中创建或修改任何内容时使用。

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选 — 通过 `hermes skills install official/creative/blender-mcp` 安装 |
| 路径 | `optional-skills/creative/blender-mcp` |
| 版本 | `1.0.0` |
| 作者 | alireza78a |
| 平台 | linux, macos, windows |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 agent 在 skill 激活时所看到的指令内容。

# Blender MCP

通过 TCP 端口 9876 上的 socket，从 Hermes 控制正在运行的 Blender 实例。

## 设置（一次性）[​](#设置一次性 "设置（一次性）的直接链接")

### 1. 安装 Blender 插件[​](#1-安装-blender-插件 "1. 安装 Blender 插件的直接链接")

curl -sL <https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py> -o ~/Desktop/blender\_mcp\_addon.py

在 Blender 中：
Edit > Preferences > Add-ons > Install > 选择 blender\_mcp\_addon.py
启用 "Interface: Blender MCP"

### 2. 在 Blender 中启动 socket 服务器[​](#2-在-blender-中启动-socket-服务器 "2. 在 Blender 中启动 socket 服务器的直接链接")

在 Blender 视口中按 N 键打开侧边栏。
找到 "BlenderMCP" 标签页，点击 "Start Server"。

### 3. 验证连接[​](#3-验证连接 "3. 验证连接的直接链接")

nc -z -w2 localhost 9876 && echo "OPEN" || echo "CLOSED"

## 协议[​](#协议 "协议的直接链接")

通过 TCP 传输纯 UTF-8 JSON — 无长度前缀。

发送： {"type": "<command>", "params": {<kwargs>}}
接收： {"status": "success", "result": <value>}
{"status": "error", "message": "<reason>"}

## 可用命令[​](#可用命令 "可用命令的直接链接")

| type | params | 说明 |
| --- | --- | --- |
| execute\_code | code (str) | 运行任意 bpy Python 代码 |
| get\_scene\_info | （无） | 列出场景中的所有对象 |
| get\_object\_info | object\_name (str) | 获取特定对象的详细信息 |
| get\_viewport\_screenshot | （无） | 截取当前视口截图 |

## Python 辅助函数[​](#python-辅助函数 "Python 辅助函数的直接链接")

在 execute\_code 工具调用中使用：

import socket, json

def blender\_exec(code: str, host="localhost", port=9876, timeout=15):
s = socket.socket(socket.AF\_INET, socket.SOCK\_STREAM)
s.connect((host, port))
s.settimeout(timeout)
payload = json.dumps({"type": "execute\_code", "params": {"code": code}})
s.sendall(payload.encode("utf-8"))
buf = b""
while True:
try:
chunk = s.recv(4096)
if not chunk:
break
buf += chunk
try:
json.loads(buf.decode("utf-8"))
break
except json.JSONDecodeError:
continue
except socket.timeout:
break
s.close()
return json.loads(buf.decode("utf-8"))

## 常用 bpy 模式[​](#常用-bpy-模式 "常用 bpy 模式的直接链接")

### 清空场景[​](#清空场景 "清空场景的直接链接")

bpy.ops.object.select\_all(action='SELECT')
bpy.ops.object.delete()

### 添加网格对象[​](#添加网格对象 "添加网格对象的直接链接")

bpy.ops.mesh.primitive\_uv\_sphere\_add(radius=1, location=(0, 0, 0))
bpy.ops.mesh.primitive\_cube\_add(size=2, location=(3, 0, 0))
bpy.ops.mesh.primitive\_cylinder\_add(radius=0.5, depth=2, location=(-3, 0, 0))

### 创建并指定材质[​](#创建并指定材质 "创建并指定材质的直接链接")

mat = bpy.data.materials.new(name="MyMat")
mat.use\_nodes = True
bsdf = mat.node\_tree.nodes.get("Principled BSDF")
bsdf.inputs["Base Color"].default\_value = (R, G, B, 1.0)
bsdf.inputs["Roughness"].default\_value = 0.3
bsdf.inputs["Metallic"].default\_value = 0.0
obj.data.materials.append(mat)

### 关键帧动画[​](#关键帧动画 "关键帧动画的直接链接")

obj.location = (0, 0, 0)
obj.keyframe\_insert(data\_path="location", frame=1)
obj.location = (0, 0, 3)
obj.keyframe\_insert(data\_path="location", frame=60)

### 渲染到文件[​](#渲染到文件 "渲染到文件的直接链接")

bpy.context.scene.render.filepath = "/tmp/render.png"
bpy.context.scene.render.engine = 'CYCLES'
bpy.ops.render.render(write\_still=True)

## 注意事项[​](#注意事项 "注意事项的直接链接")

* 运行前必须检查 socket 是否已开放（nc -z localhost 9876）
* 每次会话都需要在 Blender 内部启动插件服务器（N 面板 > BlenderMCP > Connect）
* 将复杂场景拆分为多个较小的 execute\_code 调用，以避免超时
* 渲染输出路径必须为绝对路径（/tmp/...），不能使用相对路径
* `shade_smooth()` 要求对象已被选中且处于对象模式

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [设置（一次性）](#设置一次性)
  + [1. 安装 Blender 插件](#1-安装-blender-插件)
  + [2. 在 Blender 中启动 socket 服务器](#2-在-blender-中启动-socket-服务器)
  + [3. 验证连接](#3-验证连接)
* [协议](#协议)
* [可用命令](#可用命令)
* [Python 辅助函数](#python-辅助函数)
* [常用 bpy 模式](#常用-bpy-模式)
  + [清空场景](#清空场景)
  + [添加网格对象](#添加网格对象)
  + [创建并指定材质](#创建并指定材质)
  + [关键帧动画](#关键帧动画)
  + [渲染到文件](#渲染到文件)
* [注意事项](#注意事项)