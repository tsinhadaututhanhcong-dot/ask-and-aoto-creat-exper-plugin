# Instructor | Hermes Agent
**Source:** [https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/mlops/mlops-instructor](https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/optional/mlops/mlops-instructor)

本页总览

使用 Pydantic 验证从 LLM 响应中提取结构化数据，自动重试失败的提取，以类型安全方式解析复杂 JSON，并使用 Instructor 流式传输部分结果——经过实战检验的结构化输出库

## Skill 元数据[​](#skill-元数据 "Skill 元数据的直接链接")

|  |  |
| --- | --- |
| 来源 | 可选 — 通过 `hermes skills install official/mlops/instructor` 安装 |
| 路径 | `optional-skills/mlops/instructor` |
| 版本 | `1.0.0` |
| 作者 | Orchestra Research |
| 许可证 | MIT |
| 依赖项 | `instructor`, `pydantic`, `openai`, `anthropic` |
| 平台 | linux, macos, windows |
| 标签 | `Prompt Engineering`, `Instructor`, `Structured Output`, `Pydantic`, `Data Extraction`, `JSON Parsing`, `Type Safety`, `Validation`, `Streaming`, `OpenAI`, `Anthropic` |

## 参考：完整 SKILL.md[​](#参考完整-skillmd "参考：完整 SKILL.md的直接链接")

信息

以下是 Hermes 在触发此 skill 时加载的完整 skill 定义。这是 skill 激活时 agent 所看到的指令内容。

# Instructor：结构化 LLM 输出

## 何时使用此 Skill[​](#何时使用此-skill "何时使用此 Skill的直接链接")

在以下情况下使用 Instructor：

* **从 LLM 响应中可靠地提取结构化数据**
* **根据 Pydantic schema 自动验证输出**
* **通过自动错误处理重试失败的提取**
* **以类型安全和验证方式解析复杂 JSON**
* **流式传输部分结果**以进行实时处理
* **以一致的 API 支持多个 LLM 提供商**

**GitHub Stars**：15,000+｜**实战检验**：100,000+ 开发者

## 安装[​](#安装 "安装的直接链接")

```
# 基础安装  
pip install instructor  
  
# 指定提供商  
pip install "instructor[anthropic]"  # Anthropic Claude  
pip install "instructor[openai]"     # OpenAI  
pip install "instructor[all]"        # 所有提供商
```

## 快速开始[​](#快速开始 "快速开始的直接链接")

### 基础示例：提取用户数据[​](#基础示例提取用户数据 "基础示例：提取用户数据的直接链接")

```
import instructor  
from pydantic import BaseModel  
from anthropic import Anthropic  
  
# Define output structure  
class User(BaseModel):  
    name: str  
    age: int  
    email: str  
  
# Create instructor client  
client = instructor.from_anthropic(Anthropic())  
  
# Extract structured data  
user = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": "John Doe is 30 years old. His email is john@example.com"  
    }],  
    response_model=User  
)  
  
print(user.name)   # "John Doe"  
print(user.age)    # 30  
print(user.email)  # "john@example.com"
```

### 使用 OpenAI[​](#使用-openai "使用 OpenAI的直接链接")

```
from openai import OpenAI  
  
client = instructor.from_openai(OpenAI())  
  
user = client.chat.completions.create(  
    model="gpt-4o-mini",  
    response_model=User,  
    messages=[{"role": "user", "content": "Extract: Alice, 25, alice@email.com"}]  
)
```

## 核心概念[​](#核心概念 "核心概念的直接链接")

### 1. 响应模型（Pydantic）[​](#1-响应模型pydantic "1. 响应模型（Pydantic）的直接链接")

响应模型定义 LLM 输出的结构和验证规则。

#### 基础模型[​](#基础模型 "基础模型的直接链接")

```
from pydantic import BaseModel, Field  
  
class Article(BaseModel):  
    title: str = Field(description="Article title")  
    author: str = Field(description="Author name")  
    word_count: int = Field(description="Number of words", gt=0)  
    tags: list[str] = Field(description="List of relevant tags")  
  
article = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": "Analyze this article: [article text]"  
    }],  
    response_model=Article  
)
```

**优势：**

* 使用 Python 类型提示保证类型安全
* 自动验证（word\_count > 0）
* 通过 Field 描述实现自文档化
* IDE 自动补全支持

#### 嵌套模型[​](#嵌套模型 "嵌套模型的直接链接")

