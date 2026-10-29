# JetBrains 运行配置模板（.run/*.run.xml）

放在项目根目录 `.run/` 下，JetBrains IDE 自动加载。文件名即配置名：`code-walk-<topic>.run.xml`。

通用占位符：

- `<topic>`：本次 debug 主题（kebab-case）
- `<module>`：IDE 模块名，取 `.idea/modules.xml` 里的条目或 `*.iml` 文件名（不带扩展名）
- `$PROJECT_DIR$`：JetBrains 内置宏，指项目根目录，原样保留

<rules>
- 只选与项目语言对应的一个模板，按需填占位符，其余原样。
- `module` 名写错是"配置不被 IDE 识别"的最常见原因；查 `.idea/modules.xml` 确认。
</rules>

## Java / Kotlin（IntelliJ，`type="Application"`）

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="code-walk-<topic>" type="Application" factoryName="Application">
    <option name="MAIN_CLASS_NAME" value="com.example.DebugEntry" />
    <module name="<module>" />
    <option name="PROGRAM_PARAMETERS" value="" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <method v="2">
      <option name="Make" enabled="true" />
    </method>
  </configuration>
</component>
```

- Kotlin 的顶层 `main` 函数：入口类是 `文件名Kt`，如 `MainKt`。
- 跑测试而非 main：把 `type` 换成 `JUnit`（Java/Kotlin），`MAIN_CLASS_NAME` 换成 `<option name="MAIN_CLASS_NAME" value="com.example.SomeTest" />`，并加 `<option name="TEST_OBJECT" value="class" />`。

## Go（GoLand，`type="GoApplicationRunConfiguration"`）

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="code-walk-<topic>" type="GoApplicationRunConfiguration" factoryName="Go Application">
    <module name="<module>" />
    <option name="PACKAGE" value="example.com/project/cmd/debug-entry" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="PROGRAM_PARAMETERS" value="" />
    <method v="2" />
  </configuration>
</component>
```

- `PACKAGE` 填包路径（`go list ./...` 可查），不是文件路径。
- 跑测试：把 `type` 换成 `GoTestRunConfiguration`，`factoryName` 换成 `Go Test`，加 `<option name="TESTING_TYPE" value="package" />`。

## Python（PyCharm，`type="PythonConfigurationType"`）

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="code-walk-<topic>" type="PythonConfigurationType" factoryName="Python">
    <module name="<module>" />
    <option name="SCRIPT_NAME" value="$PROJECT_DIR$/examples/debug_entry.py" />
    <option name="PARAMETERS" value="" />
    <option name="WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="SDK_HOME" value="" />
    <method v="2" />
  </configuration>
</component>
```

- `SDK_HOME` 留空表示用项目解释器。
- 跑 pytest：把 `type` 换成 `tests`，`factoryName` 换成 `py.test`，`SCRIPT_NAME` 换成 `<option name="TARGET" value="$PROJECT_DIR$/tests/test_x.py" />`，并加 `<option name="TARGET_TYPE" value="PATH" />`。
