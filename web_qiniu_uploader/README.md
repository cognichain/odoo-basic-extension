[![License](https://img.shields.io/badge/license-LGPL--3.0-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0-standalone.html)

# Qiniu attachment uploader in form views

该模块利用了 `Odoo` 的 `ir.attachment` 附件模型可创建 `URL` 类型附件记录的能力，结合第三方云存储服务[七牛云](https://www.qiniu.com)将本地存储的资源存放到七牛云中。

## Todo

- [] 增加上传进度
- [] 添加错误处理

## Usage

- 配置七牛云的密钥等信息，进入开发模式，打开「设置 -> 第三方服务 -> 七牛云」菜单，并填写如下内容：

| 属性字段   	    | 说明               	|
|------------	|--------------------	|
| Access Key 	| 七牛云 Access Key  	|
| Secret Key 	| 七牛云 Secret Key  	|
| Bucket     	| 七牛云存储空间名称 	    |
| Domain     	| 七牛云融合 CDN 域名     |

其中 `AK` 和 `SK` 在七牛云的面板「个人中心 —- 密钥管理」内可找到，而 `Bucket` 和 `Domain` 则可以在存储空间列表中找到。

**注意：请勿在生产环境中使用测试域名，七牛会回收测试域名从而导致资源无法访问，请使用已备案域名绑定。**

- 在视图中定义 `ir.attachment` 附件字段时，添加属性 `context="{'default_res_model': 'your_model_name', 'default_public': True, 'default_type': 'url'}"` 到 `field` 标签内
- 在 `field` 中定义上传附件时打开的 `form` 视图，并在合适的位置加上 `<uploader />` 标签

```xml
...
<field name="attachment_ids" context="{'default_res_model': 'your_model_name', 'default_public': True, 'default_type': 'url'}">
    <form string="Attachments">
        ...
        <field name="name"/>
        <field name="url" widget="url"/>
        <field name="type" invisible="True"/>
        <field name="public" invisible="True"/>
        <field name="res_model" invisible="True"/>
        ...
        <group string="Qiniu Uploader" class="oe_edit_only">
            <uploader />
        </group>
    </form>
</field>
...
```

属性 `context` 里的 `default_*` 是为了给附件创建时的某些字段添加默认值，其中 `default_type` 是必需设置成 `url` 的。

标签 `<uploader />` 是上传组件，请在合适的位置放置该组件。

## Bug Tracker

如果遇到任何问题，欢迎在 [GitHub Issues](https://github.com/cognichain/odoo-basic-extension/issues) 进行反馈。

## Credits

### Contributors

- Ruter <i@ruterly.com>

### Maintainer

<img src="./static/description/icon.png" width="20%" alt="深圳市知链科技有限公司" />

该模块由深圳市知链科技有限公司开发及维护。