```
class Address(BaseModel):  
    street: str  
    city: str  
    country: str  
  
class Person(BaseModel):  
    name: str  
    age: int  
    address: Address  # Nested model  
  
person = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": "John lives at 123 Main St, Boston, USA"  
    }],  
    response_model=Person  
)  
  
print(person.address.city)  # "Boston"
```

#### 可选字段[​](#可选字段 "可选字段的直接链接")

```
from typing import Optional  
  
class Product(BaseModel):  
    name: str  
    price: float  
    discount: Optional[float] = None  # Optional  
    description: str = Field(default="No description")  # Default value  
  
# LLM doesn't need to provide discount or description
```

#### 使用枚举约束值[​](#使用枚举约束值 "使用枚举约束值的直接链接")

```
from enum import Enum  
  
class Sentiment(str, Enum):  
    POSITIVE = "positive"  
    NEGATIVE = "negative"  
    NEUTRAL = "neutral"  
  
class Review(BaseModel):  
    text: str  
    sentiment: Sentiment  # Only these 3 values allowed  
  
review = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": "This product is amazing!"  
    }],  
    response_model=Review  
)  
  
print(review.sentiment)  # Sentiment.POSITIVE
```

### 2. 验证[​](#2-验证 "2. 验证的直接链接")

Pydantic 自动验证 LLM 输出。若验证失败，Instructor 会自动重试。

#### 内置验证器[​](#内置验证器 "内置验证器的直接链接")

```
from pydantic import Field, EmailStr, HttpUrl  
  
class Contact(BaseModel):  
    name: str = Field(min_length=2, max_length=100)  
    age: int = Field(ge=0, le=120)  # 0 <= age <= 120  
    email: EmailStr  # Validates email format  
    website: HttpUrl  # Validates URL format  
  
# If LLM provides invalid data, Instructor retries automatically
```

#### 自定义验证器[​](#自定义验证器 "自定义验证器的直接链接")

```
from pydantic import field_validator  
  
class Event(BaseModel):  
    name: str  
    date: str  
    attendees: int  
  
    @field_validator('date')  
    def validate_date(cls, v):  
        """Ensure date is in YYYY-MM-DD format."""  
        import re  
        if not re.match(r'\d{4}-\d{2}-\d{2}', v):  
            raise ValueError('Date must be YYYY-MM-DD format')  
        return v  
  
    @field_validator('attendees')  
    def validate_attendees(cls, v):  
        """Ensure positive attendees."""  
        if v < 1:  
            raise ValueError('Must have at least 1 attendee')  
        return v
```

#### 模型级验证[​](#模型级验证 "模型级验证的直接链接")

```
from pydantic import model_validator  
  
class DateRange(BaseModel):  
    start_date: str  
    end_date: str  
  
    @model_validator(mode='after')  
    def check_dates(self):  
        """Ensure end_date is after start_date."""  
        from datetime import datetime  
        start = datetime.strptime(self.start_date, '%Y-%m-%d')  
        end = datetime.strptime(self.end_date, '%Y-%m-%d')  
  
        if end < start:  
            raise ValueError('end_date must be after start_date')  
        return self
```

### 3. 自动重试[​](#3-自动重试 "3. 自动重试的直接链接")

当验证失败时，Instructor 会自动重试，并将错误反馈提供给 LLM。

```
# Retries up to 3 times if validation fails  
user = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": "Extract user from: John, age unknown"  
    }],  
    response_model=User,  
    max_retries=3  # Default is 3  
)  
  
# If age can't be extracted, Instructor tells the LLM:  
# "Validation error: age - field required"  
# LLM tries again with better extraction
```

**工作原理：**

1. LLM 生成输出
2. Pydantic 进行验证
3. 若无效：将错误信息发回给 LLM
4. LLM 根据错误反馈重新尝试
5. 重复直至达到 max\_retries 次数

### 4. 流式传输[​](#4-流式传输 "4. 流式传输的直接链接")

流式传输部分结果以进行实时处理。

#### 流式传输部分对象[​](#流式传输部分对象 "流式传输部分对象的直接链接")

```
from instructor import Partial  
  
class Story(BaseModel):  
    title: str  
    content: str  
    tags: list[str]  
  
# Stream partial updates as LLM generates  
for partial_story in client.messages.create_partial(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": "Write a short sci-fi story"  
    }],  
    response_model=Story  
):  
    print(f"Title: {partial_story.title}")  
    print(f"Content so far: {partial_story.content[:100]}...")  
    # Update UI in real-time
```

