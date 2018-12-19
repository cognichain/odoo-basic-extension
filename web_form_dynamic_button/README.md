[![License](https://img.shields.io/badge/license-LGPL--3.0-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0-standalone.html)

# Hide buttons in form views

该模块可根据表达式对表单视图上的控制按钮进行动态显示或隐藏，目前支持对如下按钮进行处理：

- 编辑按钮 `Edit`
- 创建按钮 `Create`
- 删除按钮 `Delete`
- 复制按钮 `Duplicate`

## Features

- 添加属性 `edit_expr` 到表单 `form` 标签中以在表达式成立时才显示编辑按钮
- 添加属性 `create_expr` 到表单 `form` 标签中以在表达式成立时才显示创建按钮
- 添加属性 `delete_expr` 到表单 `form` 标签中以在表达式成立时才显示删除按钮
- 添加属性 `duplicate_expr` 到表单 `form` 标签中以在表达式成立时才显示复制按钮

## Usage

- 在定义表单视图时，添加属性 `edit_expr="state == 'draft'"` 到 `form` 标签内：

```xml
<!-- 在该例中，当 state 不为 draft 时，编辑按钮将会被隐藏，反之则会显示 -->
...
<field name="arch" type="xml">
    <form string="View name" edit_expr="state == 'draft'">
        <header>
            <field name="state" widget="statusbar" statusbar_visible="draft,done" nolabel="1" readonly="1"/>
        </header>
        ...
        <field name="name"/>
        ...
    </form>
</field>
...
```

在 `Features` 中列出的属性可以同时使用，如上例所示，直接添加相应的属性到 `form` 标签中即可。

## Bug Tracker

如果遇到任何问题，欢迎在 [GitHub Issues](https://github.com/cognichain/odoo-basic-extension/issues) 进行反馈。

## Credits

### Contributors

- Ruter <i@ruterly.com>

### Maintainer

<img src="./static/description/icon.png" width="20%" alt="深圳市知链科技有限公司" />

该模块由深圳市知链科技有限公司开发及维护。