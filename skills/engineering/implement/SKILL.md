---
name: implement
description: "基于 spec（规格说明）或一组工单（ticket）实现一项工作。"
disable-model-invocation: true
---

实现用户在 spec 或工单中描述的工作。

尽可能使用 /tdd，在事先约定的接缝（seam）处进行。

定期运行类型检查，定期运行单个测试文件，最后运行一次完整测试套件。

完成后，用 /code-review 审查这项工作。

把你的工作提交到当前分支。