#### 流式传输可迭代对象[​](#流式传输可迭代对象 "流式传输可迭代对象的直接链接")

```
class Task(BaseModel):  
    title: str  
    priority: str  
  
# Stream list items as they're generated  
tasks = client.messages.create_iterable(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": "Generate 10 project tasks"  
    }],  
    response_model=Task  
)  
  
for task in tasks:  
    print(f"- {task.title} ({task.priority})")  
    # Process each task as it arrives
```

## 提供商配置[​](#提供商配置 "提供商配置的直接链接")

### Anthropic Claude[​](#anthropic-claude "Anthropic Claude的直接链接")

```
import instructor  
from anthropic import Anthropic  
  
client = instructor.from_anthropic(  
    Anthropic(api_key="your-api-key")  
)  
  
# Use with Claude models  
response = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[...],  
    response_model=YourModel  
)
```

### OpenAI[​](#openai "OpenAI的直接链接")

```
from openai import OpenAI  
  
client = instructor.from_openai(  
    OpenAI(api_key="your-api-key")  
)  
  
response = client.chat.completions.create(  
    model="gpt-4o-mini",  
    response_model=YourModel,  
    messages=[...]  
)
```

### 本地模型（Ollama）[​](#本地模型ollama "本地模型（Ollama）的直接链接")

```
from openai import OpenAI  
  
# Point to local Ollama server  
client = instructor.from_openai(  
    OpenAI(  
        base_url="http://localhost:11434/v1",  
        api_key="ollama"  # Required but ignored  
    ),  
    mode=instructor.Mode.JSON  
)  
  
response = client.chat.completions.create(  
    model="llama3.1",  
    response_model=YourModel,  
    messages=[...]  
)
```

## 常用模式[​](#常用模式 "常用模式的直接链接")

### 模式 1：从文本中提取数据[​](#模式-1从文本中提取数据 "模式 1：从文本中提取数据的直接链接")

```
class CompanyInfo(BaseModel):  
    name: str  
    founded_year: int  
    industry: str  
    employees: int  
    headquarters: str  
  
text = """  
Tesla, Inc. was founded in 2003. It operates in the automotive and energy  
industry with approximately 140,000 employees. The company is headquartered  
in Austin, Texas.  
"""  
  
company = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": f"Extract company information from: {text}"  
    }],  
    response_model=CompanyInfo  
)
```

### 模式 2：分类[​](#模式-2分类 "模式 2：分类的直接链接")

```
class Category(str, Enum):  
    TECHNOLOGY = "technology"  
    FINANCE = "finance"  
    HEALTHCARE = "healthcare"  
    EDUCATION = "education"  
    OTHER = "other"  
  
class ArticleClassification(BaseModel):  
    category: Category  
    confidence: float = Field(ge=0.0, le=1.0)  
    keywords: list[str]  
  
classification = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": "Classify this article: [article text]"  
    }],  
    response_model=ArticleClassification  
)
```

### 模式 3：多实体提取[​](#模式-3多实体提取 "模式 3：多实体提取的直接链接")

```
class Person(BaseModel):  
    name: str  
    role: str  
  
class Organization(BaseModel):  
    name: str  
    industry: str  
  
class Entities(BaseModel):  
    people: list[Person]  
    organizations: list[Organization]  
    locations: list[str]  
  
text = "Tim Cook, CEO of Apple, announced at the event in Cupertino..."  
  
entities = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": f"Extract all entities from: {text}"  
    }],  
    response_model=Entities  
)  
  
for person in entities.people:  
    print(f"{person.name} - {person.role}")
```

### 模式 4：结构化分析[​](#模式-4结构化分析 "模式 4：结构化分析的直接链接")

```
class SentimentAnalysis(BaseModel):  
    overall_sentiment: Sentiment  
    positive_aspects: list[str]  
    negative_aspects: list[str]  
    suggestions: list[str]  
    score: float = Field(ge=-1.0, le=1.0)  
  
review = "The product works well but setup was confusing..."  
  
analysis = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[{  
        "role": "user",  
        "content": f"Analyze this review: {review}"  
    }],  
    response_model=SentimentAnalysis  
)
```

### 模式 5：批量处理[​](#模式-5批量处理 "模式 5：批量处理的直接链接")

