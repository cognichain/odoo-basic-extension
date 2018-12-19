[![License](https://img.shields.io/badge/license-LGPL--3.0-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0-standalone.html)

# Colorize field in form views

这个模块添加了根据表达式动态渲染字段颜色的能力支持，可用的字段类型及其对应的 `widget` 如下表：

| 字段类型    	| Widget 名       	|
|-----------	|-----------------	|
| Char      	| color_char      	|
| Float     	| color_float     	|
| Integer   	| color_integer   	|
| Selection 	| color_selection 	|

## Features

- 添加属性 `color` 到表单字段 `field` 的 `options` 中以在表达式 `expr` 成立时渲染该字段的颜色
- 添加属性 `title` 到表单字段 `field` 的 `options` 中以在表达式 `expr` 成立时为该字段添加 `tooltip` 显示 `title` 中的内容

## Usage

- 在定义表单视图中的字段时，添加属性 `widget="color_float"` 以及 `options="{'color': 'red', 'expr': 'cost != price'}"` 到 `field` 标签内：

```xml
<!-- 在该例中，当 cost 和 price 不相等时，字段 cost 将会以红色字体显示其值 -->
...
<field name="arch" type="xml">
    <form string="View name">
        ...
        <field name="cost" widget="color_float" options="{'color': 'red', 'expr': 'cost != price'}"/>
        <field name="price"/>
    </form>
</field>
...
```

- 在定义表单视图中的字段时，添加属性 `widget="color_char"` 以及 `options="{'color': 'blue', 'title': 'It's same!, 'expr': 'a != b'}"` 到 `field` 标签内：

```xml
<!-- 在该例中，当 a 和 b 相等时，字段 a 将会以蓝色字体显示其值，且当鼠标指针停留在字段 a 上时会弹出一个 tooltip 并显示 title 中的内容 -->
...
<field name="arch" type="xml">
    <form string="View name">
        ...
        <field name="a" widget="color_char" options="{'color': 'blue', 'title': 'It's same!, 'expr': 'a == b'}"/>
        <field name="b"/>
    </form>
</field>
...
```

属性 `options` 中的 `title` 是非必需的，可以仅在需要增加提示信息时添加该属性；其中颜色属性 `color` 可以是 CSS 中的颜色关键字，也可以是十六进制表示的颜色值（如白色 `#FFFFFF`）。

## Bug Tracker

如果遇到任何问题，欢迎在 [GitHub Issues](https://github.com/cognichain/odoo-basic-extension/issues) 进行反馈。

## Credits

### Contributors

- Ruter <i@ruterly.com>

### Maintainer

<img src="./static/description/icon.png" width="20%" alt="深圳市知链科技有限公司" />

该模块由深圳市知链科技有限公司开发及维护。