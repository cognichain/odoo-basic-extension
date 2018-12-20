[![License](https://img.shields.io/badge/license-LGPL--3.0-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0-standalone.html)

# Open many2many_tags record in form views

该模块可以在只读模式下打开 `many2many_tags` 对应的记录的表单视图。

## Usage

- 在定义表单字段时，添加属性 `{'open_view': True}` 到 `widget="many2many_tags"` 的字段的 `options` 中：

```xml
<!-- 在非编辑状态下点击字段 category_id 的 tag 将会打开对应记录的表单视图 -->
...
<field name="arch" type="xml">
    <form string="View name">
        ...
        <field name="category_id" widget="many2many_tags" options="{'open_view': True}"/>
        ...
    </form>
</field>
...
```

## Bug Tracker

如果遇到任何问题，欢迎在 [GitHub Issues](https://github.com/cognichain/odoo-basic-extension/issues) 进行反馈。

## Credits

### Contributors

- Ruter <i@ruterly.com>

### Maintainer

<img src="./static/description/icon.png" width="20%" alt="深圳市知链科技有限公司" />

该模块由深圳市知链科技有限公司开发及维护。