```
def extract_person(text: str) -> Person:  
    return client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": f"Extract person from: {text}"  
        }],  
        response_model=Person  
    )  
  
texts = [  
    "John Doe is a 30-year-old engineer",  
    "Jane Smith, 25, works in marketing",  
    "Bob Johnson, age 40, software developer"  
]  
  
people = [extract_person(text) for text in texts]
```

## 高级特性[​](#高级特性 "高级特性的直接链接")

### 联合类型[​](#联合类型 "联合类型的直接链接")

```
from typing import Union  
  
class TextContent(BaseModel):  
    type: str = "text"  
    content: str  
  
class ImageContent(BaseModel):  
    type: str = "image"  
    url: HttpUrl  
    caption: str  
  
class Post(BaseModel):  
    title: str  
    content: Union[TextContent, ImageContent]  # Either type  
  
# LLM chooses appropriate type based on content
```

### 动态模型[​](#动态模型 "动态模型的直接链接")

```
from pydantic import create_model  
  
# Create model at runtime  
DynamicUser = create_model(  
    'User',  
    name=(str, ...),  
    age=(int, Field(ge=0)),  
    email=(EmailStr, ...)  
)  
  
user = client.messages.create(  
    model="claude-sonnet-4-5-20250929",  
    max_tokens=1024,  
    messages=[...],  
    response_model=DynamicUser  
)
```

### 自定义模式[​](#自定义模式 "自定义模式的直接链接")

```
# For providers without native structured outputs  
client = instructor.from_anthropic(  
    Anthropic(),  
    mode=instructor.Mode.JSON  # JSON mode  
)  
  
# Available modes:  
# - Mode.ANTHROPIC_TOOLS (recommended for Claude)  
# - Mode.JSON (fallback)  
# - Mode.TOOLS (OpenAI tools)
```

### 上下文管理[​](#上下文管理 "上下文管理的直接链接")

```
# Single-use client  
with instructor.from_anthropic(Anthropic()) as client:  
    result = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[...],  
        response_model=YourModel  
    )  
    # Client closed automatically
```

## 错误处理[​](#错误处理 "错误处理的直接链接")

### 处理验证错误[​](#处理验证错误 "处理验证错误的直接链接")

```
from pydantic import ValidationError  
  
try:  
    user = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[...],  
        response_model=User,  
        max_retries=3  
    )  
except ValidationError as e:  
    print(f"Failed after retries: {e}")  
    # Handle gracefully  
  
except Exception as e:  
    print(f"API error: {e}")
```

### 自定义错误信息[​](#自定义错误信息 "自定义错误信息的直接链接")

```
class ValidatedUser(BaseModel):  
    name: str = Field(description="Full name, 2-100 characters")  
    age: int = Field(description="Age between 0 and 120", ge=0, le=120)  
    email: EmailStr = Field(description="Valid email address")  
  
    class Config:  
        # Custom error messages  
        json_schema_extra = {  
            "examples": [  
                {  
                    "name": "John Doe",  
                    "age": 30,  
                    "email": "john@example.com"  
                }  
            ]  
        }
```

## 最佳实践[​](#最佳实践 "最佳实践的直接链接")

### 1. 清晰的字段描述[​](#1-清晰的字段描述 "1. 清晰的字段描述的直接链接")

```
# ❌ Bad: Vague  
class Product(BaseModel):  
    name: str  
    price: float  
  
# ✅ Good: Descriptive  
class Product(BaseModel):  
    name: str = Field(description="Product name from the text")  
    price: float = Field(description="Price in USD, without currency symbol")
```

### 2. 使用适当的验证[​](#2-使用适当的验证 "2. 使用适当的验证的直接链接")

```
# ✅ Good: Constrain values  
class Rating(BaseModel):  
    score: int = Field(ge=1, le=5, description="Rating from 1 to 5 stars")  
    review: str = Field(min_length=10, description="Review text, at least 10 chars")
```

### 3. 在 prompt（提示词）中提供示例[​](#3-在-prompt提示词中提供示例 "3. 在 prompt（提示词）中提供示例的直接链接")

```
messages = [{  
    "role": "user",  
    "content": """Extract person info from: "John, 30, engineer"  
  
Example format:  
{  
  "name": "John Doe",  
  "age": 30,  
  "occupation": "engineer"  
}"""  
}]
```

### 4. 对固定类别使用枚举[​](#4-对固定类别使用枚举 "4. 对固定类别使用枚举的直接链接")

```
# ✅ Good: Enum ensures valid values  
class Status(str, Enum):  
    PENDING = "pending"  
    APPROVED = "approved"  
    REJECTED = "rejected"  
  
class Application(BaseModel):  
    status: Status  # LLM must choose from enum
```

### 5. 优雅处理缺失数据[​](#5-优雅处理缺失数据 "5. 优雅处理缺失数据的直接链接")

```
class PartialData(BaseModel):  
    required_field: str  
    optional_field: Optional[str] = None  
    default_field: str = "default_value"  
  
# LLM only needs to provide required_field
```

## 与其他方案的对比[​](#与其他方案的对比 "与其他方案的对比的直接链接")

| 特性 | Instructor | 手动 JSON | LangChain | DSPy |
| --- | --- | --- | --- | --- |
| 类型安全 | ✅ 是 | ❌ 否 | ⚠️ 部分 | ✅ 是 |
| 自动验证 | ✅ 是 | ❌ 否 | ❌ 否 | ⚠️ 有限 |
| 自动重试 | ✅ 是 | ❌ 否 | ❌ 否 | ✅ 是 |
| 流式传输 | ✅ 是 | ❌ 否 | ✅ 是 | ❌ 否 |
| 多提供商 | ✅ 是 | ⚠️ 手动 | ✅ 是 | ✅ 是 |
| 学习曲线 | 低 | 低 | 中 | 高 |

**何时选择 Instructor：**

* 需要结构化、经过验证的输出
* 需要类型安全和 IDE 支持
* 需要自动重试
* 构建数据提取系统

**何时选择其他方案：**

* DSPy：需要 prompt 优化
* LangChain：构建复杂链路
* 手动：简单的一次性提取

## 资源[​](#资源 "资源的直接链接")

* **文档**：<https://python.useinstructor.com>
* **GitHub**：[https://github.com/jxnl/instructor（15k+](https://github.com/jxnl/instructor%EF%BC%8815k+) stars）
* **Cookbook**：<https://python.useinstructor.com/examples>
* **Discord**：提供社区支持

## 另请参阅[​](#另请参阅 "另请参阅的直接链接")

* `references/validation.md` — 高级验证模式
* `references/providers.md` — 提供商专项配置
* `references/examples.md` — 真实使用案例

* [Skill 元数据](#skill-元数据)
* [参考：完整 SKILL.md](#参考完整-skillmd)
* [何时使用此 Skill](#何时使用此-skill)
* [安装](#安装)
* [快速开始](#快速开始)
  + [基础示例：提取用户数据](#基础示例提取用户数据)
  + [使用 OpenAI](#使用-openai)
* [核心概念](#核心概念)
  + [1. 响应模型（Pydantic）](#1-响应模型pydantic)
  + [2. 验证](#2-验证)
  + [3. 自动重试](#3-自动重试)
  + [4. 流式传输](#4-流式传输)
* [提供商配置](#提供商配置)
  + [Anthropic Claude](#anthropic-claude)
  + [OpenAI](#openai)
  + [本地模型（Ollama）](#本地模型ollama)
* [常用模式](#常用模式)
  + [模式 1：从文本中提取数据](#模式-1从文本中提取数据)
  + [模式 2：分类](#模式-2分类)
  + [模式 3：多实体提取](#模式-3多实体提取)
  + [模式 4：结构化分析](#模式-4结构化分析)
  + [模式 5：批量处理](#模式-5批量处理)
* [高级特性](#高级特性)
  + [联合类型](#联合类型)
  + [动态模型](#动态模型)
  + [自定义模式](#自定义模式)
  + [上下文管理](#上下文管理)
* [错误处理](#错误处理)
  + [处理验证错误](#处理验证错误)
  + [自定义错误信息](#自定义错误信息)
* [最佳实践](#最佳实践)
  + [1. 清晰的字段描述](#1-清晰的字段描述)
  + [2. 使用适当的验证](#2-使用适当的验证)
  + [3. 在 prompt（提示词）中提供示例](#3-在-prompt提示词中提供示例)
  + [4. 对固定类别使用枚举](#4-对固定类别使用枚举)
  + [5. 优雅处理缺失数据](#5-优雅处理缺失数据)
* [与其他方案的对比](#与其他方案的对比)
* [资源](#资源)
* [另请参阅](#另请参阅)